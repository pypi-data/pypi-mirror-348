#include "posFeatureExtractor.h"

#ifdef _WIN32
#   define API __declspec(dllexport)
#else
#   define API
#endif

int getBigramFeature(
    const wchar_t *flagToken, int flagTokenLength, const wchar_t *mark,
    PyObject *firstWord, PyObject *secondWord,
    int firstWordLength, int secondWordLength,
    PyObject *featureList)
{
    Py_ssize_t firstWordLengthPy = (Py_ssize_t)firstWordLength;
    Py_ssize_t secondWordLengthPy = (Py_ssize_t)secondWordLength;
    wchar_t *firstWordWideChar = PyUnicode_AsWideCharString(firstWord, &firstWordLengthPy);
    wchar_t *secondWordWideChar = PyUnicode_AsWideCharString(secondWord, &secondWordLengthPy);

    wchar_t *biWordFeature = malloc(
        (firstWordLength + secondWordLength + flagTokenLength + 1) * sizeof(wchar_t));
    wcsncpy(biWordFeature, flagToken, flagTokenLength);
    wcsncpy(biWordFeature + flagTokenLength, firstWordWideChar, firstWordLength);
    wcsncpy(biWordFeature + flagTokenLength + firstWordLength, mark, 1);
    wcsncpy(biWordFeature + flagTokenLength + firstWordLength + 1, secondWordWideChar, secondWordLength);

    PyObject *tmpPythonStr = PyUnicode_FromWideChar(
        biWordFeature, firstWordLength + secondWordLength + flagTokenLength + 1);
    int ret = PyList_Append(featureList, tmpPythonStr);

    Py_DECREF(tmpPythonStr);
    free(biWordFeature);
    biWordFeature = NULL;

    PyMem_Free(firstWordWideChar);
    PyMem_Free(secondWordWideChar);
    firstWordWideChar = NULL;
    secondWordWideChar = NULL;

    return ret;
}

int getUnigramFeatureWideChar(
    const wchar_t *flagToken, int flagTokenLength, wchar_t *word,
    Py_ssize_t wordLength, PyObject *featureList)
{
    int ret = -1;
    PyObject *tmpPythonStr;

    wchar_t *feature = malloc((flagTokenLength + wordLength) * sizeof(wchar_t));
    wcsncpy(feature, flagToken, flagTokenLength);
    wcsncpy(feature + flagTokenLength, word, wordLength);
    tmpPythonStr = PyUnicode_FromWideChar(feature, flagTokenLength + wordLength);
    ret = PyList_Append(featureList, tmpPythonStr);

    Py_DECREF(tmpPythonStr);
    free(feature);
    feature = NULL;

    return ret;
}

int getUnigramFeaturePythonString(
    const wchar_t *flagToken, int flagTokenLength, PyObject *word, Py_ssize_t wordLength,
    PyObject *featureList)
{
    int ret = -1;
    PyObject *tmpPythonStr;

    wchar_t *wordWideChar = PyUnicode_AsWideCharString(word, &wordLength);

    wchar_t *feature = malloc((flagTokenLength + wordLength) * sizeof(wchar_t));
    wcsncpy(feature, flagToken, flagTokenLength);
    wcsncpy(feature + flagTokenLength, wordWideChar, wordLength);
    tmpPythonStr = PyUnicode_FromWideChar(feature, flagTokenLength + wordLength);
    ret = PyList_Append(featureList, tmpPythonStr);

    Py_DECREF(tmpPythonStr);
    free(feature);
    feature = NULL;

    PyMem_Free(wordWideChar);
    wordWideChar = NULL;

    return ret;
}

int getUnknownFeature(
    const wchar_t *flagToken, int flagTokenLength, PyObject *featureList)
{
    int ret = -1;
    PyObject *tmpPythonStr;

    tmpPythonStr = PyUnicode_FromWideChar(flagToken, flagTokenLength);
    ret = PyList_Append(featureList, tmpPythonStr);

    Py_DECREF(tmpPythonStr);

    return ret;
}

