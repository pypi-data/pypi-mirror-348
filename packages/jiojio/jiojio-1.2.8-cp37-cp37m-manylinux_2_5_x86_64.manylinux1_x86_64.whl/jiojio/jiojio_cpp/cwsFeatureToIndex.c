#include "cwsFeatureToIndex.h"

#ifdef _WIN32
#define API __declspec(dllexport)
#else
#define API
#endif

/**
 * @brief 从特征映射至索引号
 *
 * @param nodeFeature: 特征 python 列表
 * @param featureToIndex: 特征索引号
 * @return PyObject*: 索引列表
 */
PyObject *getFeatureIndex(PyObject *nodeFeature, PyObject *featureToIndex)
{
    int ret;
    int flag = 0;

    PyObject *indexList = PyList_New(0);
    Py_ssize_t nodeFeatureLength = PyList_GET_SIZE(nodeFeature);

    for (int i = 0; i < nodeFeatureLength; i++)
    {
        PyObject *curFeature = PyList_GetItem(nodeFeature, i);
        ret = PyDict_Contains(featureToIndex, curFeature);
        if (ret == 1)
        {
            // Py_ssize_t curLength = PyUnicode_GET_LENGTH(curFeature);
            // wchar_t *tmpString = malloc(sizeof(wchar_t) * curLength);
            // Py_ssize_t length = PyUnicode_AsWideChar(curFeature, tmpString, curLength);
            // printf("\t%d\t%ls\n", i, tmpString);
            // free(tmpString);
            // tmpString = NULL;

            PyObject *index = PyDict_GetItemWithError(featureToIndex, curFeature);
            ret = PyList_Append(indexList, index);
            // Py_DECREF(index);
        }
        else
        {
            flag = 1;
        }
        // Py_DECREF(curFeature);
    }

    if (flag == 1)
    {
        PyObject *zero = PyLong_FromLong(0);
        ret = PyList_Append(indexList, zero);
        Py_DECREF(zero);
    }

    return indexList;
}
