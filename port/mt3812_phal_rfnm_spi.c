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

/** @file mt3812_phal_rfnm_spi.c
 *  @brief MT3812 SDK - Physical Layer Abstraction Layer (PHAL)
 *         Dummy PHAL Functions
 *
 *  @date July 29, 2024
 *  @author Dinesh Ladi
 */

#include "mt3812_drv.h"
#include "diora_osal.h"
#include "diora_phal.h"
#include <stdio.h>

#define unused(param) param __attribute__ ((unused))

/** @fn error_t diora_phal_init_gpio(u32 gpioid, u32 pinnum, gpio_mode_t mode)
 *  @brief Configure the PIN <pinnum> of the GPIO <gpioid> in specified mode
 *  
 * @param gpioid [GPIO_1 .. GPIO_4]
 * @param pinnum
 * @param mode
 */
error_t diora_phal_init_gpio (u32 gpioid, u32 pinnum, gpio_mode_t mode)
{
	diora_osal_log(LOG_ERR, "\rdiora_phal_init_gpio() is called \n");
    return 0;
}

/** @fn error_t diora_phal_get_gpio(u32 gpioid, u32 pinnum, bool *val)
 *  @brief Get the PIN <pinnum> of the GPIO <gpioid>
 * 
 * @param gpioid [GPIO_1 .. GPIO_4]
 * @param pinnum
 * @param *val
 */
error_t diora_phal_get_gpio(u32 gpioid, u32 pinnum, bool *val)
{
	diora_osal_log(LOG_ERR, "\rdiora_phal_get_gpio() is called \n");
    return 0;
}

/** @fn error_t diora_phal_set_gpio(u32 gpioid, u32 pinnum, bool val)
 *  @brief Set the PIN <pinnum> of the GPIO <gpioid> to specified value [0, 1]
 * 
 * @param gpioid [GPIO_1 .. GPIO_4]
 * @param pinnum
 * @param val
 */
error_t diora_phal_set_gpio(u32 gpioid, u32 pinnum, bool val)
{
	diora_osal_log(LOG_ERR, "\rdiora_phal_set_gpio() is called \n");
    return 0;
}
