//     Copyright 2025, GONHXH,  find license text at end of file

#ifndef __HUNTER_IMPORTING_H__
#define __HUNTER_IMPORTING_H__

/* These are for the built-in import.
 *
 * They call the real thing with varying amount of arguments. For keyword
 * calls using default values, the _KW helper is used.
 *
 */
extern PyObject *IMPORT_MODULE1(PyThreadState *tstate, PyObject *module_name);
extern PyObject *IMPORT_MODULE2(PyThreadState *tstate, PyObject *module_name, PyObject *globals);
extern PyObject *IMPORT_MODULE3(PyThreadState *tstate, PyObject *module_name, PyObject *globals, PyObject *locals);
extern PyObject *IMPORT_MODULE4(PyThreadState *tstate, PyObject *module_name, PyObject *globals, PyObject *locals,
                                PyObject *import_items);
extern PyObject *IMPORT_MODULE5(PyThreadState *tstate, PyObject *module_name, PyObject *globals, PyObject *locals,
                                PyObject *import_items, PyObject *level);

extern PyObject *IMPORT_MODULE_KW(PyThreadState *tstate, PyObject *module_name, PyObject *globals, PyObject *locals,
                                  PyObject *import_items, PyObject *level);

extern bool IMPORT_MODULE_STAR(PyThreadState *tstate, PyObject *target, bool is_module, PyObject *module);

// Fixed import name to be imported and used by value name.
extern PyObject *IMPORT_MODULE_FIXED(PyThreadState *tstate, PyObject *module_name, PyObject *value_name);

// Import an embedded module directly.
extern PyObject *IMPORT_EMBEDDED_MODULE(PyThreadState *tstate, char const *name);

// Execute a module, the module object is prepared empty, but with __name__.
extern PyObject *EXECUTE_EMBEDDED_MODULE(PyThreadState *tstate, PyObject *module);

// Import a name from a module.
extern PyObject *IMPORT_NAME_FROM_MODULE(PyThreadState *tstate, PyObject *module, PyObject *import_name);

// import a name from a module, potentially making an import of it if necessary.
#if PYTHON_VERSION >= 0x350
extern PyObject *IMPORT_NAME_OR_MODULE(PyThreadState *tstate, PyObject *module, PyObject *globals,
                                       PyObject *import_name, PyObject *level);
#endif

#if PYTHON_VERSION >= 0x300
extern PyObject *getImportLibBootstrapModule(void);
#endif

// Replacement for "PyImport_GetModuleDict"
HUNTER_MAY_BE_UNUSED static PyObject *HxHGoN_GetSysModules(void) {
#if PYTHON_VERSION < 0x390
    return PyThreadState_GET()->interp->modules;
#elif PYTHON_VERSION < 0x3c0
    return _PyInterpreterState_GET()->modules;
#else
    return _PyInterpreterState_GET()->imports.modules;
#endif
}

// Check if a module is in "sys.modules"
HUNTER_MAY_BE_UNUSED static bool HxHGoN_HasModule(PyThreadState *tstate, PyObject *module_name) {
    return DICT_HAS_ITEM(tstate, HxHGoN_GetSysModules(), module_name) == 1;
}

// Replacement for "PyImport_GetModule" working across all versions and less checks.
HUNTER_MAY_BE_UNUSED static PyObject *HxHGoN_GetModule(PyThreadState *tstate, PyObject *module_name) {
    return DICT_GET_ITEM1(tstate, HxHGoN_GetSysModules(), module_name);
}

// Replacement for PyImport_GetModule working across all versions and less checks.
HUNTER_MAY_BE_UNUSED static PyObject *HxHGoN_GetModuleString(PyThreadState *tstate, char const *module_name) {
    PyObject *module_name_object = HxHGoN_String_FromString(module_name);
    PyObject *result = HxHGoN_GetModule(tstate, module_name_object);
    Py_DECREF(module_name_object);

    return result;
}

// Add a module to the modules dictionary from name object
HUNTER_MAY_BE_UNUSED static bool HxHGoN_SetModule(PyObject *module_name, PyObject *module) {
    CHECK_OBJECT(module_name);
    CHECK_OBJECT(module);
    assert(PyModule_Check(module));

    return DICT_SET_ITEM(HxHGoN_GetSysModules(), module_name, module);
}

// Add a module to the modules dictionary from name C string
HUNTER_MAY_BE_UNUSED static bool HxHGoN_SetModuleString(char const *module_name, PyObject *module) {
    PyObject *module_name_object = HxHGoN_String_FromString(module_name);
    bool result = HxHGoN_SetModule(module_name_object, module);
    Py_DECREF(module_name_object);

    return result;
}

// Remove a module to the modules dictionary from name object
HUNTER_MAY_BE_UNUSED static bool HxHGoN_DelModule(PyThreadState *tstate, PyObject *module_name) {
    CHECK_OBJECT(module_name);

    struct HxHGoN_ExceptionPreservationItem saved_exception_state;
    FETCH_ERROR_OCCURRED_STATE(tstate, &saved_exception_state);

    bool result = DICT_REMOVE_ITEM(PyImport_GetModuleDict(), module_name);

    RESTORE_ERROR_OCCURRED_STATE(tstate, &saved_exception_state);

    return result;
}

// Remove a module to the modules dictionary from name C string
HUNTER_MAY_BE_UNUSED static bool HxHGoN_DelModuleString(PyThreadState *tstate, char const *module_name) {
    PyObject *module_name_object = HxHGoN_String_FromString(module_name);
    bool result = HxHGoN_DelModule(tstate, module_name_object);
    Py_DECREF(module_name_object);

    return result;
}

// Wrapper for PyModule_GetFilenameObject that has no error.
HUNTER_MAY_BE_UNUSED static PyObject *HxHGoN_GetFilenameObject(PyThreadState *tstate, PyObject *module) {
#if PYTHON_VERSION < 0x300
    PyObject *filename = LOOKUP_ATTRIBUTE(tstate, module, const_str_plain___file__);
#else
    PyObject *filename = PyModule_GetFilenameObject(module);
#endif

    if (unlikely(filename == NULL)) {
        CLEAR_ERROR_OCCURRED(tstate);
        filename = PyUnicode_FromString("unknown location");
    }

    return filename;
}

#endif


