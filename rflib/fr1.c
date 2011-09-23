/*
 * Copyright 2022-2023 NXP
 */

/*
 * NXP Confidential. This software is owned or controlled by NXP and may only
 * be used strictly in accordance with the applicable license terms. By expressly accepting
 * such terms or by downloading, installing, activating and/or otherwise using
 * the software, you are agreeing that you have read, and that you agree to
 * comply with and are bound by, such license terms. If you do not agree to
 * be bound by the applicable license terms, then you may not retain,
 * install, activate or otherwise use the software.
 */

#include <stdint.h>
#include <errno.h>
#include <time.h>
#include <rfic_common.h>
#include <icw_rfic_types.h>
#include <icw_rfic_common.h>
#include <gul_host_if.h>
#include <rf_sw_cmds.h>
#include <rf_common.h>
#include <rf_init.h>
#define GEUL

int icw_get_version( uint32_t *hw_ver, uint32_t *min_ver, uint32_t *maj_ver,
        uint32_t *bld_nr)
{
    RF_API_PRESW(sw_cmd_get_vers_t, FR1_SW_CMD_GET_VER, RF_CMD_FR1_FLAGS_SWCMD);
    RF_API_SEND(sw_cmd_get_vers_t);
    GET_PARAM(hw_ver);
    GET_PARAM(min_ver);
    GET_PARAM(maj_ver);
    GET_PARAM(bld_nr);
    RF_API_END;
}

int icw_get_curdata(uint32_t *freq_khz, uint32_t *txbw, uint32_t *rxbw,
	uint8_t *txgain_idx, uint8_t *rxgain_idx,
	uint8_t *dpd_loopback, uint8_t *qec_loopback,
	uint8_t *gset_tx, uint8_t *gset_rx, int32_t *txgain_db, int32_t *rxgain_db,
	int8_t *pa_ctrl_en, int8_t *lna_ctrl_en, int8_t *txrelgain_db,
	int8_t *rxrelgain_db, uint32_t *rssi1, uint32_t *rssi2, uint32_t *rssi3,
	uint32_t *rssi4, uint8_t *agc_blocker, uint8_t *gset_rx1, uint8_t *gset_rx2,
	uint8_t *gset_rx3, uint8_t *gset_rx4)
{
    RF_FR1_Device_t *icwdata;
    icwdata = (RF_FR1_Device_t *)(&(((struct rf_host_if *)(rfdev->rfic_p))->rf_prv_mdata.rfdev_fr1));
    int32_t txgain, rxgain;

    *freq_khz = iord32( rfdev,&(icwdata->freq_khz));
    *txbw = iord32( rfdev,&(icwdata->txbw));
    *rxbw = iord32( rfdev,&(icwdata->rxbw));
    *txgain_idx = icwdata->txgain_idx;
    *rxgain_idx = icwdata->rxgain_idx;
    *dpd_loopback = icwdata->dpd_loopback;
    *qec_loopback = icwdata->qec_loopback;
    *gset_tx      = icwdata->gset_tx;
    *gset_rx      = icwdata->gset_rx;
     txgain       = iord32(rfdev, &(icwdata->txgain_db));
    *txgain_db    = txgain * 0.1;
     rxgain       = iord32(rfdev, &(icwdata->rxgain_db));
    *rxgain_db    = rxgain * 0.1;
    *pa_ctrl_en   = icwdata->pa_ctrl_en;
    *lna_ctrl_en  = icwdata->lna_ctrl_en;
    *txrelgain_db = icwdata->txrelgain_db;
    *rxrelgain_db = icwdata->rxrelgain_db;
    *rssi1        = iord32( rfdev,&(icwdata->rssi1));
    *rssi2        = iord32( rfdev,&(icwdata->rssi2));
    *rssi3        = iord32( rfdev,&(icwdata->rssi3));
    *rssi4        = iord32( rfdev,&(icwdata->rssi4));
    *agc_blocker  = icwdata->agc_blocker;
    *gset_rx1     = icwdata->gset_rx1;
    *gset_rx2     = icwdata->gset_rx2;
    *gset_rx3     = icwdata->gset_rx3;
    *gset_rx4     = icwdata->gset_rx4;
    return 0;
}

