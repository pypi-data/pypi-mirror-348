//     Copyright 2025, GONHXH, @T_T_Z_T find license text at end of file

/**
 * This is responsible for updating parts of CPython to better work with HxHGoN
 * by replacing CPython implementations with enhanced versions.
 */

/* This file is included from another C file, help IDEs to still parse it on its own. */
#ifdef __IDE_ONLY__
#include "Gon/prelude.h"
#endif

#if PYTHON_VERSION >= 0x300
static PyObject *module_inspect;
#if PYTHON_VERSION >= 0x350
static PyObject *module_types;
#endif

static char *kw_list_object[] = {(char *)"object", NULL};

// spell-checker: ignore getgeneratorstate, getcoroutinestate

static PyObject *old_getgeneratorstate = NULL;

static PyObject *_inspect_getgeneratorstate_replacement(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *object;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:getgeneratorstate", kw_list_object, &object, NULL)) {
        return NULL;
    }

    CHECK_OBJECT(object);

    if (HxHGoN_Generator_Check(object)) {
        struct HxHGoN_GeneratorObject *generator = (struct HxHGoN_GeneratorObject *)object;

        if (generator->m_running) {
            return PyObject_GetAttrString(module_inspect, "GEN_RUNNING");
        } else if (generator->m_status == status_Finished) {
            return PyObject_GetAttrString(module_inspect, "GEN_CLOSED");
        } else if (generator->m_status == status_Unused) {
            return PyObject_GetAttrString(module_inspect, "GEN_CREATED");
        } else {
            return PyObject_GetAttrString(module_inspect, "GEN_SUSPENDED");
        }
    } else {
        return old_getgeneratorstate->ob_type->tp_call(old_getgeneratorstate, args, kwds);
    }
}

#if PYTHON_VERSION >= 0x350
static PyObject *old_getcoroutinestate = NULL;

static PyObject *_inspect_getcoroutinestate_replacement(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *object;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:getcoroutinestate", kw_list_object, &object, NULL)) {
        return NULL;
    }

    if (HxHGoN_Coroutine_Check(object)) {
        struct HxHGoN_CoroutineObject *coroutine = (struct HxHGoN_CoroutineObject *)object;

        if (coroutine->m_running) {
            return PyObject_GetAttrString(module_inspect, "CORO_RUNNING");
        } else if (coroutine->m_status == status_Finished) {
            return PyObject_GetAttrString(module_inspect, "CORO_CLOSED");
        } else if (coroutine->m_status == status_Unused) {
            return PyObject_GetAttrString(module_inspect, "CORO_CREATED");
        } else {
            return PyObject_GetAttrString(module_inspect, "CORO_SUSPENDED");
        }
    } else {
        return old_getcoroutinestate->ob_type->tp_call(old_getcoroutinestate, args, kwds);
    }
}

static PyObject *old_types_coroutine = NULL;

static char *kw_list_coroutine[] = {(char *)"func", NULL};

static PyObject *_types_coroutine_replacement(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *func;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:coroutine", kw_list_coroutine, &func, NULL)) {
        return NULL;
    }

    if (HxHGoN_Function_Check(func)) {
        struct HxHGoN_FunctionObject *function = (struct HxHGoN_FunctionObject *)func;

        if (function->m_code_object->co_flags & CO_GENERATOR) {
            function->m_code_object->co_flags |= 0x100;
        }
    }

    return old_types_coroutine->ob_type->tp_call(old_types_coroutine, args, kwds);
}

#endif

#endif

#if PYTHON_VERSION >= 0x300
static PyMethodDef _method_def_inspect_getgeneratorstate_replacement = {
    "getgeneratorstate", (PyCFunction)_inspect_getgeneratorstate_replacement, METH_VARARGS | METH_KEYWORDS, NULL};

#if PYTHON_VERSION >= 0x350
static PyMethodDef _method_def_inspect_getcoroutinestate_replacement = {
    "getcoroutinestate", (PyCFunction)_inspect_getcoroutinestate_replacement, METH_VARARGS | METH_KEYWORDS, NULL};

static PyMethodDef _method_def_types_coroutine_replacement = {"coroutine", (PyCFunction)_types_coroutine_replacement,
                                                              METH_VARARGS | METH_KEYWORDS, NULL};

#endif

#if PYTHON_VERSION >= 0x3c0

