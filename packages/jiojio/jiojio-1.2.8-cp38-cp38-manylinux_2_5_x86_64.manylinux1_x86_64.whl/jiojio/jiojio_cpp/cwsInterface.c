#include "cwsInterface.h"

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

void *init(int unigramSetHashTableMaxSize,
           PyObject *unigramPyList,
           int bigramSetHashTableMaxSize,
           PyObject *bigramPyList,
           int featureToIdxDictHashTableMaxSize,
           PyObject *featureToIdxPyList,
           PyObject *pyModelWeightList,
           int printing)
{

    CwsPrediction *cwsPredictionObj = newCwsPrediction();
    if (cwsPredictionObj == NULL)
    {
        return 0;
    }

    int ret = Init(cwsPredictionObj,
                   unigramSetHashTableMaxSize,
                   unigramPyList,
                   bigramSetHashTableMaxSize,
                   bigramPyList,
                   featureToIdxDictHashTableMaxSize,
                   featureToIdxPyList,
                   pyModelWeightList,
                   printing);

    return cwsPredictionObj;
}

PyObject *cut(void *voidObj, const wchar_t *text) {

    CwsPrediction *cwsPredictionObj = (CwsPrediction *)voidObj;
    PyObject *featureIdx = Cut(cwsPredictionObj, text);

    return featureIdx;
}

int main()
{

    Py_Initialize();
    // unsigned int res = set_hash_table_hash_str(L"一下子");
    PyObject *tmpList = PyList_New(0);
    PyObject *tmp;
    int ret;
    tmp = PyUnicode_FromWideChar(L"一个", -1);
    ret = PyList_Append(tmpList, tmp);
    tmp = PyUnicode_FromWideChar(L"美好", -1);
    ret = PyList_Append(tmpList, tmp);
    tmp = PyUnicode_FromWideChar(L"真实", -1);
    ret = PyList_Append(tmpList, tmp);
    tmp = PyUnicode_FromWideChar(L"qqqqq", -1);
    ret = PyList_Append(tmpList, tmp);

    Py_ssize_t length = PyList_Size(tmpList);
    for (int i = 0; i < length; i++)
    {
        PyObject *curWord = PyList_GetItem(tmpList, i);
        wchar_t buff[30];
        Py_ssize_t ret = PyUnicode_AsWideChar(curWord, buff, 20);
        printf("cur word: %ls\n", buff);
    }

    unsigned int pos = dict_hash_table_hash_str(L"[END]") % 200000;
    // CwsPrediction *cwsPredictionObj = init(3, tmpList, 6, tmpList, 10, tmpList);

    // Init(cwsPredictionObj, 10000,
    //      "/home/cuichengyu/github/jiojio/jiojio/models/default_cws_model/unigram.txt",
    //      20000,
    //      "/home/cuichengyu/github/jiojio/jiojio/models/default_cws_model/bigram.txt",
    //      1000000,
    //      "/home/cuichengyu/github/jiojio/jiojio/models/default_cws_model/feature_to_idx.txt");

    const wchar_t *text = L"中国人真的很勤奋。";
    int textLength = wcslen(text);
    // PyObject *featureList = cut(cwsPredictionObj, text);

    Py_Finalize();
    return 0;
}