/**
 * @brief Get the Node Feature Python object
 * 函数压缩方法为尽量减少对 py 内置函数的调用，而采用 C 和 参数方式进行传递
 *
 * @param idx: 处理的词汇索引
 * @param wordList: 词汇列表
 * @param nodeNum: 节点数
 * @param part: 部分词特征，主要是针对汉字的部分词采集的特征
 * @param unigram: 独词集，主要包括常见词汇
 * @param chars: 字符集，不包括汉字，仅包括一些数字、字母、常见符号等
 * @return PyObject*
 */
API PyObject *getPosNodeFeature(
    int idx, PyObject *wordList, // int wordListLength,
    PyObject *part, PyObject *unigram, PyObject *chars)
{
    int ret = -1;
    PyObject *tmpPyStr;

    Py_ssize_t wordListLength = PyList_Size(wordList);
    PyObject *featureList = PyList_New(0);
    PyObject *currentWord = PyList_GetItem(wordList, idx);

    // 获取词长
    Py_ssize_t currentWordLength = PyUnicode_GET_LENGTH(currentWord);

    int maxPartLength = 5;

    int before_word = 0; // 此类均为指示 flag，所指示内容为其词长，为寻找 bigram 拼凑特征
    int before_left = 0;
    int before_right = 0;
    PyObject *beforeWordGlobal = NULL;
    PyObject *beforeWordPartLeftGlobal = NULL;
    PyObject *beforeWordPartRightGlobal = NULL;

    int current_word = 0;
    int current_left = 0;
    int current_right = 0;
    PyObject *currentWordGlobal = NULL;
    PyObject *currentWordPartLeftGlobal = NULL;
    PyObject *currentWordPartRightGlobal = NULL;

    int next_word = 0;
    int next_left = 0;
    int next_right = 0;
    PyObject *nextWordGlobal = NULL;
    PyObject *nextWordPartLeftGlobal = NULL;
    PyObject *nextWordPartRightGlobal = NULL;

    if (idx > 0)
    {
        // 获取前一词
        PyObject *beforeWord = PyList_GetItem(wordList, idx - 1);
        ret = PySet_Contains(unigram, beforeWord);

        if (ret == 1)
        {
            beforeWordGlobal = beforeWord;
            before_word = PyUnicode_GET_LENGTH(beforeWordGlobal);
            ret = getUnigramFeaturePythonString(L"v", 1, beforeWord, before_word, featureList);
            beforeWord = NULL;
        }
        else
        {
            const wchar_t *partBeforeLeftToken = L"bl";

            Py_ssize_t beforeWordLength = PyUnicode_GET_LENGTH(beforeWord);
            Py_ssize_t beforeWordTrimLength = min(beforeWordLength, maxPartLength);

            // 转换为 wchar_t*
            wchar_t *beforeWordTmp = PyUnicode_AsWideCharString(beforeWord, &beforeWordLength);

            for (int i = beforeWordTrimLength - 1; i > 0; i--)
            {
                // 左侧部分词特征
                wchar_t *beforeWordPartLeft = malloc(i * sizeof(wchar_t)); // 长度不定，如 “v中国”
                wcsncpy(beforeWordPartLeft, beforeWordTmp, i);

                PyObject *beforeWordPartLeftTmp = PyUnicode_FromWideChar(beforeWordPartLeft, i);
                // printf("cur left %ls\n", beforeWordPartLeft);
                ret = PySet_Contains(part, beforeWordPartLeftTmp);

                if (ret == 1)
                {
                    // 添加特征
                    ret = getUnigramFeatureWideChar(
                        partBeforeLeftToken, 2, beforeWordPartLeft, i, featureList);

                    // 将临时变量赋给全局变量，为bigram 特征做准备
                    beforeWordPartLeftGlobal = beforeWordPartLeftTmp;
                    before_left = i;

                    // Py_DECREF(beforeWordPartLeftTmp);
                    beforeWordPartLeftTmp = NULL;
                    free(beforeWordPartLeft);
                    beforeWordPartLeft = NULL;

                    break;
                }
                else {
                    Py_DECREF(beforeWordPartLeftTmp);
                    free(beforeWordPartLeft);
                    beforeWordPartLeft = NULL;
                }

            }

            const wchar_t *partBeforeRightToken = L"br";

            for (int i = beforeWordTrimLength - 1; i > 0; i--)
            {
                // 右侧部分词特征
                wchar_t *beforeWordPartRight = malloc(i * sizeof(wchar_t));
                wcsncpy(beforeWordPartRight, beforeWordTmp + beforeWordLength - i, i);

                PyObject *beforeWordPartRightTmp = PyUnicode_FromWideChar(beforeWordPartRight, i);
                ret = PySet_Contains(part, beforeWordPartRightTmp);
                // printf("ret right: %d\t%ls\n", ret, beforeWordPartRight);
                if (ret == 1)
                {
                    // 添加特征
                    ret = getUnigramFeatureWideChar(
                        partBeforeRightToken, 2, beforeWordPartRight, i, featureList);

                    beforeWordPartRightGlobal = beforeWordPartRightTmp;
                    before_right = i;

                    // Py_DECREF(beforeWordPartRightTmp);
                    beforeWordPartRightTmp = NULL;
                    free(beforeWordPartRight);
                    beforeWordPartRight = NULL;

                    break;
                }
                else {
                    Py_DECREF(beforeWordPartRightTmp);
                    free(beforeWordPartRight);
                    beforeWordPartRight = NULL;
                }
            }

            PyMem_Free(beforeWordTmp);
            beforeWordTmp = NULL;

            if (before_left == 0 && before_right == 0)
            {
                ret = getUnknownFeature(L"vk", 2, featureList);
            }
        }
    }
    else
    {
        // 添加起始符特征
        ret = getUnknownFeature(L"[START]", 7, featureList);
    }

    // 考察当前一词
    ret = PySet_Contains(unigram, currentWord);
    if (ret == 1)
    {
        ret = getUnigramFeaturePythonString(L"w", 1, currentWord, currentWordLength, featureList);

        currentWordGlobal = currentWord;
        current_word = currentWordLength;
        currentWord = NULL;
    }
    else
    {
        const wchar_t *partCurrentLeftToken = L"cl";

        Py_ssize_t currentWordTrimLength = min(currentWordLength, maxPartLength);

        // 转换为 wchar_t*
        wchar_t *currentWordTmp = PyUnicode_AsWideCharString(currentWord, &currentWordLength);

        for (int i = currentWordTrimLength - 1; i > 0; i--)
        {
            // 左侧部分词特征
            wchar_t *currentWordPartLeft = malloc(i * sizeof(wchar_t)); // 长度不定，如 “v中国”
            wcsncpy(currentWordPartLeft, currentWordTmp, i);

            PyObject *currentWordPartLeftTmp = PyUnicode_FromWideChar(currentWordPartLeft, i);
            ret = PySet_Contains(part, currentWordPartLeftTmp);

            if (ret == 1)
            {
                // 添加特征
                ret = getUnigramFeatureWideChar(
                    partCurrentLeftToken, 2, currentWordPartLeft, i, featureList);

                // 将临时变量赋给全局变量，为 bigram 特征做准备
                currentWordPartLeftGlobal = currentWordPartLeftTmp;
                current_left = i;

                // Py_DECREF(currentWordPartLeftTmp);
                currentWordPartLeftTmp = NULL;
                free(currentWordPartLeft);
                currentWordPartLeft = NULL;

                break;
            }
            else {
                Py_DECREF(currentWordPartLeftTmp);
                free(currentWordPartLeft);
                currentWordPartLeft = NULL;
            }
        }

        const wchar_t *partCurrentRightToken = L"cr";

        for (int i = currentWordTrimLength - 1; i > 0; i--)
        {
            // 右侧部分词特征
            wchar_t *currentWordPartRight = malloc(i * sizeof(wchar_t));

            wcsncpy(currentWordPartRight, currentWordTmp + currentWordLength - i, i);

            PyObject *currentWordPartRightTmp = PyUnicode_FromWideChar(currentWordPartRight, i);
            ret = PySet_Contains(part, currentWordPartRightTmp);
            // printf("ret right: %d\t%ls\n", ret, currentWordPartRight);
            if (ret == 1)
            {
                // 添加特征
                ret = getUnigramFeatureWideChar(
                    partCurrentRightToken, 2, currentWordPartRight, i, featureList);

                currentWordPartRightGlobal = currentWordPartRightTmp;
                current_right = i;

                // Py_DECREF(currentWordPartRightTmp);
                currentWordPartRightTmp = NULL;
                free(currentWordPartRight);
                currentWordPartRight = NULL;

                break;
            }
            else {
                Py_DECREF(currentWordPartRightTmp);
                free(currentWordPartRight);
                currentWordPartRight = NULL;
            }

        }

        PyMem_Free(currentWordTmp);
        currentWordTmp = NULL;

        if (current_left == 0 && current_right == 0)
        {
            ret = getUnknownFeature(L"wk", 2, featureList);

            const wchar_t *charCurrent1 = L"c1";
            const wchar_t *charCurrent2 = L"c2";
            const wchar_t *charCurrent3 = L"c3";
            const wchar_t *charCurrent4 = L"c4";

            tmpPyStr = PyUnicode_FromWideChar(L"ck", 2);
            if (currentWordLength == 1) {
                ret = PyList_Append(featureList, tmpPyStr);
                Py_DECREF(tmpPyStr);

                ret = PySet_Contains(chars, currentWord);
                if (ret == 1) {
                    ret = getUnigramFeaturePythonString(charCurrent1, 2, currentWord, 1, featureList);
                }
            }

            else if (currentWordLength == 2) {
                ret = PyList_Append(featureList, tmpPyStr);
                Py_DECREF(tmpPyStr);

                PyObject *charIndex1 = PyUnicode_Substring(currentWord, 0, 1);
                ret = PySet_Contains(chars, charIndex1);
                if (ret == 1) {
                    ret = getUnigramFeaturePythonString(charCurrent1, 2, charIndex1, 1, featureList);
                }
                Py_DECREF(charIndex1);

                PyObject *charIndex2 = PyUnicode_Substring(currentWord, 1, 2);
                ret = PySet_Contains(chars, charIndex2);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent2, 2, charIndex2, 1, featureList);
                }
                Py_DECREF(charIndex2);
            }

            else if (currentWordLength == 3)
            {
                ret = PyList_Append(featureList, tmpPyStr);
                Py_DECREF(tmpPyStr);

                PyObject *charIndex1 = PyUnicode_Substring(currentWord, 0, 1);
                ret = PySet_Contains(chars, charIndex1);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent1, 2, charIndex1, 1, featureList);
                }
                Py_DECREF(charIndex1);

                PyObject *charIndex2 = PyUnicode_Substring(currentWord, 1, 2);
                ret = PySet_Contains(chars, charIndex2);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent2, 2, charIndex2, 1, featureList);
                }
                Py_DECREF(charIndex2);

                PyObject *charIndex3 = PyUnicode_Substring(currentWord, 2, 3);
                ret = PySet_Contains(chars, charIndex3);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent3, 2, charIndex3, 1, featureList);
                }
                Py_DECREF(charIndex3);
            }

            else if (currentWordLength >= 4)
            {
                Py_DECREF(tmpPyStr);

                PyObject *charIndex1 = PyUnicode_Substring(currentWord, 0, 1);
                ret = PySet_Contains(chars, charIndex1);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent1, 2, charIndex1, 1, featureList);
                }
                Py_DECREF(charIndex1);

                PyObject *charIndex2 = PyUnicode_Substring(currentWord, 1, 2);
                ret = PySet_Contains(chars, charIndex2);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent2, 2, charIndex2, 1, featureList);
                }
                Py_DECREF(charIndex2);

                PyObject *charIndex3 = PyUnicode_Substring(currentWord, 2, 3);
                ret = PySet_Contains(chars, charIndex3);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent3, 2, charIndex3, 1, featureList);
                }
                Py_DECREF(charIndex3);

                PyObject *charIndex4 = PyUnicode_Substring(currentWord, 3, 4);
                ret = PySet_Contains(chars, charIndex4);
                if (ret == 1)
                {
                    ret = getUnigramFeaturePythonString(charCurrent4, 2, charIndex4, 1, featureList);
                }
                Py_DECREF(charIndex4);

                const wchar_t *charCurrent5 = L"c5";
                const wchar_t *charCurrent6 = L"c6";

                if (currentWordLength == 5) {
                    PyObject *charIndex6 = PyUnicode_Substring(
                        currentWord, currentWordLength-1, currentWordLength);
                    ret = PySet_Contains(chars, charIndex6);
                    if (ret == 1)
                    {
                        ret = getUnigramFeaturePythonString(charCurrent6, 2, charIndex6, 1, featureList);
                    }
                    Py_DECREF(charIndex6);
                }

                else if (currentWordLength > 5) {
                    PyObject *charIndex6 = PyUnicode_Substring(
                        currentWord, currentWordLength - 1, currentWordLength);
                    ret = PySet_Contains(chars, charIndex6);
                    if (ret == 1)
                    {
                        ret = getUnigramFeaturePythonString(charCurrent6, 2, charIndex6, 1, featureList);
                    }
                    Py_DECREF(charIndex6);

                    PyObject *charIndex5 = PyUnicode_Substring(
                        currentWord, currentWordLength - 2, currentWordLength - 1);
                    ret = PySet_Contains(chars, charIndex5);
                    if (ret == 1)
                    {
                        ret = getUnigramFeaturePythonString(charCurrent5, 2, charIndex5, 1, featureList);
                    }
                    Py_DECREF(charIndex5);
                }
            }
        }

        currentWord = NULL;
    }

    if (idx < wordListLength - 1)
    {
        // 获取后一词
        PyObject *nextWord = PyList_GetItem(wordList, idx + 1);
        ret = PySet_Contains(unigram, nextWord);

        if (ret == 1)
        {
            nextWordGlobal = nextWord;
            next_word = PyUnicode_GET_LENGTH(nextWordGlobal);
            ret = getUnigramFeaturePythonString(L"x", 1, nextWord, next_word, featureList);

            nextWord = NULL;
        }
        else
        {
            const wchar_t *partNextLeftToken = L"dl";

            Py_ssize_t nextWordLength = PyUnicode_GET_LENGTH(nextWord);
            Py_ssize_t nextWordTrimLength = min(nextWordLength, maxPartLength);

            // 转换为 wchar_t*
            wchar_t *nextWordTmp = PyUnicode_AsWideCharString(nextWord, &nextWordLength);

            for (int i = nextWordTrimLength - 1; i > 0; i--)
            {
                // 左侧部分词特征
                wchar_t *nextWordPartLeft = malloc(i * sizeof(wchar_t)); // 长度不定，如 “v中国”
                wcsncpy(nextWordPartLeft, nextWordTmp, i);

                PyObject *nextWordPartLeftTmp = PyUnicode_FromWideChar(nextWordPartLeft, i);
                // printf("cur left %ls\n", nextWordPartLeft);
                ret = PySet_Contains(part, nextWordPartLeftTmp);

                if (ret == 1)
                {
                    // 添加特征
                    ret = getUnigramFeatureWideChar(
                        partNextLeftToken, 2, nextWordPartLeft, i, featureList);

                    // 将临时变量赋给全局变量，为bigram 特征做准备
                    nextWordPartLeftGlobal = nextWordPartLeftTmp;
                    next_left = i;

                    // Py_DECREF(nextWordPartLeftTmp);
                    nextWordPartLeftTmp = NULL;
                    free(nextWordPartLeft);
                    nextWordPartLeft = NULL;

                    break;
                }
                else {
                    Py_DECREF(nextWordPartLeftTmp);
                    free(nextWordPartLeft);
                    nextWordPartLeft = NULL;
                }
            }

            const wchar_t *partNextRightToken = L"dr";

            for (int i = nextWordTrimLength - 1; i > 0; i--)
            {
                // 右侧部分词特征
                wchar_t *nextWordPartRight = malloc(i * sizeof(wchar_t));

                wcsncpy(nextWordPartRight, nextWordTmp + nextWordLength - i, i);
                // printf("\tdr i = %d  %ls\n", i, nextWordTmp + nextWordLength - i);
                PyObject *nextWordPartRightTmp = PyUnicode_FromWideChar(nextWordPartRight, i);
                ret = PySet_Contains(part, nextWordPartRightTmp);
                // printf("ret right: %d\t%ls\n", ret, nextWordPartRight);
                if (ret == 1)
                {
                    // 添加特征
                    ret = getUnigramFeatureWideChar(
                        partNextRightToken, 2, nextWordPartRight, i, featureList);

                    nextWordPartRightGlobal = nextWordPartRightTmp;
                    next_right = i;

                    // Py_DECREF(nextWordPartRightTmp);
                    nextWordPartRightTmp = NULL;
                    free(nextWordPartRight);
                    nextWordPartRight = NULL;

                    break;
                }
                else {
                    Py_DECREF(nextWordPartRightTmp);
                    free(nextWordPartRight);
                    nextWordPartRight = NULL;
                }
            }

            PyMem_Free(nextWordTmp);
            nextWordTmp = NULL;

            if (next_left == 0 && next_right == 0)
            {
                ret = getUnknownFeature(L"xk", 2, featureList);
            }
        }
    }
    else
    {
        // 添加结束符特征
        ret = getUnknownFeature(L"[END]", 5, featureList);
    }

    const wchar_t *mark = L"*";
    // printf("%d, %d, %d        %d, %d, %d        %d, %d, %d\n",
    //        before_word, before_left, before_right,
    //        current_word, current_left, current_right,
    //        next_word, next_left, next_right);
    // get bigram feature
    if (current_word > 0) {
        if (before_word > 0) {
            ret = getBigramFeature(
                L"vw", 2, mark, beforeWordGlobal, currentWordGlobal,
                before_word, current_word, featureList);
        }
        else {
            if (before_left > 0) {
                ret = getBigramFeature(
                    L"blw", 3, mark, beforeWordPartLeftGlobal, currentWordGlobal,
                    before_left, current_word, featureList);
            }

            if (before_right > 0)
            {
                ret = getBigramFeature(
                    L"brw", 3, mark, beforeWordPartRightGlobal, currentWordGlobal,
                    before_right, current_word, featureList);
            }
        }

        if (next_word > 0)
        {
            ret = getBigramFeature(
                L"wx", 2, mark, currentWordGlobal, nextWordGlobal,
                current_word, next_word, featureList);
        }
        else
        {
            if (next_left > 0)
            {
                ret = getBigramFeature(
                    L"wdl", 3, mark, currentWordGlobal, nextWordPartLeftGlobal,
                    current_word, next_left, featureList);
            }

            if (next_right > 0)
            {
                ret = getBigramFeature(
                    L"wdr", 3, mark, currentWordGlobal, nextWordPartRightGlobal,
                    current_word, next_right, featureList);
            }
        }
    }
    else
    {
        if (before_word > 0)
        {
            if (current_left > 0) {
                ret = getBigramFeature(
                    L"vcl", 3, mark, beforeWordGlobal, currentWordPartLeftGlobal,
                    before_word, current_left, featureList);
            }

            if (current_right > 0) {
                ret = getBigramFeature(
                    L"vcr", 3, mark, beforeWordGlobal, currentWordPartRightGlobal,
                    before_word, current_right, featureList);
            }
        }
        else {
            if (before_left > 0) {
                if (current_left > 0) {
                    ret = getBigramFeature(
                        L"blcl", 4, mark, beforeWordPartLeftGlobal, currentWordPartLeftGlobal,
                        before_left, current_left, featureList);
                }

                if (current_right > 0) {
                    ret = getBigramFeature(
                        L"blcr", 4, mark, beforeWordPartLeftGlobal, currentWordPartRightGlobal,
                        before_left, current_right, featureList);
                }
            }

            if (before_right > 0)
            {
                if (current_left > 0)
                {
                    ret = getBigramFeature(
                        L"brcl", 4, mark, beforeWordPartRightGlobal, currentWordPartLeftGlobal,
                        before_right, current_left, featureList);
                }

                if (current_right > 0)
                {
                    ret = getBigramFeature(
                        L"brcr", 4, mark, beforeWordPartRightGlobal, currentWordPartRightGlobal,
                        before_right, current_right, featureList);
                }
            }
        }

        if (next_word > 0) {
            if (current_left > 0) {
                ret = getBigramFeature(
                    L"clx", 3, mark, currentWordPartLeftGlobal, nextWordGlobal,
                    current_left, next_word, featureList);
            }

            if (current_right > 0)
            {
                ret = getBigramFeature(
                    L"crx", 3, mark, currentWordPartRightGlobal, nextWordGlobal,
                    current_right, next_word, featureList);
            }
        }
        else {
            if (next_left > 0) {
                if (current_left > 0) {
                    ret = getBigramFeature(
                        L"cldl", 4, mark, currentWordPartLeftGlobal, nextWordPartLeftGlobal,
                        current_left, next_left, featureList);
                }

                if (current_right > 0)
                {
                    ret = getBigramFeature(
                        L"crdl", 4, mark, currentWordPartRightGlobal, nextWordPartLeftGlobal,
                        current_right, next_left, featureList);
                }
            }

            if (next_right > 0) {
                if (current_left > 0) {
                    ret = getBigramFeature(
                        L"cldr", 4, mark, currentWordPartLeftGlobal, nextWordPartRightGlobal,
                        current_left, next_right, featureList);
                }

                if (current_right > 0)
                {
                    ret = getBigramFeature(
                        L"crdr", 4, mark, currentWordPartRightGlobal, nextWordPartRightGlobal,
                        current_right, next_right, featureList);
                }
            }
        }
    }

    if (current_word > 0) {
        currentWordGlobal = NULL;
    }
    if (current_left > 0) {
        Py_DECREF(currentWordPartLeftGlobal);
        currentWordPartLeftGlobal = NULL;
    }
    if (current_right > 0) {
        Py_DECREF(currentWordPartRightGlobal);
        currentWordPartRightGlobal = NULL;
    }
    if (before_word > 0)
    {
        beforeWordGlobal = NULL;
    }
    if (before_left > 0)
    {
        Py_DECREF(beforeWordPartLeftGlobal);
        beforeWordPartLeftGlobal = NULL;
    }
    if (before_right > 0)
    {
        Py_DECREF(beforeWordPartRightGlobal);
        beforeWordPartRightGlobal = NULL;
    }
    if (next_word > 0)
    {
        nextWordGlobal = NULL;
    }
    if (next_left > 0)
    {
        Py_DECREF(nextWordPartLeftGlobal);
        nextWordPartLeftGlobal = NULL;
    }
    if (next_right > 0)
    {
        Py_DECREF(nextWordPartRightGlobal);
        nextWordPartRightGlobal = NULL;
    }

    return featureList;
}