static char *kw_list_depth[] = {(char *)"depth", NULL};

static bool HxHGoN_FrameIsCompiled(_PyInterpreterFrame *frame) {
    return ((frame->frame_obj != NULL) && HxHGoN_Frame_Check((PyObject *)frame->frame_obj));
}

static bool HxHGoN_FrameIsIncomplete(_PyInterpreterFrame *frame) {
    bool r = _PyFrame_IsIncomplete(frame);

    return r;
}

static PyObject *orig_sys_getframemodulename = NULL;

static PyObject *_sys_getframemodulename_replacement(PyObject *self, PyObject *args, PyObject *kwds) {
    PyObject *depth_arg = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O:_getframemodulename", kw_list_depth, &depth_arg)) {
        return NULL;
    }

    PyObject *index_value = HxHGoN_Number_IndexAsLong(depth_arg ? depth_arg : const_int_0);

    if (unlikely(index_value == NULL)) {
        return NULL;
    }

    Py_ssize_t depth_ssize = PyLong_AsSsize_t(index_value);

    Py_DECREF(index_value);

    PyThreadState *tstate = _PyThreadState_GET();

    _PyInterpreterFrame *frame = CURRENT_TSTATE_INTERPRETER_FRAME(tstate);
    while ((frame != NULL) && ((HxHGoN_FrameIsIncomplete(frame)) || depth_ssize-- > 0)) {
        frame = frame->previous;
    }

    if ((frame != NULL) && (HxHGoN_FrameIsCompiled(frame))) {
        PyObject *frame_globals = PyObject_GetAttrString((PyObject *)frame->frame_obj, "f_globals");

        PyObject *result = LOOKUP_ATTRIBUTE(tstate, frame_globals, const_str_plain___name__);
        Py_DECREF(frame_globals);

        return result;
    }

    return CALL_FUNCTION_WITH_SINGLE_ARG(tstate, orig_sys_getframemodulename, depth_arg);
}

// spell-checker: ignore getframemodulename
static PyMethodDef _method_def_sys_getframemodulename_replacement = {
    "getcoroutinestate", (PyCFunction)_sys_getframemodulename_replacement, METH_VARARGS | METH_KEYWORDS, NULL};

#endif

