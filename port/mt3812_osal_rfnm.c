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

/** @file mt3812_osal_rfnm.c
 *  @brief MT3812 SDK - Operating System Abstraction Layer (OSAL)
 *         OSAL Functions
 *
 *  @date July 29, 2024
 *  @author Dinesh Ladi
 */


#include "diora_osal.h"

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <time.h>
#include <errno.h>

#include<string.h>

#include <stdint.h>
#include <fr1.h>

#define unused(param) param __attribute__ ((unused))

/* msleep(): Sleep for the requested number of milliseconds. */
int msleep(long msec)
{
    struct timespec ts;
    int res;

    if (msec < 0)
    {
        errno = EINVAL;
        return -1;
    }

    ts.tv_sec = msec / 1000;
    ts.tv_nsec = (msec % 1000) * 1000000;

    do {
        res = nanosleep(&ts, &ts);
    } while (res && errno == EINTR);

    return res;
}

void diora_osal_init()
{

}

/** @fn void diora_osal_udelay(int usec)
 *  @brief Wait usec microseconds.
 *  This function will be blocking and used for shorter intervals (< 1 ms)
 * 
 * @param usec
 * 
*/
void diora_osal_udelay(int usec)
{
    int t = usec*1000;
    struct timespec start,end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    while(1){
        clock_gettime(CLOCK_MONOTONIC,&end);
        if(end.tv_sec -start.tv_sec > 0 || end.tv_nsec - start.tv_nsec >= t)
            break;
    }
    return;
}

/** @fn void diora_osal_sleep(int usec)
 *  @brief Pause usec microseconds.
 *  This function will pend and used for longer intervals (> 1 ms)
 * 
 * @param ostick
 * 
*/
void diora_osal_sleep(int usec)
{
	int msec = (usec+999)/1000;
    msleep(msec);
    return;
}

/** @fn void diora_osal_wmb()
 *  @brief Guarantee ordering in write operation (wmb = write memory barrier)
 * 
 * This function inserts hardware memory barriers in the compiled instruction flow. 
 * Also it is platform dependent.
 * 
*/
void diora_osal_wmb()
{
    __sync_synchronize();
    return;
}

/** @fn void diora_osal_log(log_t type, char* format, ... )
 *  @brief Format the output of a stdarg argument list.
 * 
 * This function can be called with a varying number of arguments
 * of varying types.  
 * The include file <stdarg.h> declares a type va_list and defines 
 * macros for stepping through a list of arguments whose number and 
 * types are not known to the called function.
 * 
 * @param type
 * @param format
 * @param ...
 * 
 */
#define LOG_LEVEL	LOG_ERR   // LOG_VER (1) LOG_ERR (2)

void diora_osal_log(log_t type, char *format, ... )
{
    if (type >= LOG_LEVEL) {
        va_list  ap;
        char buf[1024];
        int  result ;
        va_start(ap, format);
        result = vsnprintf(buf, sizeof(buf), format, ap);
        va_end(ap);
        printf("[MT3812- res %d]%s ",result,buf);
        return;
    }
}

/** @fn void diora_osal_exit(int status)
 *  @brief Cause normal process termination
 * 
 * @param status
 * 
 */
void diora_osal_exit(int status)
{
    exit(0);
}

/** @fn void *diora_osal_malloc(int size)
 *  @brief Allocate size bytes and returns a pointer to the allocated memory.
 * 
 * The memory is not initialized.  If size is 0, then returns either NULL, 
 * or a unique pointer value that can later be successfully passed to free().
 * 
 * @param size
 * 
 */
void *diora_osal_malloc(int size)
{
	diora_osal_log(LOG_ERR, "Malloc is done for metanoia struct of size %d bytes\n", size);
	diora_osal_log(LOG_ERR, "Returning adddress of mt_mdata  %p, size 0x%x\n", &(rf_mdata[0]->mt_mdata), sizeof(struct mt_mdata));
	memset((uint8_t *) &(rf_mdata[0]->mt_mdata),0, sizeof(struct mt_mdata));
	return (void *) &(rf_mdata[0]->mt_mdata);
}

/** @fn void diora_osal_free(void* ptr)
 *  @brief Free the memory space pointed to by ptr.
 * 
 * ptr must have been returned by a previous call to malloc().
 * Otherwise, or if free(ptr) has already been called before, 
 * undefined behavior occurs.  If ptr is NULL, no operation is performed.
 * 
 * @param *ptr
 * 
 */
void diora_osal_free(void *ptr)
{
    //As we are dealing with scratch_buf, No need to free any pointers;
    return;
}
