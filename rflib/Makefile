# Copyright 2021-2024 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software.

ifeq ($(ARCH), "powerpc")
CFLAGS  += -c -msoft-float
else
CFLAGS  += -c -fPIC
endif

CFLAGS += -Wall -Wno-address-of-packed-member -Wno-unused-variable

INCLUDES += -I${INTERFACE_DIR}
ifeq ($(MT3812), 1)
INCLUDES += -I${MT3812_API_DIR}
INCLUDES += -I${MT3812_FIRMWARE_DIR}
INCLUDES += -I${PORT_DIR}
INCLUDES += -I${MT3812_LIB_DIR}
INCLUDES += -I${FR1_SPI_INTERFACE_DIR}
INCLUDES += -I${LA9310_COMMON_HEADERS}
endif

SRCS := rflib_common.c

ifeq ($(MT3812), 1)
SRCS += fr1.c
SRCS += ${MT3812_FIRMWARE_DIR}/fw_init_mem_R2_7_001.c ${MT3812_FIRMWARE_DIR}/fw_prog_mem_R2_7_001.c
SRCS += ../port/mt3812_phal_rfnm_spi.c ../port/mt3812_osal_rfnm.c ../port/mt3812_l1al_rfnm.c
endif

OBJS := ${SRCS:.c=.o}
ifeq ($(MT3812), 1)
OBJS += ${MT3812_LIB_DIR}/libdiora-aarch64.a
OBJS += ${FR1_SPI_INTERFACE_DIR}/libecspi.a
endif

ifeq ($(MT3812), 1)
SRCS1 += ../port/mt3812_phal_rfnm_spi.c ../port/mt3812_osal_rfnm.c ../port/mt3812_l1al_rfnm.c
endif

OBJS1 := ${SRCS1:.c=.o}


all: rflib phallib

rflib: ${OBJS}
	${AR} -cr librflib.a ${OBJS}

phallib: ${OBJS1}
	${AR} -cr libphallib.a ${OBJS1}

%.o: %.c
	${CC} ${CFLAGS} ${INCLUDES}  $< -o $@

clean:
	rm -rf *.o ${MT3812_FIRMWARE_DIR}/*.o ../port/*.o librflib.a libphallib.a

install:
	cp librflib.a ${RFCTRL_FR1_DIR}/