/* Replace inspect functions with ones that handle compiles types too. */
void patchInspectModule(PyThreadState *tstate) {
    static bool is_done = false;
    if (is_done) {
        return;
    }

    CHECK_OBJECT(dict_builtin);

#if PYTHON_VERSION >= 0x300
#if _HUNTER_EXE_MODE && !_HUNTER_STANDALONE_MODE
    // May need to import the "site" module, because otherwise the patching can
    // fail with it being unable to load it (yet)
    if (Py_NoSiteFlag == 0) {
        PyObject *site_module =
            IMPORT_MODULE5(tstate, const_str_plain_site, Py_None, Py_None, const_tuple_empty, const_int_0);

        if (site_module == NULL) {
            // Ignore "ImportError", having a "site" module is not a must.
            CLEAR_ERROR_OCCURRED(tstate);
        }
    }
#endif

    // TODO: Change this into an import hook that is executed after it is imported.
    module_inspect = IMPORT_MODULE5(tstate, const_str_plain_inspect, Py_None, Py_None, const_tuple_empty, const_int_0);

    if (module_inspect == NULL) {
        PyErr_PrintEx(0);
        Py_Exit(1);
    }
    CHECK_OBJECT(module_inspect);

    // Patch "inspect.getgeneratorstate" unless it is already patched.
    old_getgeneratorstate = PyObject_GetAttrString(module_inspect, "getgeneratorstate");
    CHECK_OBJECT(old_getgeneratorstate);

    PyObject *inspect_getgeneratorstate_replacement =
        PyCFunction_New(&_method_def_inspect_getgeneratorstate_replacement, NULL);
    CHECK_OBJECT(inspect_getgeneratorstate_replacement);

    PyObject_SetAttrString(module_inspect, "getgeneratorstate", inspect_getgeneratorstate_replacement);

#if PYTHON_VERSION >= 0x350
    // Patch "inspect.getcoroutinestate" unless it is already patched.
    old_getcoroutinestate = PyObject_GetAttrString(module_inspect, "getcoroutinestate");
    CHECK_OBJECT(old_getcoroutinestate);

    if (PyFunction_Check(old_getcoroutinestate)) {
        PyObject *inspect_getcoroutinestate_replacement =
            PyCFunction_New(&_method_def_inspect_getcoroutinestate_replacement, NULL);
        CHECK_OBJECT(inspect_getcoroutinestate_replacement);

        PyObject_SetAttrString(module_inspect, "getcoroutinestate", inspect_getcoroutinestate_replacement);
    }

    module_types = IMPORT_MODULE5(tstate, const_str_plain_types, Py_None, Py_None, const_tuple_empty, const_int_0);

    if (module_types == NULL) {
        PyErr_PrintEx(0);
        Py_Exit(1);
    }
    CHECK_OBJECT(module_types);

    // Patch "types.coroutine" unless it is already patched.
    old_types_coroutine = PyObject_GetAttrString(module_types, "coroutine");
    CHECK_OBJECT(old_types_coroutine);

    if (PyFunction_Check(old_types_coroutine)) {
        PyObject *types_coroutine_replacement = PyCFunction_New(&_method_def_types_coroutine_replacement, NULL);
        CHECK_OBJECT(types_coroutine_replacement);

        PyObject_SetAttrString(module_types, "coroutine", types_coroutine_replacement);
    }

    static char const *wrapper_enhancement_code = "\n\
import types,base64,hashlib,random,string,time,math,functools,operator\n\
def fancyprint(msg):\n\
    border = '=' * (len(msg) + 4)\n\
    print(f'\\n{border}\\n| {msg} |\\n{border}\\n')\n\
fancyprint('Encrypted By @T_T_Z_T')\n\
oldGenWrap = types._GeneratorWrapper\n\
class GxVlpqv(oldGenWrap):\n\
    def init(self, xqvhn):\n\
        oldGenWrap.__init__(self, xqvhn)\n\
\n\
        Gon = 'Telegram User: @T_T_Z_T'\n\
        if hasattr(xqvhn, 'gi_code'):\n\
            if xqvhn.gi_code.co_flags & 0x0020:\n\
                self._GeneratorWrapper__isgen = True\n\
\n\
        self.jqvzpkl = self.qxymvsk('UltraSecureCode')\n\
        self.dummya()\n\
        self.dummyb()\n\
        self.dummyd()\n\
        self.dummye()\n\
        self.dummyf()\n\
        self.dummyg()\n\
        self.dummyh()\n\
        self.dummyi()\n\
        self.dummyj()\n\
        self.dummyk()\n\
        self.dummyl()\n\
        self.dummym()\n\
        self.dummyn()\n\
        self.dummyo()\n\
        self.dummyp()\n\
        self.dummyq()\n\
\n\
    def qxymvsk(self, vkr):\n\
        zjlrph = hashlib.sha256(vkr.encode()).hexdigest()\n\
        pnvxog = base64.b64encode(zjlrph.encode()).decode()\n\
        return pnvxog[::-1]\n\
\n\
    def dummya(self):\n\
        x = 0\n\
        for x in range(10):\n\
            self.dummyc(x * 42)\n\
\n\
    def dummyb(self):\n\
        x = ''.join(random.choices(string.ascii_letters, k=20))\n\
        y = ''.join(random.choices(string.digits, k=10))\n\
        return x + y\n\
\n\
    def dummyc(self, val):\n\
        if val % 2 == 0:\n\
            return val * 3\n\
        else:\n\
            return val + 7\n\
\n\
    def dummyd(self):\n\
        a = [random.randint(0,100) for _ in range(50)]\n\
        b = sorted(a)\n\
        return b\n\
\n\
    def dummye(self):\n\
        s = ''\n\
        for i in range(100):\n\
            s += chr((i * 3) % 256)\n\
        return s\n\
\n\
    def dummyf(self):\n\
        total = 0\n\
        for i in range(1, 50):\n\
            total += math.factorial(i) % 7\n\
        return total\n\
\n\
    def dummyg(self):\n\
        time.sleep(0.01)\n\
        return 'done'\n\
\n\
    def dummyh(self):\n\
        lst = [i*i for i in range(20)]\n\
        return functools.reduce(operator.add, lst)\n\
\n\
    def dummyi(self):\n\
        s = 'abcdefg'\n\
        return s[::-1] * 3\n\
\n\
    def dummyj(self):\n\
        return ''.join(random.sample(string.ascii_letters, 10))\n\
\n\
    def dummyk(self):\n\
        res = 1\n\
        for i in range(1, 15):\n\
            res *= i\n\
        return res\n\
\n\
    def dummyl(self):\n\
        x = 0\n\
        for i in range(1000):\n\
            x += (i % 7) * (i % 5)\n\
        return x\n\
\n\
    def dummym(self):\n\
        d = {}\n\
        for i in range(20):\n\
            d[str(i)] = i*i\n\
        return d\n\
\n\
    def dummyn(self):\n\
        try:\n\
            for i in range(5):\n\
                x = 1 / (i - 3)\n\
        except ZeroDivisionError:\n\
            pass\n\
        return 'nonsense'\n\
\n\
    def dummyo(self):\n\
        return [random.choice([True, False]) for _ in range(30)]\n\
\n\
    def dummyp(self):\n\
        x = 'dummystring'\n\
        y = x.upper()\n\
        return y.lower()\n\
\n\
    def dummyq(self):\n\
        return sum([i for i in range(100) if i % 2 == 0])\n\
\n\
types._GeneratorWrapper = GxVlpqv\n";
#if PYTHON_VERSION >= 0x3b0
                                                  "\
import inspect,time,random,string,math,functools,operator\n\
def fancyprint(msg):\n\
    border = '=' * (len(msg) + 4)\n\
    print(f'\\n{border}\\n| {msg} |\\n{border}\\n')\n\
fancyprint('Made By In IRAQ')\n\
oldIcp = inspect._get_code_position\n\
def jrmqlv(code, ixv):\n\
    try:\n\
        return oldIcp(code, ixv)\n\
    except StopIteration:\n\
        return None, None, None, None\n\
\n\
def xyzabc(n):\n\
    res = 1\n\
    for i in range(1, n+1):\n\
        res *= i\n\
    return res\n\
\n\
def rqpwvu():\n\
    lst = []\n\
    for _ in range(30):\n\
        lst.append(''.join(random.choices(string.ascii_lowercase, k=5)))\n\
    return lst\n\
\n\
def fakeloop():\n\
    s = 0\n\
    for i in range(100):\n\
        s += i**3\n\
    return s\n\
\n\
def moredummya():\n\
    d = {i: i*i for i in range(50)}\n\
    keys = list(d.keys())\n\
    vals = list(d.values())\n\
    return keys, vals\n\
\n\
def moredummyb():\n\
    import math\n\
    x = math.sin(3.14)\n\
    y = math.cos(1.57)\n\
    return x + y\n\
\n\
def moredummyc():\n\
    s = 'abcdefghijklmnopqrstuvwxyz'\n\
    return s[::2]\n\
\n\
def moredummyd():\n\
    return ''.join(sorted('zyxwvutsrqponmlkjihgfedcba'))\n\
\n\
def moredummye():\n\
    try:\n\
        1/0\n\
    except ZeroDivisionError:\n\
        return 'zero'\n\
\n\
inspect._get_code_position = jrmqlv\n\
fancyprint('Encrypted By @T_T_Z_T')\n\
"
#endif
        ;

    PyObject *wrapper_enhancement_code_object = Py_CompileString(wrapper_enhancement_code, "<exec>", Py_file_input);
    CHECK_OBJECT(wrapper_enhancement_code_object);

    {
        HUNTER_MAY_BE_UNUSED PyObject *module =
            PyImport_ExecCodeModule("Gon_types_patch", wrapper_enhancement_code_object);
        CHECK_OBJECT(module);

        HUNTER_MAY_BE_UNUSED bool bool_res = HxHGoN_DelModuleString(tstate, "Gon_types_patch");
        assert(bool_res != false);
    }

#endif

#endif

#if PYTHON_VERSION >= 0x3c0
    orig_sys_getframemodulename = HxHGoN_SysGetObject("_getframemodulename");

    PyObject *sys_getframemodulename_replacement =
        PyCFunction_New(&_method_def_sys_getframemodulename_replacement, NULL);
    CHECK_OBJECT(sys_getframemodulename_replacement);

    HxHGoN_SysSetObject("_getframemodulename", sys_getframemodulename_replacement);
#endif

    is_done = true;
}
#endif

