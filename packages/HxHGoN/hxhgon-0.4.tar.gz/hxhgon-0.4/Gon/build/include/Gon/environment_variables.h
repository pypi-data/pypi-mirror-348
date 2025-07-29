//     Copyright 2025, GONHXH,  find license text at end of file

#ifndef __HUNTER_ENVIRONMENT_VARIABLES_H__
#define __HUNTER_ENVIRONMENT_VARIABLES_H__

#ifdef __IDE_ONLY__
#include "Gon/prelude.h"
#endif

#include "Gon/environment_variables_system.h"

extern void undoEnvironmentVariable(PyThreadState *tstate, char const *variable_name,
                                    environment_char_t const *old_value);

#endif


