/*
 * Copyright 2021-2024 NXP
 * NXP Proprietary. This software is owned or controlled by NXP and may only
 * be used strictly in accordance with the applicable license terms. By expressly accepting
 * such terms or by downloading, installing, activating and/or otherwise using
 * the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to
 * be bound by the applicable license terms, then you may not retain,
 * install, activate or otherwise use the software.
 */

%module rfif
%include "typemaps.i"
%include "carrays.i"
%array_class(int, intArray);

%typemap(in) uint8_t {
        $1 = lua_tostring(L,$input);
       }

%typemap(in) int8_t {
        $1 = lua_tostring(L,$input);
       }

%typemap(memberin) uint8_t [ANY] {
  if ($input) strncpy((char *)$1, (const char *)$input, $1_dim0);
  else $1[0] = 0;
}

%typemap(in) uint8_t[] {
        $1 = (const char*)lua_tostring(L,$input);
}

%typemap(in) uint8_t* {
        $1 = (const char*)lua_tostring(L,$input);
}

%typemap(in) uint16_t {
        $1 = (unsigned short) lua_tonumber(L,$input);
}

%typemap(in) uint32_t {
        $1 = (unsigned int) lua_tonumber(L,$input);
}

%typemap(in) int32_t {
        $1 = (int) lua_tonumber(L,$input);
}

%typemap(in) uint64_t {
        $1 = (unsigned long long) lua_tonumber(L,$input);
}

%apply unsigned char { uint8_t };
%apply char { int8_t };
%apply const char[]{ uint8_t [ANY]};
%apply const char* { uint8_t *};
%apply unsigned short { uint16_t };
%apply unsigned int { uint32_t };
%apply int { int32_t };
%apply unsigned long long { uint64_t };

%inline %{
#ifdef MT3812
    /*
    extern int fw_prog_mem_size_R2_7_001;
    extern unsigned short fw_prog_mem_R2_7_001[];
    extern int fw_init_mem_size_R2_7_001;
    extern unsigned short fw_init_mem_R2_7_001[];
    */
#endif
%}

%{
#define SWIG_FILE_WITH_INIT
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include <rflib_common.h>
#ifdef MT3812 
#include "fr1.h"
#include "types.h"
#include "complex_types.h"
#include "diora_l1al.h"
#include "diora_osal.h"
#include "diora_phal.h"
#endif
%}

%include "rflib_common.h"
#ifdef MT3812
%include "fr1.h"
%include "types.h"
%include "complex_types.h"
%include "diora_l1al.h"
%include "diora_osal.h"
%include "diora_phal.h"
#endif
