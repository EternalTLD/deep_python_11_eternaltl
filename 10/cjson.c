#include <Python.h>
#include <stdbool.h>

PyObject* loads(PyObject* self, PyObject* args) {
    PyObject* dict = PyDict_New();
    char *json_string;

    if (!PyArg_ParseTuple(args, "s", &json_string)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument. Expected string.");
        return NULL;
    }

    size_t len = strlen(json_string);
    size_t i = 0;

    while (i < len - 1) {
        while (i < len && json_string[i] != '\"') {
            i++;
            if (json_string[i] == '}') {
                return dict;
            }
        }

        i++;

        char key[256];
        size_t key_index = 0;

        while (i < len && json_string[i] != '\"') {
            key[key_index++] = json_string[i++];
        }
        key[key_index] = '\0';

        i += 2;

        while (i < len && (json_string[i] == ' ' || json_string[i] == '\t' || json_string[i] == '\n' || json_string[i] == '\r')) {
            i++;
        }

        PyObject* value;
        if (json_string[i] == '\"') {
            i++;
            char val[256];
            size_t val_index = 0;

            while (i < len && json_string[i] != '\"') {
                val[val_index++] = json_string[i++];
            }
            val[val_index] = '\0';

            if (!(value = Py_BuildValue("s", val))) {
                PyErr_SetString(PyExc_SystemError, "Failed to build string value.");
                return NULL;
            }
            i++;

        } else {
            char *endptr;
            int num = strtod(json_string + i, &endptr);

            i = endptr - json_string;

            if (!(value = Py_BuildValue("i", num))) {
                PyErr_SetString(PyExc_SystemError, "Failed to build integer value.");
                return NULL;
            }
        }

        while (i < len && (json_string[i] == ' ' || json_string[i] == '\t' || json_string[i] == '\n' || json_string[i] == '\r')) {
            i++;
        }

        if (PyDict_SetItemString(dict, key, value) < 0) {
            PyErr_SetString(PyExc_SystemError, "Failed to set item.");
            printf("ERROR: Failed to set item\n");
            return NULL;
        }
        Py_DECREF(value);
    }

    return dict;
}

static PyObject* dumps_dict(PyObject* dict) {
    PyObject *key, *value;
    Py_ssize_t pos = 0;

    PyObject *result_list = PyList_New(0);

    PyList_Append(result_list, PyUnicode_DecodeASCII("{", 1, NULL));

    while (PyDict_Next(dict, &pos, &key, &value)) {
        PyObject *key_str = PyObject_Str(key);
        PyObject *value_str;

        if (PyFloat_Check(value) || PyLong_Check(value) || PyBool_Check(value)) {
            value_str = PyObject_Str(value);
        } else {
            value_str = PyUnicode_FromFormat("\"%S\"", PyObject_Str(value));
        }

        PyObject *pair_str = PyUnicode_FromFormat("\"%S\": %S", key_str, value_str);

        PyList_Append(result_list, pair_str);

        Py_XDECREF(key_str);
        Py_XDECREF(value_str);
        Py_XDECREF(pair_str);
    }

    if (PyList_Size(result_list) > 1) {
        PyObject *result_str = PyUnicode_Join(PyUnicode_DecodeASCII(", ", 2, NULL), result_list);

        Py_DECREF(result_list);

        PyUnicode_Append(&result_str, PyUnicode_DecodeASCII("}", 1, NULL));

        return result_str;
    }

    Py_DECREF(result_list);

    return PyUnicode_DecodeASCII("{}", 2, NULL);
}

static PyObject* dumps(PyObject* self, PyObject* args) {
    PyObject* jsonDict;

    if (!PyArg_ParseTuple(args, "O", &jsonDict)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument.");
        return NULL;
    }

    if (!PyDict_Check(jsonDict)) {
        PyErr_SetString(PyExc_TypeError, "Invalid argument. Expected dictionary.");
        return NULL;
    }

    PyObject *result_str = dumps_dict(jsonDict);

    return result_str;
}


static PyMethodDef cjson_methods[] = {
    {"loads", loads, METH_VARARGS, "Load JSON from string into dict"},
    {"dumps", dumps, METH_VARARGS, "Dump dict to JSON string"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef cjson_module = {
    PyModuleDef_HEAD_INIT,
    "cjson",
    NULL,
    -1,
    cjson_methods
};

PyMODINIT_FUNC PyInit_cjson(void) {
    return PyModule_Create(&cjson_module);
}