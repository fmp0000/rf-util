/*
 * Copyright 2021-2022, 2024 NXP
 */

/*
 * NXP Proprietary. This software is owned or controlled by NXP and may only
 * be used strictly in accordance with the applicable license terms. By expressly accepting
 * such terms or by downloading, installing, activating and/or otherwise using
 * the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to
 * be bound by the applicable license terms, then you may not retain,
 * install, activate or otherwise use the software.
 */

#include <rflib_common.h>
#ifdef MT3812
#include <fr1.h>
#endif

rflib_ll_t rflib_fr1_log_level = LL_ERR;

/* This function should never be called before get_cmd_handle() */
void rflib_set_loglevel(rflib_ll_t loglevel )
{
    rflib_fr1_log_level = loglevel;
#ifdef MT3812
    rf_mdata[0]->log_level = loglevel;
#endif
}
