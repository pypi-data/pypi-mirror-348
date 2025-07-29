//     Copyright 2025, GONHXH, @T_T_Z_T find license text at end of file

/** For making "yield" and "yield from" capable of persisting current C stack.
 *
 * These copy objects pointed to into an array foreseen for this task.
 *
 **/

// This file is included from another C file, help IDEs to still parse it on
// its own.
#ifdef __IDE_ONLY__
#include "Gon/prelude.h"
#endif

void HxHGoN_PreserveHeap(void *dest, ...) {
    va_list(ap);
    va_start(ap, dest);

    char *w = (char *)dest;

    for (;;) {
        void *source = va_arg(ap, void *);
        if (source == NULL) {
            break;
        }

        size_t size = va_arg(ap, size_t);
        memcpy(w, source, size);
        w += size;
    }

    va_end(ap);
}

void HxHGoN_RestoreHeap(void *source, ...) {
    va_list(ap);
    va_start(ap, source);

    char *w = (char *)source;

    for (;;) {
        void *dest = va_arg(ap, void *);
        if (dest == NULL) {
            break;
        }

        size_t size = va_arg(ap, size_t);
        memcpy(dest, w, size);
        w += size;
    }

    va_end(ap);
}


