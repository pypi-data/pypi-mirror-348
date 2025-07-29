//     Copyright 2025, GONHXH,  find license text at end of file

#ifndef __HUNTER_COMPILED_CELL_H__
#define __HUNTER_COMPILED_CELL_H__

/* This is a clone of the normal PyCell structure. We should keep it binary
 * compatible, just in case somebody crazy insists on it.
 */

extern PyTypeObject HxHGoN_Cell_Type;

static inline bool HxHGoN_Cell_Check(PyObject *object) { return Py_TYPE(object) == &HxHGoN_Cell_Type; }

struct HxHGoN_CellObject {
    /* Python object folklore: */
    PyObject_HEAD

        /* Content of the cell or NULL when empty */
        PyObject *ob_ref;
};

// Create cell with out value, and with or without reference given.
extern struct HxHGoN_CellObject *HxHGoN_Cell_NewEmpty(void);
extern struct HxHGoN_CellObject *HxHGoN_Cell_New0(PyObject *value);
extern struct HxHGoN_CellObject *HxHGoN_Cell_New1(PyObject *value);

// Check stuff while accessing a compile cell in debug mode.
#ifdef __HUNTER_NO_ASSERT__
#define HxHGoN_Cell_GET(cell) (((struct HxHGoN_CellObject *)(cell))->ob_ref)
#else
#define HxHGoN_Cell_GET(cell)                                                                                          \
    (CHECK_OBJECT(cell), assert(HxHGoN_Cell_Check((PyObject *)cell)), (((struct HxHGoN_CellObject *)(cell))->ob_ref))
#endif

#if _DEBUG_REFCOUNTS
extern int count_active_HxHGoN_Cell_Type;
extern int count_allocated_HxHGoN_Cell_Type;
extern int count_released_HxHGoN_Cell_Type;
#endif

HUNTER_MAY_BE_UNUSED static inline void HxHGoN_Cell_SET(struct HxHGoN_CellObject *cell_object, PyObject *value) {
    CHECK_OBJECT_X(value);
    CHECK_OBJECT(cell_object);

    assert(HxHGoN_Cell_Check((PyObject *)cell_object));
    cell_object->ob_ref = value;
}

#endif