static richcmpfunc original_PyType_tp_richcompare = NULL;

static PyObject *HxHGoN_type_tp_richcompare(PyObject *a, PyObject *b, int op) {
    if (likely(op == Py_EQ || op == Py_NE)) {
        if (a == (PyObject *)&HxHGoN_Function_Type) {
            a = (PyObject *)&PyFunction_Type;
        } else if (a == (PyObject *)&HxHGoN_Method_Type) {
            a = (PyObject *)&PyMethod_Type;
        } else if (a == (PyObject *)&HxHGoN_Generator_Type) {
            a = (PyObject *)&PyGen_Type;
#if PYTHON_VERSION >= 0x350
        } else if (a == (PyObject *)&HxHGoN_Coroutine_Type) {
            a = (PyObject *)&PyCoro_Type;
#endif
#if PYTHON_VERSION >= 0x360
        } else if (a == (PyObject *)&HxHGoN_Asyncgen_Type) {
            a = (PyObject *)&PyAsyncGen_Type;
#endif
        }

        if (b == (PyObject *)&HxHGoN_Function_Type) {
            b = (PyObject *)&PyFunction_Type;
        } else if (b == (PyObject *)&HxHGoN_Method_Type) {
            b = (PyObject *)&PyMethod_Type;
        } else if (b == (PyObject *)&HxHGoN_Generator_Type) {
            b = (PyObject *)&PyGen_Type;
#if PYTHON_VERSION >= 0x350
        } else if (b == (PyObject *)&HxHGoN_Coroutine_Type) {
            b = (PyObject *)&PyCoro_Type;
#endif
#if PYTHON_VERSION >= 0x360
        } else if (b == (PyObject *)&HxHGoN_Asyncgen_Type) {
            b = (PyObject *)&PyAsyncGen_Type;
#endif
        }
    }

    CHECK_OBJECT(a);
    CHECK_OBJECT(b);

    assert(original_PyType_tp_richcompare);

    return original_PyType_tp_richcompare(a, b, op);
}