int fr1_set_qec_loopback(uint32_t qec_lpbk_en, uint32_t qec_lpbk_path,
	uint32_t tx_lo_freq, uint32_t rx_lo_freq)
{
    RF_API_PRESW(geode_qec_lpbk_en_t, FR1_SW_CMD_SET_QEC, RF_CMD_FR1_FLAGS_SWCMD);
    SET_PARAM(qec_lpbk_en);
    SET_PARAM(qec_lpbk_path);
    SET_PARAM(tx_lo_freq);
    SET_PARAM(rx_lo_freq);
    RF_API_SEND(geode_qec_lpbk_en_t);
    RF_API_END;
}

int fr1_set_dpd_loopback(uint32_t dpd_lpbk_en, uint32_t dpd_lpbk_path)
{
    RF_API_PRESW(geode_dpd_lpbk_en_t, FR1_SW_CMD_SET_DPD, RF_CMD_FR1_FLAGS_SWCMD);
    SET_PARAM(dpd_lpbk_en);
    SET_PARAM(dpd_lpbk_path);
    RF_API_SEND(geode_dpd_lpbk_en_t);
    RF_API_END;
}

int32_t fr1_rf_init(uint32_t lo_freq_khz, int32_t tx_gain_idx, int32_t rx_gain_idx, int32_t rx_path_bitmask)
{
    RF_API_PRESW(sw_cmd_set_rf_init_t, FR1_SW_CMD_SET_RF_INIT, RF_CMD_FR1_FLAGS_SWCMD);
    SET_PARAM(lo_freq_khz);
    SET_PARAM(tx_gain_idx);
    SET_PARAM(rx_gain_idx);
    SET_PARAM(rx_path_bitmask);
    RF_API_SEND(sw_cmd_set_rf_init_t);
    RF_API_END;
}
int fr1_get_ep_stats(rf_cmd_flags_t rf_type)
{
	struct fr1_ep_stats *fr1_ep_stats;
    u32  j;
    fr1_ep_stats = (&((struct rf_host_if *)(rfdev->rfic_p))->stats.fr1_ep_stats);
    printf("\n\t\t fr1_swcmdhdlr_id_doesnt_exist_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_id_doesnt_exist_ctr)));
    printf("\n\t\t fr1_swcmdhdlr_mallocfailed_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_mallocfailed_ctr)));
    printf("\n\t\t fr1_swcmdhdlr_maxerr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_maxerr_ctr)));
    printf("\n\t\t fr1_swcmdhdlr_cmdinvalid_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_cmdinvalid_ctr)));
    printf("\n\t\t fr1_swcmdhdlr_txdcant1_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_txdcant1_ctr)));
    printf("\n\t\t fr1_swcmdhdlr_txdcant2_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swcmdhdlr_txdcant2_ctr)));
    printf("\n\t\t fr1_icwswswtx__fsmgpioerr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwswswtx__fsmgpioerr_ctr)));
    printf("\n\t\t fr1_icwswswtx_setpaerr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwswswtx_setpaerr_ctr)));
    printf("\n\t\t fr1_icwswswrx_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwswswrx_rfic_err_ctr)));
    printf("\n\t\t fr1_settrxpll_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settrxpll_rfic_err_ctr)));
    printf("\n\t\t fr1_settxrelgain_minpwr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_minpwr_ctr)));
    printf("\n\t\t fr1_settxrelgain_decpwrdeltal_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_decpwrdeltal_ctr)));
    printf("\n\t\t fr1_settxrelgain_decpwrdeltah_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_decpwrdeltah_ctr)));
    printf("\n\t\t fr1_settxrelgain_maxpwr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_maxpwr_ctr)));
    printf("\n\t\t fr1_settxrelgain_incpwrdeltal_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_incpwrdeltal_ctr)));
    printf("\n\t\t fr1_settxrelgain_incpwrdeltah_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_incpwrdeltah_ctr)));
    printf("\n\t\t fr1_settxrelgain_txgseterr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_txgseterr_ctr)));
    printf("\n\t\t fr1_settxrelgain_setpaerr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxrelgain_setpaerr_ctr)));
    printf("\n\t\t fr1_setrxrelgain_outofdynpos_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxrelgain_outofdynpos_ctr)));
    printf("\n\t\t fr1_setrxrelgain_outofdynneg_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxrelgain_outofdynneg_ctr)));
    printf("\n\t\t fr1_setrxrelgain_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxrelgain_rfic_err_ctr)));
    printf("\n\t\t fr1_swreltxgain_nocmdresult_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swreltxgain_nocmdresult_ctr)));
    printf("\n\t\t fr1_swreltxgain_minout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swreltxgain_minout_ctr)));
    printf("\n\t\t fr1_swreltxgain_maxout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swreltxgain_maxout_ctr)));
    printf("\n\t\t fr1_swreltxgain_txgaingaperr_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_swreltxgain_txgaingaperr_ctr)));
    printf("\n\t\t fr1_gettxgain_invalid_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_gettxgain_invalid_ctr)));
    printf("\n\t\t fr1_relrxgain_reqignoredbyagc_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_relrxgain_reqignoredbyagc_ctr)));
    printf("\n\t\t fr1_relrxgain_minout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_relrxgain_minout_ctr)));
    printf("\n\t\t fr1_relrxgain_maxout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_relrxgain_maxout_ctr)));
    printf("\n\t\t fr1_relrxgain_invalidegi_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_relrxgain_invalidegi_ctr)));
    printf("\n\t\t fr1_getrxgain_invalid_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_getrxgain_invalid_ctr)));
    printf("\n\t\t fr1_getrssi_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_getrssi_rfic_err_ctr)));
    printf("\n\t\t fr1_settxgainidx_minout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxgainidx_minout_ctr)));
    printf("\n\t\t fr1_settxgainidx_maxout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxgainidx_maxout_ctr)));
    printf("\n\t\t fr1_settxgainidx_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_settxgainidx_rfic_err_ctr)));
    printf("\n\t\t fr1_setrxgainidx_minout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxgainidx_minout_ctr)));
    printf("\n\t\t fr1_setrxgainidx_maxout_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxgainidx_maxout_ctr)));
    printf("\n\t\t fr1_setrxgainidx_rfic_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setrxgainidx_rfic_err_ctr)));
    printf("\n\t\t fr1_setdpd_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setdpd_err_ctr)));
    printf("\n\t\t fr1_setqec_err_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_setqec_err_ctr)));
    printf("\n\t\t fr1_icwinit_mallocfailed_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_mallocfailed_ctr)));
    printf("\n\t\t fr1_icwinit_siapiopen_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapiopen_ctr)));
    printf("\n\t\t fr1_icwinit_prvIcwfemgpio_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_prvIcwfemgpio_ctr)));
    printf("\n\t\t fr1_icwinit_siapifastsynth_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapifastsynth_ctr)));
    printf("\n\t\t fr1_icwinit_siapirxtxon_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapirxtxon_ctr)));
    printf("\n\t\t fr1_icwinit_siapitxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapitxgain_ctr)));
    printf("\n\t\t fr1_icwinit_siapirxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapirxgain_ctr)));
    printf("\n\t\t fr1_icwinit_siapirxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapitxrlgain_ctr)));
    printf("\n\t\t fr1_icwinit_siapirxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwinit_siapirxrlgain_ctr)));
    printf("\n\t\t fr1_icwsetinit_siapifastsynth_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwsetinit_siapifastsynth_ctr)));
    printf("\n\t\t fr1_icwsetinit_siapitxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwsetinit_siapitxgain_ctr)));
    printf("\n\t\t fr1_icwsetinit_siapirxgain_ctr = %u \n",iord32(rfdev,&(fr1_ep_stats->fr1_icwsetinit_siapirxgain_ctr)));
    printf("\n");
    return 0;
}

int test_fr1_api(uint32_t cpuid)
{
    RF_API_PRESW(uint32_t, RF_SW_CMD_APIPLAYER, RF_CMD_FR1_FLAGS_SWCMD);
    *data = (uint32_t)cpuid;
    RF_API_SEND(uint32_t);
    RF_API_END;
}

