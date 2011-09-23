# Copyright 2021-2023 NXP
# NXP Confidential. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software.

.ONESHELL:

CC = $(CROSS_COMPILE)gcc
AR = $(CROSS_COMPILE)ar

ABERDEEN ?= 0
#KERNEL_DIR ?=/home/nxa19341/data/work/5g/cpe/geul_linux_ls1046a
DEST_DIR ?= ${PWD}/install
BIN_DIR ?= ${DEST_DIR}/usr/bin
LIB_DIR ?= ${DEST_DIR}/usr/lib
HOME_DIR ?= ${DEST_DIR}/home/root
RFCTRL_FR1_DIR ?= ${DEST_DIR}/home/root/rf-ctrl/fr1
RFCTRL_UTILS_FR1_DIR ?= ${DEST_DIR}/home/root/rf-ctrl/utils/fr1
INTERFACE_DIR := ${PWD}/interface
PYTHON_PACKAGES_DIR ?= ${DEST_DIR}/usr/lib/python3.6/site-packages
INCLUDES += -I${INTERFACE_DIR}/
INCLUDES += -I${PWD}/rflib/
INCLUDES += -I${COMMON_HEADERS_DIR}

#CFLAGS += -DDEBUG
CFLAGS += -Wall -O0 -g -D__RFIC

ifeq ($(ICEWINGS), 1)
EXTRA_CFLAGS += -DICEWINGS
ENABLE_ICWINGS ?= 1
endif

CFLAGS += $(EXTRA_CFLAGS)
export CC BIN_DIR LIB_DIR CONFIG_DIR RFCTRL_FR1_DIR RFCTRL_UTILS_FR1_DIR
export INTERFACE_DIR KERNEL_DIR COMMON_HEADERS_DIR
export INCLUDES CFLAGS ABERDEEN EXTRA_CFLAGS
export ENABLE_ICWINGS

DIRS := rflib python

all: ${DIRS}
	$(foreach b, $(DIRS), ${MAKE} -C ${b}  all;)

clean: ${DIRS}
	$(foreach b, $(DIRS), ${MAKE} -C ${b}  clean;)
	rm -rf ${DEST_DIR}

install: ${DIRS}
	mkdir -p ${BIN_DIR} ${LIB_DIR} ${CONFIG_DIR} ${PYTHON_PACKAGES_DIR} ${HOME_DIR} ${RFCTRL_FR1_DIR} $(RFCTRL_UTILS_FR1_DIR);
	$(foreach b, $(DIRS), ${MAKE} -C ${b}  install;)

release: ${DIRS}
