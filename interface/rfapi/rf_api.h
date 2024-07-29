/*
 * Copyright 2024 NXP
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

#ifndef _RF_API_H_
#define _RF_API_H_

#include <stdint.h>
#include <sys/types.h>
#include <time.h>

#define RFAPI

#include "fr1.h"
#include "rflib_common.h"

/*
 * MT Error Codes
 *
 * MT3812_NOERR = 0 - No error
 * MT3812_ERROR = -1 - Unspecified error
 * MT3812_ENOTSUP = -2 - Not supported error
 * MT3812_ECMDPROC = -3 - Command  Procedure Error
 * MT3812_ERSPPROC = -4 - Response Procedure Error
 * MT3812_EINVTR = -5 - Invalid state transition
 * MT3812_EINVPR = -6 - Invalid parameter
 * MT3812_ENOMEM = -7 - Out of memory
 */


typedef struct api_latency {
    rf_sw_cmd_t rf_api;
    struct timespec start_time;
    struct timespec end_time;
} api_latency_t;


/*
 * rfic_api_init
 *
 * First API to be called before calling any RF API
 *
 * Input: FR1DevType devtype
 * Returns: RficAPIHandle_t
 */

RficAPIHandle_t rfic_api_init( FR1DevType devtype );


/*
 * rfic_api_deinit
 *
 * Input: RficAPIHandle_t xAPIHandle
 * Return: MT3812_NOERR
 *
 * Tihs API needs to be called once the API usage is complete
 */

int32_t rfic_api_deinit( RficAPIHandle_t xAPIHandle);


/*
 * rfic_adjust_pll_freq
 *
 * Inputs: xAPIHandle, freq_khz
 * It follows following sequence:
 * 	rf_set_active - 
 * 	rf_set_path
 * 	rf_adjust_pll_freq
 * 	rf_set_path
 * 	rf_set_active
 *
 * Return: rtc message
 */

int32_t rfic_adjust_pll_freq( RficAPIHandle_t xAPIHandle, uint32_t freq_khz );


/*
 * rfic_gain_control_tx_relative_diff
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t ucGainIndB
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 */

int32_t rfic_gain_control_tx_relative_diff( RficAPIHandle_t xAPIHandle, int32_t ucGainIndB);


/*
 * rfic_gain_control_rx_relative_diff
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t ucGainIndB
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 */

int32_t rfic_gain_control_rx_relative_diff( RficAPIHandle_t xAPIHandle, int32_t ucGainIndB);


/*
 * rfic_gain_set_tx_gain_idx
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  uint32_t bb_idx
 * 	  uint32_t rf_idx
 *
 * Return: rtc message
 */

int32_t rfic_gain_set_tx_gain_idx(RficAPIHandle_t xAPIHandle, uint32_t bb_idx, uint32_t rf_idx);


/*
 * rfic_gain_set_rx_gain_idx
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  uint32_t bb_idx
 * 	  uint32_t rf_idx
 *
 * Return: rtc message
 */

int32_t rfic_gain_set_rx_gain_idx(RficAPIHandle_t xAPIHandle, uint32_t idx, uint32_t rf_idx);


/*
 * rfic_get_tx_gain_value
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t *gain
 *
 * Return: gain value
 */

float rfic_get_tx_gain_value( RficAPIHandle_t xAPIHandle, int32_t *gain );


/*
 * rfic_get_rx_gain_value
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t *gain
 *
 * Return: gain value
 */

float rfic_get_rx_gain_value( RficAPIHandle_t xAPIHandle, int32_t *gain );


/*
 * rfic_get_status
 *
 * Input: RficAPIHandle_t xAPIHandle
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 *
 * Output: Prints the Status
 */

float rfic_get_status( RficAPIHandle_t xAPIHandle );

#endif