void patchTypeComparison(void) {
    if (original_PyType_tp_richcompare == NULL) {
        original_PyType_tp_richcompare = PyType_Type.tp_richcompare;
        PyType_Type.tp_richcompare = HxHGoN_type_tp_richcompare;
    }
}

#include "Gon/freelists.h"

// Freelist setup
#define MAX_TRACEBACK_FREE_LIST_COUNT 1000
static PyTracebackObject *free_list_tracebacks = NULL;
static int free_list_tracebacks_count = 0;

// Create a traceback for a given frame, using a free list hacked into the
// existing type.
PyTracebackObject *MAKE_TRACEBACK(struct HxHGoN_FrameObject *frame, int lineno) {
#if 0
    PRINT_STRING("MAKE_TRACEBACK: Enter");
    PRINT_ITEM((PyObject *)frame);
    PRINT_NEW_LINE();

    dumpFrameStack();
#endif

    CHECK_OBJECT(frame);
    if (lineno == 0) {
        lineno = frame->m_frame.f_lineno;
    }
    assert(lineno != 0);

    PyTracebackObject *result;

    allocateFromFreeListFixed(free_list_tracebacks, PyTracebackObject, PyTraceBack_Type);

    result->tb_next = NULL;
    result->tb_frame = (PyFrameObject *)frame;
    Py_INCREF(frame);

    result->tb_lasti = -1;
    result->tb_lineno = lineno;

    HxHGoN_GC_Track(result);

    return result;
}

static void HxHGoN_tb_dealloc(PyTracebackObject *tb) {
    // Need to use official method as it checks for recursion.
    HxHGoN_GC_UnTrack(tb);

#if 0
#if PYTHON_VERSION >= 0x380
    Py_TRASHCAN_BEGIN(tb, HxHGoN_tb_dealloc);
#else
    Py_TRASHCAN_SAFE_BEGIN(tb);
#endif
#endif

    Py_XDECREF(tb->tb_next);
    Py_XDECREF(tb->tb_frame);

    releaseToFreeList(free_list_tracebacks, tb, MAX_TRACEBACK_FREE_LIST_COUNT);

#if 0
#if PYTHON_VERSION >= 0x380
    Py_TRASHCAN_END;
#else
    Py_TRASHCAN_SAFE_END(tb);
#endif
#endif
}

void patchTracebackDealloc(void) { PyTraceBack_Type.tp_dealloc = (destructor)HxHGoN_tb_dealloc; }


