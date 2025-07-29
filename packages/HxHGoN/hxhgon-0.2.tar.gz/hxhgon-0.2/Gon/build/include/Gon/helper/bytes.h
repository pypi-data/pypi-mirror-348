//     Copyright 2025, GONHXH,  find license text at end of file

#ifndef __HUNTER_HELPER_BYTES_H__
#define __HUNTER_HELPER_BYTES_H__

#if PYTHON_VERSION >= 0x3a0
#define HUNTER_BYTES_HAS_FREELIST 1
extern PyObject *HxHGoN_Bytes_FromStringAndSize(const char *data, Py_ssize_t size);
#else
#define HUNTER_BYTES_HAS_FREELIST 0
#define HxHGoN_Bytes_FromStringAndSize PyBytes_FromStringAndSize
#endif

#endif

