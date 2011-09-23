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

#ifndef _FR1_ICW_H_
#define _FR1_ICW_H_

int icw_get_version( uint32_t *hw_ver, uint32_t *min_ver, uint32_t *maj_ver,
        uint32_t *bld_nr);
int icw_get_curdata(uint32_t *freq_khz, uint32_t *txbw, uint32_t *rxbw,
	uint8_t *txgain_idx, uint8_t *rxgain_idx,
	uint8_t *dpd_loopback, uint8_t *qec_loopback,
	uint8_t *gset_tx, uint8_t *gset_rx, int32_t *txgain_db, int32_t *rxgain_db,
	int8_t *pa_ctrl_en, int8_t *lna_ctrl_en, int8_t *txrelgain_db,
	int8_t *rxrelgain_db, uint32_t *rssi1, uint32_t *rssi2, uint32_t *rssi3,
	uint32_t *rssi4, uint8_t *agc_blocker, uint8_t *gset_rx1, uint8_t *gset_rx2,
	uint8_t *gset_rx3, uint8_t *gset_rx4);
int fr1_set_qec_loopback(uint32_t qec_en, uint32_t qec_path_id,
	uint32_t tx_lo_freq, uint32_t rx_lo_freq);
int fr1_set_dpd_loopback(uint32_t dpd_lpbk_en, uint32_t dpd_lpbk_path);
int32_t fr1_rf_init(uint32_t lo_freq_khz, int32_t tx_gain_idx, int32_t rx_gain_idx, int32_t rx_path_bitmask);
int fr1_get_ep_stats(rf_cmd_flags_t rf_type);
int test_fr1_api(uint32_t cpuid);
#endif
