#include "tagWordsConverter.h"

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

void PyAppend(int wordLength, int start, PyObject *wordList, const wchar_t *charList)
{
    PyObject *tmpPyStr = PyUnicode_FromWideChar(charList + start, wordLength);
    int ret = PyList_Append(wordList, tmpPyStr);
    Py_DECREF(tmpPyStr);
    // if (ret == -1)
    //     printf("Failed to append string to list.");
}

/**
 * @brief 从 tag 转为 words
 *
 * @param charList: 字符串 python unicode 类型
 * @param tags: 标签 python 列表，其中内容为 0，1 整数值
 * @param nodeNum: 字符总数
 * @return PyObject*: 词汇列表
 */
API PyObject *tagWordsConverter(const wchar_t *charList, char *tags, int nodeNum)
{
    PyObject *wordList = PyList_New(0);

    int ret;
    int wordLength;
    int start = -1;
    // printf("nodeNum: %d\n", nodeNum);
    // printf("size of wchar_t: %ld\n", sizeof(wchar_t));

    for (int i = 0; i < nodeNum; i++)
    {
        // printf("%d\t%ls\t%d\t%d\n", i, charList + i, *(tags + i), tags[i]);
        if (tags[i] == 0)
        {
            if (i == 0)
            {
                start = i;
                if (i == nodeNum - 1) // 即文本中仅一个字
                {
                    PyAppend(1, 0, wordList, charList);
                    break;
                };
                continue;
            }
            else if (i != nodeNum - 1)
            {
                if (start == -1)
                    continue;

                wordLength = i - start;
                PyAppend(wordLength, start, wordList, charList);
                start = i;
            }
            else
            {
                wordLength = i - start;
                PyAppend(wordLength, start, wordList, charList);
                PyAppend(1, i, wordList, charList);
            }
        }
        else //if (tags[i] == 1)
        {
            if (i == 0)
            {
                start = i;
                continue;
            }
            else if (i != nodeNum - 1)
            {
                continue;
            }
            else
            {
                wordLength = i - start + 1;
                PyAppend(wordLength, start, wordList, charList);
            }
        }
    }

    return wordList;
}

int main()
{
    const wchar_t *charList = L"你知道吗？冰雪运动的发源地，原来在我国阿勒泰地区";
    char tags[] = {0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1};
    int nodeNums = 24;

    Py_Initialize();
    PyObject *res = tagWordsConverter(charList, tags, nodeNums);
    // printf("the pyobject: %ls\n", res);
    // Py_DECREF(res);
    Py_Finalize();
}