int main() {
    Py_Initialize();
    PyObject *word_list = PyList_New(0);

    PyObject *tmpPyStr;

    tmpPyStr = PyUnicode_FromWideChar(L"今天", 2);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"圣诞节", 3);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"中华人民共和国", 7);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"的", 1);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"天气", 2);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"真的", 2);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"挺好", 2);
    PyList_Append(word_list, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"。", 1);
    PyList_Append(word_list, tmpPyStr);
    printf("length %ld\n", PyList_Size(word_list));
    // Py_DECREF(tmpPyStr);

    PyObject *unigram = PySet_New(0);
    tmpPyStr = PyUnicode_FromWideChar(L"天气", 2);
    PySet_Add(unigram, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"今天", 2);
    PySet_Add(unigram, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"中国", 2);
    PySet_Add(unigram, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"美国", 2);
    PySet_Add(unigram, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"总统", 2);
    PySet_Add(unigram, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"总统府", 3);
    PySet_Add(unigram, tmpPyStr);
    printf("length %ld\n", PySet_Size(unigram));

    // unigram = set([ "天气", "今天", "中国", "美国", "总统", "总统府" ]);
    // char = set("abcdefghijklmnopqrstuvwxyz0123456789.:-_");
    PyObject *chars = PySet_New(0);
    const wchar_t *chars_list = L"abcdefghijklmnopqrstuvwxyz0123456789.:-_";
    for (int i = 0; i < 40; i++) {
        printf("i: %d\n", i);
        tmpPyStr = PyUnicode_FromWideChar(chars_list + i, 1);
        PySet_Add(chars, tmpPyStr);
    }
    printf("length %ld\n", PySet_Size(chars));

    PyObject *part = PySet_New(0);
    tmpPyStr = PyUnicode_FromWideChar(L"节", 1);
    PySet_Add(part, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"共和国", 3);
    PySet_Add(part, tmpPyStr);
    tmpPyStr = PyUnicode_FromWideChar(L"府", 1);
    PySet_Add(part, tmpPyStr);
    Py_DECREF(tmpPyStr);

    // start test:
    PyObject *res;
    int index = -1;
    for (int i = 0; i < 1000; i++)
    {
        index = i % 8;
        res = getPosNodeFeature(index, word_list, part, unigram, chars);
    }

    Py_Finalize();
}
