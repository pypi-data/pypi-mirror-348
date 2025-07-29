//     Copyright 2025, GONHXH,  find license text at end of file

// This implements the resource reader for of C compiled modules and
// shared library extension modules bundled for standalone mode with
// newer Python.

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "Gon/prelude.h"
#include "Gon/unfreezing.h"
#endif

// Just for the IDE to know, this file is not included otherwise.
#if PYTHON_VERSION >= 0x370

struct HxHGoN_ResourceReaderObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* The loader entry, to know this is about exactly. */
        struct HxHGoN_MetaPathBasedLoaderEntry const *m_loader_entry;
};

static void HxHGoN_ResourceReader_tp_dealloc(struct HxHGoN_ResourceReaderObject *reader) {
    HxHGoN_GC_UnTrack(reader);

    PyObject_GC_Del(reader);
}

static PyObject *HxHGoN_ResourceReader_tp_repr(struct HxHGoN_ResourceReaderObject *reader) {
    return PyUnicode_FromFormat("<Gon_resource_reader for '%s'>", reader->m_loader_entry->name);
}

// Obligatory, even if we have nothing to own
static int HxHGoN_ResourceReader_tp_traverse(struct HxHGoN_ResourceReaderObject *reader, visitproc visit, void *arg) {
    return 0;
}

static PyObject *_HxHGoN_ResourceReader_resource_path(PyThreadState *tstate, struct HxHGoN_ResourceReaderObject *reader,
                                                      PyObject *resource) {
    PyObject *dir_name = getModuleDirectory(tstate, reader->m_loader_entry);

    if (unlikely(dir_name == NULL)) {
        return NULL;
    }

    PyObject *result = JOIN_PATH2(dir_name, resource);
    Py_DECREF(dir_name);

    return result;
}

static PyObject *HxHGoN_ResourceReader_resource_path(struct HxHGoN_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:resource_path", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    return _HxHGoN_ResourceReader_resource_path(tstate, reader, resource);
}

static PyObject *HxHGoN_ResourceReader_open_resource(struct HxHGoN_ResourceReaderObject *reader, PyObject *args,
                                                     PyObject *kwds) {
    PyObject *resource;

    int res = PyArg_ParseTupleAndKeywords(args, kwds, "O:open_resource", (char **)_kw_list_get_data, &resource);

    if (unlikely(res == 0)) {
        return NULL;
    }

    PyThreadState *tstate = PyThreadState_GET();

    PyObject *filename = _HxHGoN_ResourceReader_resource_path(tstate, reader, resource);

    return BUILTIN_OPEN_BINARY_READ_SIMPLE(tstate, filename);
}

#include "MetaPathBasedLoaderResourceReaderFiles.c"

static PyObject *HxHGoN_ResourceReader_files(struct HxHGoN_ResourceReaderObject *reader, PyObject *args,
                                             PyObject *kwds) {

    PyThreadState *tstate = PyThreadState_GET();
    return HxHGoN_ResourceReaderFiles_New(tstate, reader->m_loader_entry, const_str_empty);
}

static PyMethodDef HxHGoN_ResourceReader_methods[] = {
    {"resource_path", (PyCFunction)HxHGoN_ResourceReader_resource_path, METH_VARARGS | METH_KEYWORDS, NULL},
    {"open_resource", (PyCFunction)HxHGoN_ResourceReader_open_resource, METH_VARARGS | METH_KEYWORDS, NULL},
    {"files", (PyCFunction)HxHGoN_ResourceReader_files, METH_NOARGS, NULL},
    {NULL}};

static PyTypeObject HxHGoN_ResourceReader_Type = {
    PyVarObject_HEAD_INIT(NULL, 0) "Gon_resource_reader",
    sizeof(struct HxHGoN_ResourceReaderObject),      // tp_basicsize
    0,                                               // tp_itemsize
    (destructor)HxHGoN_ResourceReader_tp_dealloc,    // tp_dealloc
    0,                                               // tp_print
    0,                                               // tp_getattr
    0,                                               // tp_setattr
    0,                                               // tp_reserved
    (reprfunc)HxHGoN_ResourceReader_tp_repr,         // tp_repr
    0,                                               // tp_as_number
    0,                                               // tp_as_sequence
    0,                                               // tp_as_mapping
    0,                                               // tp_hash
    0,                                               // tp_call
    0,                                               // tp_str
    0,                                               // tp_getattro (PyObject_GenericGetAttr)
    0,                                               // tp_setattro
    0,                                               // tp_as_buffer
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_HAVE_GC,         // tp_flags
    0,                                               // tp_doc
    (traverseproc)HxHGoN_ResourceReader_tp_traverse, // tp_traverse
    0,                                               // tp_clear
    0,                                               // tp_richcompare
    0,                                               // tp_weaklistoffset
    0,                                               // tp_iter
    0,                                               // tp_iternext
    HxHGoN_ResourceReader_methods,                   // tp_methods
    0,                                               // tp_members
    0,                                               // tp_getset
};

static PyObject *HxHGoN_ResourceReader_New(struct HxHGoN_MetaPathBasedLoaderEntry const *entry) {
    struct HxHGoN_ResourceReaderObject *result;

    result = (struct HxHGoN_ResourceReaderObject *)HxHGoN_GC_New(&HxHGoN_ResourceReader_Type);
    HxHGoN_GC_Track(result);

    result->m_loader_entry = entry;

    return (PyObject *)result;
}

#endif

