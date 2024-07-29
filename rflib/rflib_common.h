/*
 * Copyright 2021-2024 NXP
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

#ifndef __RFLIB_COMMON_H__
#define __RFLIB_COMMON_H__

#include <stdint.h>
#include <endian.h>
#include <stdio.h>

#define FATAL do { fprintf(stderr, "Error at line %d, file %s (%d) [%s]\n", \
  __LINE__, __FILE__, errno, strerror(errno)); exit(1); } while(0)

typedef enum rflib_ll {
    LL_ERR,
    LL_WARN,
    LL_INFO,
    LL_DBG
} rflib_ll_t;

extern rflib_ll_t rflib_fr1_log_level;

#define FR1_LOGMSG_ERR(fmt) \
    do { \
        if (rflib_fr1_log_level >= LL_ERR) { \
            printf ("[ERR] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__); \
        } \
    } while(0);
#define FR1_LOGMSG_WARN(fmt) \
    do { \
        if (rflib_fr1_log_level >= LL_WARN) { \
            printf ("[WARN] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__); \
        } \
    } while(0);

#define FR1_LOGMSG_INFO(fmt) \
    do { \
        if (rflib_fr1_log_level >= LL_INFO) { \
            printf ("[INFO] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__); \
        } \
    } while(0);
#define FR1_LOGMSG_DBG(fmt) \
    do { \
        if (rflib_fr1_log_level >= LL_DBG) { \
            printf ("[DBG] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__); \
        } \
    } while(0);



#define FR1_LOG_ERR(fmt, ...) \
    do { \
        if (rflib_fr1_log_level >= LL_ERR) { \
            printf ("[ERR] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__, __VA_ARGS__); \
        } \
    } while(0);
#define FR1_LOG_WARN(fmt, ...) \
    do { \
        if (rflib_fr1_log_level >= LL_WARN) { \
            printf ("[WARN] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__, __VA_ARGS__); \
        } \
    } while(0);

#define FR1_LOG_INFO(fmt, ...) \
    do { \
        if (rflib_fr1_log_level >= LL_INFO) { \
            printf ("[INFO] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__, __VA_ARGS__); \
        } \
    } while(0);
#define FR1_LOG_DBG(fmt, ...) \
    do { \
        if (rflib_fr1_log_level >= LL_DBG) { \
            printf ("[DBG] (%s:%s:%d) " fmt, __FILE__, __func__, __LINE__, __VA_ARGS__); \
        } \
    } while(0);

void rflib_set_loglevel(rflib_ll_t loglevel );

#endif /* __RFLIB_COMMON_H__ */

