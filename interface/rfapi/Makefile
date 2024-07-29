# Copyright 2024 NXP
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

ifeq ($(MT3812), 1)
INCLUDES += -I${RFLIB_DIR}
INCLUDES += -I${MT3812_API_DIR}
endif

ifeq ($(MT3812), 1)
SRCS := rf_api.c
endif

OBJS := ${SRCS:.c=.o}
ifeq ($(MT3812), 1)
OBJS += ${RFLIB_DIR}/librflib.a
endif

all: rfapi

rfapi: ${OBJS}
	${AR} -cr librfapi.a ${OBJS}

%.o: %.c
	${CC} ${CFLAGS} ${INCLUDES}  $< -o $@

clean:
	rm -rf *.o librfapi.a

install:
	cp librfapi.a ${RFAPI_FR1_DIR}/



