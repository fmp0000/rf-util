#Copyright 2021-2023 NXP
# NXP Confidential. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software.


SWIG ?= swig
SWIG_LIB ?= $(shell swig -swiglib)

TARGET= _rfif.so
MODULE = rfif
INCLUDE= -I../../interface -I../../rflib/ -I${COMMON_HEADERS_DIR}

ifeq ($(PYTHON_INCLUDE),)
PY_INCLUDE= -I/usr/include/python3.8 -I../../pyincludes
else
PY_INCLUDE=-I../../pyincludes -I${PYTHON_INCLUDE} -I${PYTHON_INCLUDE}/../
endif

all : $(TARGET)

$(TARGET):
	$(SWIG) -python $(INCLUDE) $(EXTRA_CFLAGS) $(MODULE).i
	$(CC) -O2 -fPIC -c $(EXTRA_CFLAGS) $(MODULE)_wrap.c $(INCLUDE) $(PY_INCLUDE)
	$(CC) -shared $(MODULE)_wrap.o -L../../rflib/ -lrflib -o $(TARGET)

install:
	cp ${TARGET} $(RFCTRL_FR1_DIR)/
	cp $(MODULE).py $(RFCTRL_FR1_DIR)

clean:
	rm -f *_wrap* *~ .~* rfif.py
	rm -f core
	rm -f *.o *.so
