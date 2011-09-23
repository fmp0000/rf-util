# Copyright 2021-2023 NXP
# NXP Confidential. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software.

CONFIG_DIRS := fr1
FR1_FILES := ${PWD}/python/fr1/fr1.py
UTILS_FR1_FILES := ${PWD}/python/utils/fr1/fr1_def_config.json 

all: ${CONFIG_DIRS}
	$(foreach b, $(CONFIG_DIRS), ${MAKE} -C ${b}  all;)

clean: ${CONFIG_DIRS}
	$(foreach b, $(CONFIG_DIRS), ${MAKE} -C ${b}  clean;)

install: ${CONFIG_DIRS}
	$(foreach b, $(CONFIG_DIRS), ${MAKE} -C ${b}  install;)
ifeq ($(ENABLE_ICWINGS),1)
	cp $(FR1_FILES) $(RFCTRL_FR1_DIR)/
	cp $(UTILS_FR1_FILES) $(RFCTRL_FR1_DIR)/

else
	rm -rf $(RFCTRL_FR1_DIR)/ $(RFCTRL_UTILS_FR1_DIR)/
endif
