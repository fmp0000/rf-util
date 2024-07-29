/*
 * Copyright 2024 NXP
 */

/*
 * NXP Proprietary. This software is owned or controlled by NXP and may only
 * be used strictly in accordance with the applicable license terms.
 * By expressly accepting such terms or by downloading, installing, activating
 * and/or otherwise using the software, you are agreeing that you have read,
 * and that you agree to comply with and are bound by, such license terms.
 * If you do not agree to be bound by the applicable license terms, then you
 * may not retain, install, activate or otherwise use the software.
 */


#include <stdio.h>
#include "rf_api.h"

extern struct rf_dev_mdata *rf_mdata[];

api_latency_t api_latency_info[RF_SW_CMD_MAX_COUNT];

/*
 * Helper function
 * Calculates the latency of the APIs - Start
 */

static inline void rf_start_latency_calc ( volatile rf_sw_cmd_t cmd)
{
    api_latency_info[cmd].rf_api = cmd;
    clock_gettime(CLOCK_MONOTONIC, &api_latency_info[cmd].start_time);
}


/*
 * Helper function
 * Calculates the latency of the APIs - End
 */

static inline void rf_end_latency_calc ( volatile rf_sw_cmd_t cmd)
{
    if(api_latency_info[cmd].rf_api == cmd){
        clock_gettime(CLOCK_MONOTONIC, &api_latency_info[cmd].end_time);
        rf_mdata[0]->nx_rf_dev.cmd_latencies[cmd] = \
	(api_latency_info[cmd].end_time.tv_sec - \
	api_latency_info[cmd].start_time.tv_sec)*1000000 \
        +(api_latency_info[cmd].end_time.tv_nsec - \
	api_latency_info[cmd].start_time.tv_nsec)/1000;
    }
}


/*
 * rfic_api_init
 *
 * First API to be called before calling any RF API
 *
 * Input: FR1DevType devtype
 * Returns: RficAPIHandle_t
 */

RficAPIHandle_t rfic_api_init( FR1DevType devtype )
{
    get_cmd_handle();
    FR1_LOG_INFO("rf_mdata mapped add %p\n", rf_mdata[0]);

    return &rf_mdata[0]->nx_rf_dev;
}


/*
 * rfic_api_deinit
 *
 * Input: RficAPIHandle_t xAPIHandle
 * Return: MT3812_NOERR
 *
 * Tihs API needs to be called once the API usage is complete
 */

int32_t rfic_api_deinit( RficAPIHandle_t xAPIHandle)
{
    diora_drv_close();

    return MT3812_NOERR;
}


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

