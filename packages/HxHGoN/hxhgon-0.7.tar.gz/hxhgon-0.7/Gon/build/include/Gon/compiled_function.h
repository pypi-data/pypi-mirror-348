//     Copyright 2025, GONHXH, @T_T_Z_T find license text at end of file

#ifndef __HUNTER_COMPILED_FUNCTION_H__
#define __HUNTER_COMPILED_FUNCTION_H__

#ifdef __IDE_ONLY__
#include "Gon/prelude.h"
#endif

// Compiled function type.

// The backbone of the integration into CPython. Try to behave as well as normal
// functions and built-in functions, or even better.

struct HxHGoN_FunctionObject;

// The actual function code with arguments as an array.
typedef PyObject *(*function_impl_code)(PyThreadState *tstate, struct HxHGoN_FunctionObject const *, PyObject **);

// The HxHGoN_FunctionObject is the storage associated with a compiled function
// instance of which there can be many for each code.
struct HxHGoN_FunctionObject {
    /* Python object folklore: */
    PyObject_VAR_HEAD

        PyObject *m_name;

    PyObject *m_module;
    PyObject *m_doc;

    PyCodeObject *m_code_object;
    Py_ssize_t m_args_overall_count;
    Py_ssize_t m_args_positional_count;
    Py_ssize_t m_args_keywords_count;
    bool m_args_simple;
    Py_ssize_t m_args_star_list_index;
    Py_ssize_t m_args_star_dict_index;

#if PYTHON_VERSION >= 0x380
    Py_ssize_t m_args_pos_only_count;
#endif

    // Same as code_object->co_varnames
    PyObject **m_varnames;

    // C implementation of the function
    function_impl_code m_c_code;

#if PYTHON_VERSION >= 0x380
    vectorcallfunc m_vectorcall;
#endif

    PyObject *m_dict;
    PyObject *m_weakrefs;

    // Tuple of defaults, for use in __defaults__ and parameter parsing.
    PyObject *m_defaults;
    Py_ssize_t m_defaults_given;

#if PYTHON_VERSION >= 0x300
    // List of keyword only defaults, for use in __kwdefaults__ and parameter
    // parsing.
    PyObject *m_kwdefaults;

    // Annotations to the function arguments and return value.
    PyObject *m_annotations;
#endif

#if PYTHON_VERSION >= 0x300
    PyObject *m_qualname;
#endif

#if PYTHON_VERSION >= 0x3c0
    PyObject *m_type_params;
#endif

    // Constant return value to use.
    PyObject *m_constant_return_value;

    // A kind of uuid for the function object, used in comparisons.
    long m_counter;

    // Closure taken objects, for use in __closure__ and for accessing it.
    Py_ssize_t m_closure_given;
    struct HxHGoN_CellObject *m_closure[1];
};

extern PyTypeObject HxHGoN_Function_Type;

// Make a function with context.
#if PYTHON_VERSION < 0x300
extern struct HxHGoN_FunctionObject *HxHGoN_Function_New(function_impl_code c_code, PyObject *name,
                                                         PyCodeObject *code_object, PyObject *defaults,
                                                         PyObject *module, PyObject *doc,
                                                         struct HxHGoN_CellObject **closure, Py_ssize_t closure_given);
#else
extern struct HxHGoN_FunctionObject *HxHGoN_Function_New(function_impl_code c_code, PyObject *name, PyObject *qualname,
                                                         PyCodeObject *code_object, PyObject *defaults,
                                                         PyObject *kw_defaults, PyObject *annotations, PyObject *module,
                                                         PyObject *doc, struct HxHGoN_CellObject **closure,
                                                         Py_ssize_t closure_given);
#endif

extern void HxHGoN_Function_EnableConstReturnTrue(struct HxHGoN_FunctionObject *function);

extern void HxHGoN_Function_EnableConstReturnFalse(struct HxHGoN_FunctionObject *function);

extern void HxHGoN_Function_EnableConstReturnGeneric(struct HxHGoN_FunctionObject *function, PyObject *value);

#ifdef _HUNTER_PLUGIN_DILL_ENABLED
extern PyObject *HxHGoN_Function_GetFunctionState(struct HxHGoN_FunctionObject *function,
                                                  function_impl_code const *function_table);
extern struct HxHGoN_FunctionObject *HxHGoN_Function_CreateFunctionViaCodeIndex(
    PyObject *module, PyObject *function_qualname, PyObject *function_index, PyObject *code_object_desc,
    PyObject *constant_return_value, PyObject *defaults, PyObject *kw_defaults, PyObject *doc, PyObject *closure,
    PyObject *annotations, PyObject *func_dict, function_impl_code const *function_table, int function_table_size);
extern PyObject *HxHGoN_Function_ExtractCodeObjectDescription(PyThreadState *tstate,
                                                              struct HxHGoN_FunctionObject *function);
#endif

static inline bool HxHGoN_Function_Check(PyObject *object) { return Py_TYPE(object) == &HxHGoN_Function_Type; }

static inline PyObject *HxHGoN_Function_GetName(PyObject *object) {
    return ((struct HxHGoN_FunctionObject *)object)->m_name;
}

PyObject *HxHGoN_CallFunctionNoArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function);

PyObject *HxHGoN_CallFunctionPosArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                     PyObject *const *args, Py_ssize_t args_size);

PyObject *HxHGoN_CallFunctionVectorcall(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                        PyObject *const *args, Py_ssize_t args_size, PyObject *const *kw_names,
                                        Py_ssize_t kw_size);
PyObject *HxHGoN_CallFunctionPosArgsKwArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                           PyObject *const *args, Py_ssize_t args_size, PyObject *kw);
PyObject *HxHGoN_CallFunctionPosArgsKwSplit(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                            PyObject *const *args, Py_ssize_t args_size, PyObject *const *kw_values,
                                            PyObject *kw_names);

PyObject *HxHGoN_CallMethodFunctionNoArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                          PyObject *object);
PyObject *HxHGoN_CallMethodFunctionPosArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                           PyObject *object, PyObject *const *args, Py_ssize_t args_size);
PyObject *HxHGoN_CallMethodFunctionPosArgsKwArgs(PyThreadState *tstate, struct HxHGoN_FunctionObject const *function,
                                                 PyObject *object, PyObject *const *args, Py_ssize_t args_size,
                                                 PyObject *kw);

#if _DEBUG_REFCOUNTS
extern int count_active_HxHGoN_Function_Type;
extern int count_allocated_HxHGoN_Function_Type;
extern int count_released_HxHGoN_Function_Type;
#endif

#endif


