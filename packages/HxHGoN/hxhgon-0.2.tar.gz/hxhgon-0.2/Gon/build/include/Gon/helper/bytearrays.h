//     Copyright 2025, GONHXH,  find license text at end of file

#ifndef __HUNTER_HELPER_BYTEARRAYS_H__
#define __HUNTER_HELPER_BYTEARRAYS_H__

HUNTER_MAY_BE_UNUSED static PyObject *BYTEARRAY_COPY(PyThreadState *tstate, PyObject *bytearray) {
    CHECK_OBJECT(bytearray);
    assert(PyByteArray_CheckExact(bytearray));

    PyObject *result = PyByteArray_FromObject(bytearray);

    if (unlikely(result == NULL)) {
        return NULL;
    }

    return result;
}

#endif


