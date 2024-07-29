# Copyright 2021-2024 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software.
#!/usr/bin/python3
from cmd import Cmd
import logging
from enum import Enum
import rfif as rfif
import unittest
import itertools
import numpy as np
import sys
from functools import reduce
import json
import inspect
import ctypes
import re
import os
import subprocess
import random as random
from textwrap import dedent

log = logging.getLogger(__name__)

def print_help():
    print(dedent('''
Usage:
fr1.py [OPTIONS] [command | filename]
No options or arguments enters into interactive mode

OPTIONS:
    -c    :    Execute given command, arguments are considered as single command
    -b    :    Execute in batch mode, argument is a filename with list of commands to run
    
./fr1.py help       : Get this help
        (or)
python3 fr1.py help       : Get this help

./fr1.py -c help    : Get all possible commands
        (or)
python3 fr1.py -c help       : Get this help
        '''))

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    if(len(arg) == 0):
        return ()
    else:
        return tuple(map(int, re.split(r'\s+', arg)))

def parsehex(arg):
    'Convert a series of zero or more hex numbers to an argument tuple'
    if(len(arg) == 0):
        return ()
    else:
        return tuple(map(lambda x:int(x,16), re.split(r'\s+', arg)))

def parsestr(arg):
    'Convert a series of zero or more strings to an argument tuple'
    if(len(arg) == 0):
        return ()
    else:
        return tuple(map(str, re.split(r'\s+', arg)))

FR1TxBw = {
    "50_MHz" : 0
    }

FR1RxBw = {
    "20_MHz" : 0,
    "25_MHz" : 1,
    "30_MHz" : 2,
    "40_MHz" : 3,
    "50_MHz" : 4
    }

FR1Channel = {
    "Tx" : 0,
    "Rx" : 1
    }

class RF_FR1_CONFIG(ctypes.Structure):
    _fields_ = [("lo_freq", ctypes.c_int),
                ("rf_cal_file", ctypes.c_char_p),
                ("path_tx", ctypes.c_ubyte),
                ("path_rx1", ctypes.c_ubyte),
                ("path_rx2", ctypes.c_ubyte),
                ("tx_bw", ctypes.c_ubyte),
                ("rx_bw", ctypes.c_ubyte),
                ("tx_gain_db", ctypes.c_int),
                ("rx_gain_db", ctypes.c_int)]

LogLevel = {
        rfif.LL_DBG : logging.DEBUG,
        rfif.LL_INFO : logging.INFO,
        rfif.LL_WARN : logging.WARNING,
        rfif.LL_ERR : logging.ERROR
        }

testlib = ctypes.cdll.LoadLibrary('_rfif.so')

def get_my_path():
    try:
        filename = __file__ # where we were when the module was loaded
    except NameError: # fallback
        filename = inspect.getsourcefile(get_my_path)
    return os.path.realpath(filename)

def load_json_file(filename):
    """load a JSON file if it exists, otherwise return empty Dict"""
    if os.path.isfile(filename):
        with open(filename) as fp:
            return json.load(fp)
    return {}


