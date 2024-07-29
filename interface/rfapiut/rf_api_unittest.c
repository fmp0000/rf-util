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

#include <stdio.h>

#if 10
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/mman.h>
#endif

#include <rf_api.h>

/*
 * Test the functionality of all the RF APIs exported to L1
 * Calculate and diplay latency of RF APIs
 */

int main() {
	RficAPIHandle_t RFDevice = NULL;

	printf("---------------------------\n");
	printf("Inside RF API Test Utility\n");
	printf("---------------------------\n");

	printf("\nc_api_init test starts\n");
	printf("---------------------------\n\n");
	RFDevice = rfic_api_init(2);
	
	printf("\nrfic_adjust_pll_freq test starts\n");
	printf("--------------------------------\n\n");
	rfic_adjust_pll_freq(RFDevice, 3600000);

	printf("\nrfic_gain_control_tx_relative_diff test starts\n");
	printf("-----------------------------------------------\n\n");
	rfic_gain_control_tx_relative_diff(RFDevice, 20);

	printf("\nrfic_gain_control_rx_relative_diff test starts\n");
	printf("-----------------------------------------------\n\n");
	rfic_gain_control_rx_relative_diff(RFDevice, 20);

	printf("\nrfic_gain_set_tx_gain_idx test starts\n");
	printf("--------------------------------------\n\n");
	rfic_gain_set_tx_gain_idx(RFDevice, 0, 25);

	
	printf("\nrfic_gain_set_rx_gain_idx test starts\n");
	printf("--------------------------------------\n\n");
	rfic_gain_set_rx_gain_idx(RFDevice, 1, 5);


	printf("\nrfic_get_status test starts\n");
	printf("--------------------------------\n\n");
	rfic_get_status(RFDevice);

	printf("\nrfic_api_deinit test starts\n");
	printf("---------------------------\n\n");
	rfic_api_deinit(RFDevice);

	printf("\nrfic_adjust_pll_freq test ends\n");
}