int32_t rfic_adjust_pll_freq( RficAPIHandle_t xAPIHandle, uint32_t freq_khz )
{
    int32_t pll_freq_args_off[] = {0, xAPIHandle->rf_lo_freq_khz,0,0,0};
    int32_t pll_freq_args[] = {1, freq_khz,0,0,0};
    int32_t rtc = 0;
    int ret;

    rf_start_latency_calc(FR1_SW_CMD_ADJUST_PLL_FREQ);

    ret = rf_set_active(0, 0);
    if(ret != 0)
    {
        FR1_LOG_ERR("set_active api failed with return_code=%d \n",ret);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_active is success with return_code=%d\n",ret);

    ret = rf_set_path(0, 2, 0, 0, xAPIHandle->rx_bw, xAPIHandle->tx_bw);
    if(ret != 0)
    {
        FR1_LOG_ERR("set_path api failed with return_code=%d \n",ret);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_path is success with return_code=%d\n",ret);


    rtc = rf_adjust_pll_freq(pll_freq_args_off, 4);
    if(rtc != 0)
    {
        FR1_LOG_ERR("trx_pll api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("trx_pll is success with return_code=%d\n",rtc);

    rtc = rf_adjust_pll_freq(pll_freq_args, 4);
    if(rtc != 0)
    {
        FR1_LOG_ERR("trx_pll api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("trx_pll is success with return_code=%d\n",rtc);

    ret = rf_set_path(xAPIHandle->trx_path, 2, 0, 0, xAPIHandle->rx_bw, xAPIHandle->tx_bw);
    if(ret != 0)
    {
        FR1_LOG_ERR("set_path api failed with return_code=%d \n",ret);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_path is success with return_code=%d\n",ret);

    ret = rf_set_active(1, 0);
    if(ret != 0)
    {
        FR1_LOG_ERR("set_active api failed with return_code=%d \n",ret);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_active is success with return_code=%d\n",ret);


    rf_end_latency_calc(FR1_SW_CMD_ADJUST_PLL_FREQ);

    return rtc;
}


/*
 * rfic_gain_control_tx_relative_diff
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t ucGainIndB
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 */

int32_t rfic_gain_control_tx_relative_diff( RficAPIHandle_t xAPIHandle,
		int32_t ucGainIndB)
{
    rf_start_latency_calc(FR1_SW_CMD_SET_TX_GAIN);

    int32_t rtc = 0;

    rtc = rf_tx_gain_control_relative_diff(ucGainIndB);
    if(rtc != 0)
    {
        FR1_LOG_ERR("set_gain_db for Tx api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_gain_db for Tx is success with return_code=%d\n",rtc);

    rf_end_latency_calc(FR1_SW_CMD_SET_TX_GAIN);

    return MT3812_NOERR;
}


/*
 * rfic_gain_control_rx_relative_diff
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t ucGainIndB
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 */

int32_t rfic_gain_control_rx_relative_diff( RficAPIHandle_t xAPIHandle,
		int32_t ucGainIndB)
{
    rf_start_latency_calc(FR1_SW_CMD_SET_RX_GAIN);

    int32_t rtc = 0;

    rtc = rf_rx_gain_control_relative_diff(ucGainIndB);
    if(rtc != 0)
    {
        FR1_LOG_ERR("set_gain_db Rx api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_gain_db for Rx is success with return_code=%d\n",rtc);

    rf_end_latency_calc(FR1_SW_CMD_SET_RX_GAIN);

    return MT3812_NOERR;

}


/*
 * rfic_gain_set_tx_gain_idx
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  uint32_t bb_idx
 * 	  uint32_t rf_idx
 *
 * Return: rtc message
 */

int32_t rfic_gain_set_tx_gain_idx( RficAPIHandle_t xAPIHandle,
		uint32_t bb_idx, uint32_t rf_idx)
{
    rf_start_latency_calc(FR1_SW_CMD_SET_TX_GAIN_IDX);

    int32_t rtc = 0;

    rtc = rf_set_gain_idx(12, 0, bb_idx, rf_idx);
    if(rtc != 0)
    {
        FR1_LOG_ERR("set_gain_idx Tx api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_gain_idx for Tx is success with return_code=%d\n",rtc);

    rf_end_latency_calc(FR1_SW_CMD_SET_TX_GAIN_IDX);

    return rtc;
}


/*
 * rfic_gain_set_rx_gain_idx
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  uint32_t bb_idx
 * 	  uint32_t rf_idx
 *
 * Return: rtc message
 */

int32_t rfic_gain_set_rx_gain_idx(RficAPIHandle_t xAPIHandle,
		uint32_t bb_idx, uint32_t rf_idx )
{
    rf_start_latency_calc(FR1_SW_CMD_SET_RX_GAIN_IDX);

    int32_t rtc = 0;

    rtc = rf_set_gain_idx(3, 1, bb_idx, rf_idx);
    if(rtc != 0)
    {
        FR1_LOG_ERR("set_gain_idx for Rx api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("set_gain_idx for Rx is success with return_code=%d\n",rtc);

    rf_end_latency_calc(FR1_SW_CMD_SET_RX_GAIN_IDX);

    return rtc;
}


/*
 * rfic_get_tx_gain_value
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t *gain
 *
 * Return: gain value
 */

float rfic_get_tx_gain_value( RficAPIHandle_t xAPIHandle, int32_t *gain )
{
    rf_start_latency_calc(FR1_SW_CMD_GET_TX_GAIN);
    *gain = rf_mdata[0]->nx_rf_dev.tx_gain_db;
    rf_end_latency_calc(FR1_SW_CMD_GET_TX_GAIN);
    return *gain;
}


/*
 * rfic_get_rx_gain_value
 *
 * Input: RficAPIHandle_t xAPIHandle
 * 	  int32_t *gain
 *
 * Return: gain value
 */

float rfic_get_rx_gain_value( RficAPIHandle_t xAPIHandle, int32_t *gain )
{
    rf_start_latency_calc(FR1_SW_CMD_GET_RX_GAIN);
    *gain = rf_mdata[0]->nx_rf_dev.rx_gain_db;
    rf_end_latency_calc(FR1_SW_CMD_GET_RX_GAIN);
    return *gain;
}


/*
 * rfic_get_status
 *
 * Input: RficAPIHandle_t xAPIHandle
 *
 * Return: MT3812_NOERR/MT3812_ERROR
 *
 * Output: Prints the Status
 */

float rfic_get_status( RficAPIHandle_t xAPIHandle )
{
    int32_t rtc = 0;
    int ret = 0;

    rf_start_latency_calc(FR1_SW_CMD_GET_SYSSTATUS);

    printf("RF Status Local\n");
    printf("----------------\n");
    ret = rf_get_rf_status();
    if(ret != 0)
    {
        FR1_LOG_ERR("rf_get_rf_status api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("rf_get_rf_status is success with return_code=%d\n\n",rtc);

    printf("RF Status Diora\n");
    printf("----------------\n");
    rtc = rf_app_get_sysstatus();
    if(rtc != 0)
    {
        FR1_LOG_ERR("APP_get_sysstatus api failed with return_code=%d \n",rtc);
        return MT3812_ERROR;
    }
    FR1_LOG_DBG("APP_get_sysstatus is success with return_code=%d\n\n",rtc);

    rf_end_latency_calc(FR1_SW_CMD_GET_SYSSTATUS);

    printf("RF APIs Latencies\n");
    printf("--------------------------------------------------\n");
    printf("rfic_adjust_pll_freq                  - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_ADJUST_PLL_FREQ]);
    printf("rfic_gain_control_tx_relative_diff    - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_SET_TX_GAIN]);
    printf("rfic_gain_control_rx_relative_diff    - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_SET_RX_GAIN]);
    printf("rfic_gain_set_tx_gain_idx             - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_SET_TX_GAIN_IDX]);
    printf("rfic_gain_set_rx_gain_idx             - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_SET_RX_GAIN_IDX]);
    printf("rfic_get_tx_gain_value                - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_GET_TX_GAIN]);
    printf("rfic_get_tx_gain_value                - %d us\n",
    (int32_t)rf_mdata[0]->nx_rf_dev.cmd_latencies[FR1_SW_CMD_GET_RX_GAIN]);
    printf("--------------------------------------------------\n");

    return MT3812_NOERR;
}