class Dio():
    def __init__(self):
        rfif.get_cmd_handle()
        logging.basicConfig(level=logging.ERROR)
    
    def FR1_DrvOpen(self, dev_type):
            return rfif.diora_drv_open_reentry(dev_type)

    def FR1_DrvClose(self):
            return rfif.diora_drv_close()

    def FR1_RF_Init(self, config):
        return testlib.fr1_rf_init(ctypes.byref(config))

    def FR1_SetTrxPll(self, pll_freq_args_struct, pll_freq_args_size):
        return testlib.rf_adjust_pll_freq(ctypes.byref(pll_freq_args_struct), pll_freq_args_size)

    def FR1_GetTrxPll(self):
            return rfif.rf_get_trx_pll()

    def FR1_SetTxBw(self, txbw_args_struct, txbw_args_size):
        return testlib.rf_set_txbw(ctypes.byref(txbw_args_struct), txbw_args_size)

    def FR1_GetTxBw(self):
            return rfif.rf_get_txbw()

    def FR1_SetRxBw(self, rxbw_args_struct, rxbw_args_size):
        return testlib.rf_set_rxbw(ctypes.byref(rxbw_args_struct), rxbw_args_size)

    def FR1_GetRxBw(self):
            return rfif.rf_get_rxbw()

    def FR1_SetActive(self, on_off, rx_path):
            return rfif.rf_set_active(on_off, rx_path)

    def FR1_SetTxRelGain(self, gain_db_change):
            return rfif.rf_tx_gain_control_relative_diff(gain_db_change)

    def FR1_SetRxRelGain(self, gain_db_change):
            return rfif.rf_rx_gain_control_relative_diff(gain_db_change)

    def FR1_SetGainIndex(self, path, channel, bbgain, rfgain):
            return rfif.rf_set_gain_idx(path, channel, bbgain, rfgain)

    def FR1_GetGainIndex(self):
            return rfif.rf_get_gain_idx()

    def FR1_SetPath(self, path, band, rssi, dpd, rx_bw, tx_bw):
            return rfif.rf_set_path(path, band, rssi, dpd, rx_bw, tx_bw)

    def FR1_GetPath(self):
            return rfif.rf_get_path()

    def FR1_TXRXSW(self, switch, on_off):
            #return rfif.diora_drv_txrx_sw(on_off)
            return

    def FR1_GetDrvVersion(self):
            return rfif.diora_drv_version()

    def FR1_SetBBLoop(self, rx_path, tx_bw, rx_bw):
            return rfif.rf_set_bbloop(rx_path, tx_bw, rx_bw)

    def FR1_SetCalPll(self, cal_pll_args_struct, cal_pll_args_size):
        return testlib.rf_set_cal_pll(ctypes.byref(cal_pll_args_struct), cal_pll_args_size)

    def FR1_GetCalPll(self):
            return rfif.rf_get_cal_pll()

    def FR1_SetRFLoop(self, rx_path, freq_band, rf_loop):
            return rfif.rf_set_rfloop(rx_path, freq_band, rf_loop)

    def FR1_GetSysStatus(self):
            return rfif.rf_app_get_sysstatus()

    def FR1_GetTemperature(self):
            return rfif.rf_app_get_temperature()

    def FR1_GetRfStatus(self):
            return rfif.rf_get_rf_status()

    def FR1_GetVersion(self):
            return rfif.diora_gen_get_version()

    def FR1_SetRegister(self, set_reg_args_struct):
        return testlib.diora_gen_set_register(ctypes.byref(set_reg_args_struct))

    def FR1_GetRegister(self, addr, length):
            return rfif.diora_gen_get_register(addr, length)

    def FR1_SetRegisterMasked(self, addr, value, mask):
            return rfif.diora_gen_set_registermasked(addr, value, mask)

    def FR1_SetProperty(self, set_prop_args_struct):
        return testlib.diora_gen_set_property(ctypes.byref(set_prop_args_struct))

    def FR1_GetProperty(self, prop, length):
            return rfif.diora_gen_get_property(prop, length)

    def FR1_Calib_Bw(self, channel, band, freq, rxbw, txbw):
            return rfif.diora_calib_bw(channel, band, freq, rxbw, txbw)

    def FR1_Calib_RxDc(self, calib_rxdc_args_struct, calib_rxdc_args_size):
        return testlib.diora_calib_rxdc(ctypes.byref(calib_rxdc_args_struct), calib_rxdc_args_size)

    def cleanup(self):
        ret = dio.FR1_DrvClose()
        print("MT3812 Handle closed")
        print("Quitting.")
        raise SystemExit

    def is_file(self, args, cmd):
        try:
            assert len(args) == 1, "Invalid number of arguments"
            assert os.path.isfile(args[0]), "Given File doesn't exist"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_devtype(self, args, cmd):
        try:
            assert len(args) == 2, "Invalid number of arguments"
            assert args[0] == 'devtype' , "parameter name (devtype) should be given"
            assert 1 <= int(args[1]) <= 2 , "Invalid value given for devtype"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_freq(self, args, cmd):
        try:
            if cmd == "set_lo_freq":
                assert 4 <= len(args) <= 8,"Invalid number of arguments"
            else:
                assert 4 <= len(args) <= 6,"Invalid number of arguments"
            assert args[0] == 'mode', "parameter name (mode) should be given"
            assert 0 <= int(args[1]) <= 1 , "Invalid value given for mode"
            assert args[2] == 'freq', "parameter name (freq) should be given"
            assert 3300000 <= int(args[3]) <= 3800000, "Frequency not in range"
            if len(args) > 4:
                assert args[4] == 'precal', "parameter name (precal) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_bw_args(self, args, cmd):
        try:
            assert 2 <= len(args) <= 5,"Invalid number of arguments"
            assert args[0] == 'bw', "parameter name (bw) should be given"
            if cmd == "set_txbw":
                assert 0 <= int(args[1]) <= 2 , "Invalid value given for tx_bw"
            else:
                assert 0 <= int(args[1]) <= 4 , "Invalid value given for rx_bw"
            if len(args) > 2:
                assert args[2] == 'precal', "parameter name (precal) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_active(self, args, cmd):
        try:
            assert len(args) == 4,"Invalid number of arguments"
            assert args[0] == 'act_mode', "parameter namei (act_mode) should be given"
            assert 0 <= int(args[1]) <= 3 , "Invalid value given for activation_mode"
            assert args[2] == 'receiver', "parameter name (receiver) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for receiver_t"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_gain_change(self, args, cmd):
        try:
            assert len(args) == 2,"Invalid number of arguments"
            assert args[0] == 'gain_db', "parameter name (gain_db) should be given"
            if cmd == "set_tx_rel_gain":
                assert -62 <= int(args[1]) <= 62 , "Invalid value given for gain_db"
            else:
                assert -42 <= int(args[1]) <= 42 , "Invalid value given for gain_db"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_gain_idx(self, args, cmd):
        try:
            assert len(args) == 8,"Invalid number of arguments"
            assert args[0] == 'path', "parameter name (path) should be given"
            assert 0 <= int(args[1]) <= 15 , "Invalid value given for path"
            assert args[2] == 'channel', "parameter name (channel) should be given"
            assert args[4] == 'bbgain', "parameter name (bbgain) should be given"
            assert args[6] == 'rfgain', "parameter name (rfgain) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_path(self, args, cmd):
        try:
            assert len(args) == 12,"Invalid number of arguments"
            assert args[0] == 'path', "parameter name (path) should be given"
            assert 0 <= int(args[1]) <= 15 , "Invalid value given for path"
            assert args[2] == 'band', "parameter name (band) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for freq_band"
            assert args[4] == 'rssi', "parameter name (rssi) should be given"
            assert 0 <= int(args[5]) <= 3 , "Invalid value given for receiver_t"
            assert args[6] == 'dpd', "parameter name (dpd) should be given"
            assert 0 <= int(args[7]) <= 5 , "Invalid value given for dpd_mode"
            assert args[8] == 'rx_bw', "parameter name (rx_bw) should be given"
            assert 0 <= int(args[9]) <= 4 , "Invalid value given for rx_bw"
            assert args[10] == 'tx_bw', "parameter name (tx_bw) should be given"
            assert int(args[11]) == 0 , "Invalid value given for tx_bw"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_bbloop_args(self, args, cmd):
        try:
            assert len(args) == 6,"Invalid number of arguments"
            assert args[0] == 'rx_path', "parameter namei (rx_path) should be given"
            assert 0 <= int(args[1]) <= 3 , "Invalid value given for rx_path"
            assert args[2] == 'tx_bw', "parameter name (tx_bw) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for tx_bw"
            assert args[4] == 'rx_bw', "parameter name (rx_bw) should be given"
            assert 0 <= int(args[5]) <= 11 , "Invalid value given for rx_bw"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_rfloop_args(self, args, cmd):
        try:
            assert len(args) == 6,"Invalid number of arguments"
            assert args[0] == 'rx_path', "parameter namei (rx_path) should be given"
            assert 0 <= int(args[1]) <= 3 , "Invalid value given for rx_path"
            assert args[2] == 'band', "parameter name (band) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for freq_band"
            assert args[4] == 'rf_loop', "parameter name (rf_loop) should be given"
            assert 0 <= int(args[5]) <= 1 , "Invalid value given for rf_loop"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def is_valid_sw(self, args, cmd):
        try:
            assert len(args) == 4, "Invalid number of arguments"
            assert args[0] == 'sw' , "parameter name (sw) should be given"
            assert 1 <= int(args[1]) <= 2 , "Invalid value given for sw"
            assert args[2] == 'on_off' , "parameter name (on_off) should be given"
            assert 0 <= int(args[3]) <= 1 , "Invalid value given for on_off"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_set_reg_args(self, args, cmd):
        try:
            assert len(args) == 11, "Invalid number of arguments"
            assert args[0] == 'addr' , "parameter name (addr) should be given"
            assert args[2] == 'values' , "parameter name (values) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_get_reg(self, args, cmd):
        try:
            assert len(args) == 4, "Invalid number of arguments"
            assert args[0] == 'addr' , "parameter name (addr) should be given"
            assert args[2] == 'length' , "parameter name (length) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_set_regmasked(self, args, cmd):
        try:
            assert len(args) == 6, "Invalid number of arguments"
            assert args[0] == 'addr' , "parameter name (addr) should be given"
            assert args[2] == 'value' , "parameter name (value) should be given"
            assert args[4] == 'mask' , "parameter name (mask) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_set_prop_args(self, args, cmd):
        try:
            assert len(args) == 11, "Invalid number of arguments"
            assert args[0] == 'property' , "parameter name (addr) should be given"
            assert args[2] == 'values' , "parameter name (values) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_get_prop(self, args, cmd):
        try:
            assert len(args) == 4, "Invalid number of arguments"
            assert args[0] == 'property' , "parameter name (property) should be given"
            assert args[2] == 'length' , "parameter name (length) should be given"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_calib_bw(self, args, cmd):
        try:
            assert len(args) == 10,"Invalid number of arguments"
            assert args[0] == 'channel', "parameter name (channel) should be given"
            assert 0 <= int(args[1]) <= 1 , "Invalid value given for channel"
            assert args[2] == 'band', "parameter name (band) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for band"
            assert args[4] == 'freq', "parameter name (freq) should be given"
            assert 6600000 <= int(args[5]) <= 7600000 , "Frequency not in range"
            assert args[6] == 'rxbw', "parameter name (rxbw) should be given"
            assert 0 <= int(args[7]) <= 11 , "Invalid value given for rxbw"
            assert args[8] == 'txbw', "parameter name (txbw) should be given"
            assert 0 <= int(args[9]) <= 3 , "Invalid value given for txbw"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_calib_rxdc(self, args, cmd):
        try:
            assert ((6 <= len(args) <= 12) & (len(args) % 2 == 0)),"Invalid number of arguments"
            assert args[0] == 'receiver', "parameter name (receiver) should be given"
            assert 0 <= int(args[1]) <= 3 , "Invalid value given for receiver"
            assert args[2] == 'band', "parameter name (band) should be given"
            assert 0 <= int(args[3]) <= 3 , "Invalid value given for band"
            assert args[4] == 'freq', "parameter name (freq) should be given"
            assert 6600000 <= int(args[5]) <= 7600000 , "Frequency not in range"
            if len(args) > 6:
                assert args[6] == 'rxbw', "parameter name (rxbw) should be given"
                assert 0 <= int(args[7]) <= 11 , "Invalid value given for rxbw"
                assert args[8] == 'txbw', "parameter name (txbw) should be given"
                assert 0 <= int(args[9]) <= 3 , "Invalid value given for txbw"
                assert args[10] == 'bbgain', "parameter name (bbgain) should be given"
                assert 0 <= int(args[11]) <= 15 , "Invalid value given for bbgain"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True


