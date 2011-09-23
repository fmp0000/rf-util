/*
 * Copyright 2021-2023 NXP
 * NXP Confidential. This software is owned or controlled by NXP and may only
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
%apply unsigned int *OUTPUT{uint32_t *val };
%apply unsigned int *OUTPUT{ uint32_t *band};
%apply unsigned int *OUTPUT{ uint32_t *freq_in_khz};
%apply unsigned int *OUTPUT{ uint32_t *lna_state};
%apply unsigned int *OUTPUT{ uint32_t *gain_in_db};
%apply unsigned int *OUTPUT{ uint32_t *vga_dac1_val, uint32_t *vga_dac2_val};
%apply unsigned int *OUTPUT{ uint32_t *demod_rf_attn, uint32_t *demod_bb_gain};
%apply int *OUTPUT { int32_t *fine0,
    int32_t *fine1, 
    int32_t *fine2, 
    int32_t *fine3, 
    int32_t *fine4, 
    int32_t *fine5, 
    int32_t *fine6, 
    int32_t *fine7, 
    int32_t *coarse0,
    int32_t *coarse1,
    int32_t *coarse2,
    int32_t *coarse3,
    int32_t *coarse4,
    int32_t *coarse5,
    int32_t *coarse6,
    int32_t *coarse7 };

%apply unsigned int *OUTPUT {uint32_t *vco_sel_out, uint32_t *cal_cap, uint32_t cal_current};
%apply unsigned int *OUTPUT {uint32_t *mode, uint32_t *freq_khz, uint32_t *cal_band};
%apply unsigned int *OUTPUT {uint32_t *mode, uint32_t *vco_sel, uint32_t *freq_khz,  
    uint32_t *cal_cap, uint32_t *cal_current};
%apply unsigned int *OUTPUT { uint32_t *path, uint32_t *band,uint32_t *rssi_mode, uint32_t *dpd, 
                uint32_t *rxbw, uint32_t *txbw };
%apply unsigned int *OUTPUT {uint32_t *rtc, uint32_t *hw_ver,
    uint32_t *min_ver,
    uint32_t *maj_ver,
    uint32_t *tgt_ver,
    uint32_t *bld_nr,
    uint32_t *test_nr,
    uint32_t *dbg_flg
};

%apply unsigned int *OUTPUT {uint32_t *sys_state, uint32_t *trxpll_vco_det_lo,
    uint32_t *trxpll_vco_det_hi, uint32_t *trxpll_vtune_det_lo, uint32_t *trxpll_vtune_det_hi,
    uint32_t *trxpll_unlock, uint32_t *calpll_vtune_det_lo, uint32_t *calpll_vtune_det_hi,
    uint32_t *calpll_unlock};
%apply unsigned int *OUTPUT {uint32_t *rx1_manual, uint32_t *rx1_hash_mode, uint32_t *channel,
    uint32_t *rx1_bbgain, uint32_t *rx1_rfgain, uint32_t *rx1_gain, uint32_t *rx2_manual, uint32_t *rx2_hash_mode, uint32_t *rx2_bbgain,
    uint32_t *rx2_rfgain, uint32_t *rx2_gain, uint32_t *tx1_gain, uint32_t *tx2_gain, uint32_t *rx1_gain_raw, uint32_t *rx2_gain_raw,
    uint32_t *tx1_gain_raw, uint32_t *tx2_gain_raw, uint32_t *tx_gain_idx, uint32_t *rx_gain_idx};
%apply unsigned int *OUTPUT { uint32_t *temperature, uint32_t *value_raw};
%apply unsigned int *OUTPUT { uint32_t *bw, uint32_t *bw_ftune};
/* %apply unsigned int OUTPUT[ANY] { uint32_t fine[8], uint32_t coarse[8] }; */
%apply unsigned int *OUTPUT {uint32_t  *value1, uint32_t *value2, uint32_t *value3,
        uint32_t *value4, uint32_t *value5, uint32_t *value6, uint32_t *value7, uint32_t *value8};
%apply unsigned int *OUTPUT {uint32_t  *mode};
%apply unsigned int *OUTPUT {uint32_t *yuc1_trxstatus, uint32_t *yuc1_calstatus,
    uint32_t *yuc2_trxstatus, uint32_t *yuc2_calstatus};
%apply int *OUTPUT {int32_t *psEnforcedGain};
%apply signed *OUTPUT {int32_t *gain_db, uint32_t *tx_gain_return_code};
%apply signed *OUTPUT {uint32_t *freq_khz, uint32_t *txbw, uint32_t *rxbw,
        uint8_t *txgain_idx, uint8_t *rxgain_idx,
        uint8_t *FR1Mode, uint8_t *dupmode, uint8_t *dpd_loopback,
        uint8_t *qec_loopback,uint8_t *gset_tx, uint8_t *gset_rx,
        int32_t *txgain_db, int32_t *rxgain_db, int8_t *pa_ctrl_en,
        int8_t *lna_ctrl_en, int8_t *txrelgain_db, int8_t *rxrelgain_db,
        uint32_t *rssi1, uint32_t *rssi2, uint32_t *rssi3, uint32_t *rssi4, uint8_t *agc_blocker,
        uint8_t *gset_rx1, uint8_t *gset_rx2, uint8_t *gset_rx3, uint8_t *gset_rx4};

%inline %{
#ifdef ICEWINGS
    extern int icw_get_version( uint32_t *hw_ver, uint32_t *min_ver, uint32_t *maj_ver,
        uint32_t *bld_nr);
    extern int icw_get_curdata(uint32_t *freq_khz, uint32_t *txbw, uint32_t *rxbw,
        uint8_t *txgain_idx, uint8_t *rxgain_idx,
        uint8_t *dpd_loopback, uint8_t *qec_loopback,
        uint8_t *gset_tx, uint8_t *gset_rx, int32_t *txgain_db, int32_t *rxgain_db,
        int8_t *pa_ctrl_en, int8_t *lna_ctrl_en, int8_t *txrelgain_db,
        int8_t *rxrelgain_db, uint32_t *rssi1, uint32_t *rssi2, uint32_t *rssi3,
        uint32_t *rssi4, uint8_t *agc_blocker, uint8_t *gset_rx1, uint8_t *gset_rx2,
        uint8_t *gset_rx3, uint8_t *gset_rx4);
#endif
%}

%{
#define SWIG_FILE_WITH_INIT
#include <stdint.h>
#include <stddef.h>
#include <stdlib.h>
#include "rfdev_ioctl.h"
#include "rf_if.h"
#include "rflib_common.h"
#include "rf_sw_cmd_types.h"
#include "rf_init.h"
#include "rf_common.h"
#ifdef ICEWINGS
#include "icw_rfic_types.h"
#include "fr1.h"
#endif
%}

%include "rfdev_ioctl.h"
%include "rf_if.h"
%include "rflib_common.h"
%include "rf_sw_cmd_types.h"
%include "rf_init.h"
%include "rf_common.h"
#ifdef ICEWINGS
%include "fr1.h"
%include "icw_rfic_types.h"
#endif
