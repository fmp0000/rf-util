#Copyright 2021-2023 NXP
# NXP Confidential. This software is owned or controlled by NXP and may only
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

CFLAGS += -Wall -Werror -Wno-address-of-packed-member -Wno-unused-variable

INTERFACE_DIR = ../interface/
INCLUDES += -I${INTERFACE_DIR}
INCLUDES += -I${COMMON_HEADERS_DIR}

SRCS := rf_init.c rf_common.c rflib_common.c rflib_cmd.c

# Currently not including fr1_test.c for ICEWINGS
ifeq ($(ICEWINGS), 1)
SRCS += fr1.c
endif

OBJS := ${SRCS:.c=.o}

all: rflib

rflib: ${OBJS}
	${AR} -cr librflib.a ${OBJS}

%.o: %.c
	${CC} ${CFLAGS} ${INCLUDES}  $< -o $@

clean:
	rm -rf *.o librflib.a

install:
	cp librflib.a ${RFCTRL_FR1_DIR}/