class RfPrompt(Cmd):
    prompt = ''
    def exec_cmd(self, cmd):
        """
        Executes any given command in string 
        format on the Host console
        """
        (output, errors) = subprocess.Popen("%s" % cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=True).communicate()
        if errors : 
            output = errors
            print("Error in executing Command {} \n{}".format(cmd, output.decode("utf-8")))

    def check_loglevel(self, args, cmd):
        args = parse(args)
        try:
            assert len(args) == 1, "Invalid number of arguments"
            assert 0 <= args[0] <= 3 , "Invalid value given for log level"
        except AssertionError as msg:
            print(msg)
            self.do_help(cmd)
            return False
        return True

    def emptyline(self):
        """
        Called when an empty line is entered in response to the prompt.
        If this method is not overridden, it repeats the last nonempty
        command entered.
        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')

    def do_set_log_level(self, args):
        """
        Set Log level to any of 0,1,2,3
        Usage:
            set_log_level [0|1|2|3] (0 : ERR, 1 : WARN, 2 : INFO, 3 : DBG)
        """
        if self.check_loglevel(args, 'set_log_level') :
            args = parse(args)
            rfif.rflib_set_loglevel(args[0])
            log.setLevel(LogLevel[args[0]])
            for handler in log.handlers:
                handler.setLevel(LogLevel[args[0]])

    def do_drv_open(self, args):
        """
        Initiates the MT3812 handle
        Usage:
            drv_open devtype <dev_type>
        dev_type (1 : 1T1R, 2 : 1T2R)
        """
        args = parsestr(args)

        if dio.check_devtype(args, 'drv_open') :
            ret = dio.FR1_DrvOpen(int(args[1]))

    def do_drv_close(self, args):
        """
        Closes and Free's the MT3812 handle
        Usage:
            drv_close
        """
        args = parsestr(args)

        ret = dio.FR1_DrvClose()

    def do_rf_init(self,args):
        """
        Initialises the RF card with default configuration stored in config_json file
        Usage:
            rf_init <config_file_name>
        File name should be given along with it's absolute path
        Default configuration file_name is /home/root/rf-ctrl/fr1/fr1_def_config.json
        """
        args = parsestr(args)

        if dio.is_file(args, 'rf_init'):
            conf = load_json_file(args[0])
            lo_freq_KHz = conf["lo_freq_KHz"]
            rf_cal_file_path = conf["rf_cal_file_path"]
            rf_cal_file = ctypes.c_char_p(rf_cal_file_path.encode())
            path_tx = conf["path_tx"]
            path_rx1 = conf["path_rx1"]
            path_rx2 = conf["path_rx2"]
            tx_bw = FR1TxBw[conf["tx_bw"]]
            rx_bw = FR1RxBw[conf["rx_bw"]]
            tx_gain_db = conf["tx_gain_db"]
            rx_gain_db = conf["rx_gain_db"]
            config = RF_FR1_CONFIG(lo_freq_KHz, rf_cal_file, path_tx, path_rx1, path_rx2, tx_bw, rx_bw,
                                    tx_gain_db, rx_gain_db)
            ret = dio.FR1_RF_Init(config)

    def do_set_lo_freq(self,args):
        """
        Sets to desired freq in steps of KHz
        Generic Usage :
            set_lo_freq mode <mode> freq <freq in KHz>
        Precal Usage (with Optional Parameters) :
            set_lo_freq mode <mode> freq <freq in KHz> precal <vco_sel**> <cal_cap**> <cal_current**>
        mode (0 : OFF, 1 : ON)
        Supported Frequency range (*1KHz) is 3300000 - 3800000
        """
        args = parsestr(args)

        if dio.check_freq(args, 'set_lo_freq'):
            pll_freq_args_int = [int(args[1]), int(args[3])]
            for i in range(len(args)-5) :
                pll_freq_args_int.append(int(args[i+5]) if len(args)>= (i+6) else 0)
            print(" Args passed for adjust_pll_freq command :", pll_freq_args_int ,"\n")
            pll_freq_args_struct = (ctypes.c_int * len(pll_freq_args_int))(*pll_freq_args_int)
            ret = dio.FR1_SetTrxPll(pll_freq_args_struct, len(args))
 
    def do_get_trx_pll(self, args):
        """
        Get PLL Frequency
        Usage:
            get_trx_pll
        """
        args = parsestr(args)

        ret = dio.FR1_GetTrxPll()

    def do_set_txbw(self,args):
        """
        Set the bandwidth of the specified TX path and optionally the bandwidth calibration settings.
        Generic Usage :
            set_txbw bw <tx_bw>
        Precal Usage (with Optional Parameters) :
            set_txbw bw <tx_bw> precal <bw_ftune**> <vcm_in_low**>
        tx_bw (0 : 50MHz)
        """
        args = parsestr(args)

        if dio.check_bw_args(args, 'set_txbw'):
            txbw_args_int = [int(args[1])]
            for i in range(len(args)-3) :
                txbw_args_int.append(int(args[i+3]) if len(args)>= (i+4) else 0)
            print(" Args passed for Set TxBw command :", txbw_args_int ,"\n")
            txbw_args_struct = (ctypes.c_int * len(txbw_args_int))(*txbw_args_int)
            ret = dio.FR1_SetTxBw(txbw_args_struct, len(args))
 
    def do_get_txbw(self, args):
        """
        Retrieves the bandwidth of the specified TX path
        Usage:
            get_txbw
        """
        args = parsestr(args)

        ret = dio.FR1_GetTxBw()

    def do_set_rxbw(self,args):
        """
        Set the bandwidth of the specified RX path and optionally the bandwidth calibration settings.
        Generic Usage :
            set_rxbw bw <rx_bw>
        Precal Usage (with Optional Parameters) :
            set_rxbw bw <rx_bw> precal <bw_ftune**> <bw_fcoarse**>
        rx_bw (0: 20MHz, 1 : 25MHz, 2 : 30MHz, 3 : 40MHz, 4 : 50MHz)
        """
        args = parsestr(args)

        if dio.check_bw_args(args, 'set_rxbw'):
            rxbw_args_int = [int(args[1])]
            for i in range(len(args)-3) :
                rxbw_args_int.append(int(args[i+3]) if len(args)>= (i+4) else 0)
            print(" Args passed for Set RxBw command :", rxbw_args_int ,"\n")
            rxbw_args_struct = (ctypes.c_int * len(rxbw_args_int))(*rxbw_args_int)
            ret = dio.FR1_SetRxBw(rxbw_args_struct, len(args))
 
    def do_get_rxbw(self, args):
        """
        Retrieves the bandwidth of the specified RX path
        Usage:
            get_rxbw
        """
        args = parsestr(args)

        ret = dio.FR1_GetRxBw()

    def do_set_active(self, args):
        """
        Activate the mounted transceivers in TRANSMIT or RECEIVE state
        Depending on setting of TXRX_SW, or deactivate transceivers.
        Usage:
            set_active act_mode <activation_mode> receiver <receiver_t>
        activation_mode (0 : ACT_OFF, 1 : ACT_TDD)
        receiver_t (0 : RX_NONE, 1 : RX_1, 2 : RX_2,  3 : RX_1_2)
        """
        args = parsestr(args)

        if dio.check_active(args, 'set_active'):
            ret = dio.FR1_SetActive(int((args[1])), int((args[3])))

    def do_set_tx_rel_gain(self, args):
        """
        Set Diora Relative Gain for Tx
        Usage:
            set_tx_rel_gain gain_db <+/- Gaindiff in dB>
        Range of gain values supported: [0,62]
        """
        args = parsestr(args)

        if dio.check_gain_change(args, 'set_tx_rel_gain'):
            ret = dio.FR1_SetTxRelGain(int(args[1]))

    def do_set_rx_rel_gain(self, args):
        """
        Set Diora Relative Gain for Rx
        Usage:
            set_rx_rel_gain gain_db <+/- Gaindiff in dB>
        Range of gain values supported: [0,42]
        """
        args = parsestr(args)

        if dio.check_gain_change(args, 'set_rx_rel_gain'):
            ret = dio.FR1_SetRxRelGain(int(args[1]))

    def do_set_gain_idx(self, args):
        """
        Set Diora Gain Index for Tx/Rx
        Usage:
            set_gain_idx path <path> channel <Tx/Rx> bbgain <idx> rfgain <idx>
        path (3 : RX1_RX2, 12 : TX1_TX2)
        Range of Tx gain indices supported: RF Gain [0,31]
        Range of Rx gain indices supported: BB Gain [0,15] RF Gain [0,7]
        """
        args = parsestr(args)

        if dio.check_gain_idx(args, 'set_gain_idx'):
            ret = dio.FR1_SetGainIndex(int(args[1]), FR1Channel[args[3]], int(args[5]), int(args[7]))

    def do_get_gain_idx(self, args):
        """
        Get Diora Gain Index for Tx/Rx
        Usage:
            get_gain_idx
        """
        args = parsestr(args)

        ret = dio.FR1_GetGainIndex()

    def do_set_path(self, args):
        """
        Mount or unmount the specified TRX path, inc. enable or disable of applicable regulator, also for DPD if selected
        Usage:
            set_path path <path> band <freq_band> rssi <rssi_mode> dpd <dpd_mode> rx_bw <rxbw> tx_bw <txbw>
        path (3 : RX1_RX2, 12 : TX1_TX2, 15 : RX1_RX2_TX1_TX2)
        freq_band (2 : BAND_MB)
        rssi_mode (0 : RX_NONE, 1 : RX_1, 2 : RX_2,  3 : RX_1_2)
        dpd_mode (0 : DPD_NONE, 5 : DPD_RX1_RX2)
        rxbw (0: 20MHz, 1 : 25MHz, 2 : 30MHz, 3 : 40MHz, 4 : 50MHz)
        txbw (0: 50MHz)
        """
        args = parsestr(args)

        if dio.check_path(args, 'set_path'):
            ret = dio.FR1_SetPath(int(args[1]), int(args[3]), int(args[5]), int(args[7]), int(args[9]), int(args[11]))

    def do_get_path(self, args):
        """
        Retrieves the mode of the specified TRX path and applicable regulators
        Usage:
            get_path
        """
        args = parsestr(args)

        ret = dio.FR1_GetPath()

    def do_set_bbloop(self, args):
        """
        Set Diora BB Loopback from Tx Filter Out to Rx Filter In
        Usage:
            set_bbloop rx_path <receiver_t> tx_bw <txbw> rx_bw <rxbw>
        receiver_t (0 : RX_NONE, 1 : RX_1, 2 : RX_2,  3 : RX_1_2)
        txbw (0: 50MHz)
        rxbw (0: 20MHz, 1 : 25MHz, 2 : 30MHz, 3 : 40MHz, 4 : 50MHz)
        """
        args = parsestr(args)

        if dio.check_bbloop_args(args, 'set_bbloop'):
            ret = dio.FR1_SetBBLoop(int(args[1]), int(args[3]), int(args[5]))

    def do_set_cal_pll(self,args):
        """
        Enable or disable the CALPLL (mount and activate)
        Generic Usage :
            set_cal_pll mode <mode> freq <freq in KHz>
        Precal Usage (with Optional Parameters) :
            set_cal_pll mode <mode> freq <freq in KHz> precal <cal_band**>
        mode (0 : OFF, 1 : ON)
        Supported Frequency range (*1KHz) is 3300000 - 3800000
        """
        args = parsestr(args)

        if dio.check_freq(args, 'set_cal_pll'):
            cal_pll_args_int = [int(args[1]), int(args[3])]
            cal_pll_args_int.append(int(args[5]) if len(args) == 6 else 0)
            print(" Args passed for set_cal_pll command :", cal_pll_args_int ,"\n")
            cal_pll_args_struct = (ctypes.c_int * len(cal_pll_args_int))(*cal_pll_args_int)
            ret = dio.FR1_SetCalPll(cal_pll_args_struct, len(args))

    def do_get_cal_pll(self, args):
        """
        Retrieves the mode and frequency of the CAL PLL
        Usage:
            get_cal_pll
        """
        args = parsestr(args)

        ret = dio.FR1_GetCalPll()

    def do_set_rfloop(self, args):
        """
        Set RF loopback from TXBB to LNA or from PA to RXBB
        Usage:
            set_rfloop rx_path <receiver_t> band <freq_band> rf_loop <rf_loop>
        receiver_t (0 : RX_NONE, 1 : RX_1, 2 : RX_2,  3 : RX_1_2)
        freq_band (2 : BAND_MB)
        rf_loop (0 : TXBB2RXRF, 1 : TXRF2RXBB)
        """
        args = parsestr(args)

        if dio.check_rfloop_args(args, 'set_rfloop'):
            ret = dio.FR1_SetRFLoop(int(args[1]), int(args[3]), int(args[5]))

    def do_txrx_sw(self, args):
        """
        Set TXRXSW to either Tx or Rx
        Usage:
            txrx_sw sw <1/2> on_off <0/1>
        """
        args = parsestr(args)

        if dio.is_valid_sw(args, 'txrx_sw'):
            ret = dio.FR1_TXRXSW(int(args[1]), int(args[3]))

    def do_get_sysstatus(self, args):
        """
        Get Diora Sys Status
        Usage:
            get_sysstatus
        """
        args = parsestr(args)

        ret = dio.FR1_GetSysStatus()

    def do_get_temp(self, args):
        """
        Perform a Temperature measurement
        Usage:
            get_temp
        """
        args = parsestr(args)

        ret = dio.FR1_GetTemperature()

    def do_get_rf_status(self, args):
        """
        Displays the MT3812 Current Status
        Usage:
            get_rf_status
        """
        args = parsestr(args)

        ret = dio.FR1_GetRfStatus()

    def do_get_version(self, args):
        """
        Prints Device hardware and software version
        Usage:
            get_version
        """
        args = parsestr(args)

        ret = dio.FR1_GetDrvVersion()
        ret = dio.FR1_GetVersion()

    def do_set_register(self,args):
        """
        Write value to register. Up to eight consecutive registers can be written in one command
        Usage:
            set_register addr <addr> values <val1> <val2> <val3> <val4> <val5> <val6> <val7> <val8>
        addr & val* should be given in hexadecimal format
        """
        args = parsestr(args)

        if dio.check_set_reg_args(args, 'set_register'):
            set_reg_args_int = [int(args[1],16)]
            for i in range(len(args)-3) :
                set_reg_args_int.append(int(args[i+3],16))
            print(" Args passed for set_register command :", set_reg_args_int ,"\n")
            set_reg_args_struct = (ctypes.c_int * len(set_reg_args_int))(*set_reg_args_int)
            ret = dio.FR1_SetRegister(set_reg_args_struct)
 
    def do_get_register(self, args):
        """
        Read value from start register address upto paticular length
        Usage:
            get_register addr <addr> length <length>
        addr should be given in hexadecimal format
        """
        args = parsestr(args)

        if dio.check_get_reg(args, 'get_register'):
            ret = dio.FR1_GetRegister(int(args[1],16), int(args[3]))

    def do_set_registermasked(self, args):
        """
        Perform a read-modify-write on a single register with masking.
        If a bit in the mask is set to 1, the bit will be updated.
        Usage:
            set_registermasked addr <addr> value <val> mask <mask>
        addr, val & mask should be given in hexadecimal format
        """
        args = parsestr(args)

        if dio.check_set_regmasked(args, 'set_registermasked'):
            ret = dio.FR1_SetRegisterMasked(int((args[1],16)), int(args[3],16), int(args[5],16))

    def do_set_property(self,args):
        """
        Set value of a firmware property
        Usage:
            set_property property <property_id> values <val1> <val2> <val3> <val4> <val5> <val6> <val7> <val8>
        property_id & val* should be given in hexadecimal format
        """
        args = parsestr(args)

        if dio.check_set_prop_args(args, 'set_property'):
            set_prop_args_int = [int(args[1],16)]
            for i in range(len(args)-3) :
                set_prop_args_int.append(int(args[i+3],16))
            print(" Args passed for set_property command :", set_prop_args_int ,"\n")
            set_prop_args_struct = (ctypes.c_int * len(set_prop_args_int))(*set_prop_args_int)
            ret = dio.FR1_SetProperty(set_prop_args_struct)
 
    def do_get_property(self, args):
        """
        Get the value of a firmware property
        Usage:
            get_property property <property_id> length <length>
        property_id should be given in hexadecimal format
        """
        args = parsestr(args)

        if dio.check_get_prop(args, 'get_property'):
            ret = dio.FR1_GetRegister((int(args[1],16)), int(args[3]))

    def do_calib_bw(self, args):
        """
        Does Bandwidth Calibration of Diora RF
        Usage:
            calib_bw channel <0/1> band <band> freq <freq> rxbw <rx_bw> txbw <tx_bw>
        band (2 : BAND_MB)
        Supported Frequency range (*1KHz) is 3300000 - 3800000
        rx_bw (0: 20MHz, 1 : 25MHz, 2 : 30MHz, 3 : 40MHz, 4 : 50MHz)
        tx_bw (0: 50MHz)
        """
        args = parsestr(args)

        if dio.check_calib_bw(args, 'calib_bw'):
            ret = dio.FR1_Calib_Bw(int((args[1])), int((args[3])), int((args[5])), int((args[7])), int((args[9])))

    def do_calib_rxdc(self,args):
        """
        Does RxDc Calibration of Diora RF
        Usage :
            calib_rxdc receiver <receiver_t> band <band> freq <freq> rxbw <rx_bw> txbw <tx_bw> bbgain <bb_gain>
        receiver_t (0 : RX_NONE, 1 : RX_1, 2 : RX_2,  3 : RX_1_2)
        band (2 : BAND_MB)
        Supported Frequency range (*1KHz) is 3300000 - 3800000
        rx_bw (0: 20MHz, 1 : 25MHz, 2 : 30MHz, 3 : 40MHz, 4 : 50MHz)
        tx_bw (0: 50MHz)
        Range of bb_gain supported: [0,15]
        """
        args = parsestr(args)

        if dio.check_calib_rxdc(args, 'calib_rxdc'):
            calib_rxdc_args_int = [int(args[1]), int(args[3]), int(args[5])]
            for i in range(6,len(args),2) :
                calib_rxdc_args_int.append(int(args[i+1]))
            print(" Args passed for calib_rxdc command :", calib_rxdc_args_int ,"\n")
            calib_rxdc_args_struct = (ctypes.c_int * len(calib_rxdc_args_int))(*calib_rxdc_args_int)
            ret = dio.FR1_Calib_RxDc(calib_rxdc_args_struct, len(args))
 
    def do_q(self, args):
        """Quits the program."""
        ret = dio.FR1_DrvClose()
        print("MT3812 Handle closed")
        print("Quitting.")
        raise SystemExit
    

if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR)
    dio = Dio()
    prompt = RfPrompt()
    if(len(sys.argv) == 1):
        prompt.prompt = 'rfic_fr1> '
        prompt.cmdloop('Starting FR1 prompt...')
    elif(len(sys.argv) >= 3 and sys.argv[1] == '-c'):
        prompt.onecmd(' '.join(sys.argv[2:]))
    elif(len(sys.argv) == 3 and sys.argv[1] == '-b'):
        input = open(sys.argv[2], 'rt')
        try:
            RfPrompt(stdin=input).cmdloop()
        finally:
            input.close()
    elif(len(sys.argv) == 2 and sys.argv[1] == 'help'):
        print_help()
    else:
        print('Invalid args')
        print_help()
    dio.cleanup()
