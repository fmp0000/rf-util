# Copyright 2021-2023 NXP
# NXP Confidential. This software is owned or controlled by NXP and may only
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
        return tuple(map(int, arg.split(' ')))

def parsehex(arg):
    'Convert a series of zero or more hex numbers to an argument tuple'
    if(len(arg) == 0):
        return ()
    else:
        return tuple(map(lambda x:int(x,16),arg.split(" ")))

def parsestr(arg):
    'Convert a series of zero or more strings to an argument tuple'
    if(len(arg) == 0):
        return ()
    else:
        return tuple(map(str, arg.split(' ')))

LogLevel = {
        rfif.LL_DBG : logging.DEBUG,
        rfif.LL_INFO : logging.INFO,
        rfif.LL_WARN : logging.WARNING,
        rfif.LL_ERR : logging.ERROR
        }

IcwTrxStr = {
        "tx" : rfif.eFR1TX,
        "rx" : rfif.eFR1RX,
        "trx" : rfif.eFR1TRX,
}

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

class IcwCommon():
    def __init__(self):
        pass

    def FR1_SetTrxPll(self, freq_khz):
            return rfif.rf_adjust_pll_freq(freq_khz, rfif.RF_CMD_FR1_FLAGS_SWCMD)

    def FR1_SwitchRx(self):
            return rfif.rf_switch_rx(rfif.RF_CMD_FR1_FLAGS_SWCMD)
    
    def FR1_SwitchTx(self):
            return rfif.rf_switch_tx(rfif.RF_CMD_FR1_FLAGS_SWCMD)

    def FR1_TxGainIndex(self, idx):
            return rfif.rf_gain_set_tx_gain_idx(idx, rfif.RF_CMD_FR1_FLAGS_SWCMD)

    def FR1_RxGainIndex(self, gset, rx_path_bitmask):
            return rfif.rf_gain_set_rx_gain_idx(gset, rx_path_bitmask,rfif.RF_CMD_FR1_FLAGS_SWCMD)

    def Rf_Get_FR1_stats(self):
        rfif.rf_get_ep_stats(rfif.RF_CMD_FR1_FLAGS_SWCMD)
        rfif.fr1_get_ep_stats(rfif.RF_CMD_FR1_FLAGS_SWCMD)
        return

    def Rf_Get_trace_stats(self):
        rfif.rf_get_trace_stats(rfif.RF_CMD_FR1_FLAGS_SWCMD)
        return

    def FR1_TxRelGain(self, gain_change):
            return rfif.rf_gain_control_tx_relative_diff(gain_change,rfif.RF_CMD_FR1_FLAGS_SWCMD)

    def FR1_RxRelGain(self, gain_change):
            return rfif.rf_gain_control_rx_relative_diff(gain_change,rfif.RF_CMD_FR1_FLAGS_SWCMD)

class Icw():
    def __init__(self):
        rfif.rflib_set_loglevel(rfif.LL_ERR)
        logging.basicConfig(level=logging.ERROR)
        ret = rfif.common_rf_init()
        if ret:
            log.error("RFDev init failed")
            return None
    
    
    def FR1_SetQecLoopback(self, qec_lpbk_en, qec_lpbk_path, tx_lo_freq, rx_lo_freq):
        return rfif.fr1_set_qec_loopback(qec_lpbk_en, qec_lpbk_path, tx_lo_freq, rx_lo_freq)

    def FR1_SetDPDLoopback(self, dpd_lpbk_en, dpd_lpbk_path):
        return rfif.fr1_set_dpd_loopback(dpd_lpbk_en, dpd_lpbk_path)

    def API_GetVersion(self):
        return rfif.icw_get_version()
    
    def API_GetCurData(self):
        return rfif.icw_get_curdata()
    
    def check_freq(self, args, cmd):
        try:
            assert len(args) == 2,"Invalid number of arguments"
            assert args[0] == 'freq', "parameter name should be given"
            assert 3300000 <= int(args[1]) <= 3700000, "Frequency not in range"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_tx_gain_idx(self, args, cmd):
        try:
            assert len(args) == 2,"Invalid number of arguments"
            assert args[0] == 'idx', "parameter name should be given"
            assert 0 <= int(args[1]) <= 62, "Gain not in range"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_tx_gain_change(self, args, cmd):
        try:
            assert len(args) == 2,"Invalid number of arguments"
            assert args[0] == 'gain_change', "parameter name should be given"
            assert abs(float(args[1])) <= 62 ,"Input gain not in valid range"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_rx_gain_change(self, args, cmd):
        try:
            assert len(args) == 2,"Invalid number of arguments"
            assert args[0] == 'gain_change', "parameter name should be given"
            assert abs(float(args[1])) <= 64 ,"Input gain not in valid range"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_rx_gain_idx(self, args, cmd):
        try:
            assert len(args) == 4,"Invalid number of arguments"
            assert args[0] == 'gset', "parameter name should be given"
            assert 0 <= int(args[1]) <= 64, "gset not in range"
            assert args[2] == 'rx_path_bitmask', "parameter name should be given"
            assert 0 <= int(args[3]) <= 15, "Rx Path Bitmask not in range"
        except Exception as e:
            print(e)
            prompt.do_help(cmd)
            return False
        return True

    def check_gain(self, args, cmd):
        try:
           assert len(args) == 2,"Invalid number of arguments"
           assert args[0] == 'gain_change', "parameter name should be given"
           if cmd == "tx_rel_gain":
                assert abs(float(args[1])) <= 62 ,"Input gain not in valid range"
           else:
                assert abs(float(args[1])) <= 64 ,"Input gain not in valid range"
        except Exception as e:
           print(e)
           prompt.do_help(cmd)
           return False
        return True

    def check_qec_lpbk_args(self, args, cmd):
        try:
           assert len(args) == 8,"Invalid number of arguments"
           assert args[0] == 'enable', "Invalid syntax: parameter enable"
           assert args[2] == 'path_id', "Invalid syntax: parameter path_id"
           assert args[4] == 'tx_lo_freq', "Invalid syntax: parameter tx_lo_freq"
           assert args[6] == 'rx_lo_freq', "Invalid syntax: parameter rx_lo_freq"
           assert 3300000 <= int(args[5]) <= 3700000, "Tx Frequency not in range"
           assert 3300000 <= int(args[7]) <= 3700000, "Rx Frequency not in range"
        except Exception as e:
           print(e)
           prompt.do_help(cmd)
           return False
        return True

    def check_dpd_lpbk_args(self, args, cmd):
        try:
           assert len(args) == 4,"Invalid number of arguments"
           assert args[0] == 'enable', "Invalid syntax: parameter enable"
           assert args[2] == 'path_id', "Invalid syntax: parameter path_id"
        except Exception as e:
           print(e)
           prompt.do_help(cmd)
           return False
        return True

    def FR1_RF_Init(self, lo_freq_khz, tx_gain_idx, rx_gain_idx,rx_path_bitmask):
        return rfif.fr1_rf_init(lo_freq_khz, tx_gain_idx, rx_gain_idx,rx_path_bitmask)

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

    def do_set_lo_freq(self,args):
        """Sets to desired freq in KHz
        Usage :
        set_lo_freq freq <freq in KHz>
        Supported Frequency range (KHz) is 3300000 - 3700000
        """
        args = parsestr(args)

        if icw.check_freq(args, 'set_lo_freq'):
            ret = commonicw.FR1_SetTrxPll(int(args[1]))
    
    def do_get_rf_stats(self, args):
        """
        Displays the FR1 EP Stats

        Usage: get_rf_stats
        """
        ret = commonicw.Rf_Get_FR1_stats()

    def do_get_trace(self, args):
        """
        Dump all the Core traces to file

        Usage: get_trace
        """
        ret = commonicw.Rf_Get_trace_stats()

    def do_switch_tx(self, args):
        """
        Set the TXRx_SW to Tx

        Usage: switch_tx
        """

        """
        Sets DAC to idle mode
        """
        cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh;cd -"
        self.exec_cmd(cmd)
        ret = commonicw.FR1_SwitchTx()
        """
        Recovers DAC's previous state
        """
        cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh 0 1;cd -"
        self.exec_cmd(cmd)
    def do_switch_rx(self, args):
        """
        Set the TXRx_SW to Rx

        Usage: switch_rx
        """
        cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh;cd -"
        self.exec_cmd(cmd)
        ret = commonicw.FR1_SwitchRx()
        cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh 0 1;cd -"
        self.exec_cmd(cmd)

    def do_set_tx_gain_idx(self, args):
        """
        Set Icw Tx Gain Index
        Usage:
        set_tx_gain_idx idx <Gain Index>
        Range of gain indices supported:
            Gain in 0 to 48
        """
        args = parsestr(args)

        if icw.check_tx_gain_idx(args, 'set_tx_gain_idx'):
            ret = commonicw.FR1_TxGainIndex(int(args[1]))

    def do_tx_rel_gain(self, args):
        """
        Set Icw Tx Relative Gain
        Usage:
        tx_rel_gain gain_change <+/- Gain diff(dB)>
        Range of gain values supported:
            Gain diff(dB) in -62 to 62
        """
        args = parsestr(args)

        if icw.check_tx_gain_change(args, 'tx_rel_gain'):
            cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh;cd -"
            self.exec_cmd(cmd)
            ret , tx_gain_return_code = commonicw.FR1_TxRelGain(int((float(args[1]))))
            print("FR1 Tx Rel Gain Change ", args[1])
            print("FR1 Tx Gain Return Code ", tx_gain_return_code)
            cmd="cd /appdata/fr1_fr2_test_tool/; ./channels_act_tx.sh 0 1;cd -"
            self.exec_cmd(cmd)


    def do_rx_rel_gain(self, args):
        """
        Set Icw Rx Relative Gain
        Usage:
        rx_rel_gain gain_change <+/- Gain diff(dB)>
        Range of gain values supported:
            Gain diff(dB) in -64 to 64
        """
        args = parsestr(args)

        if icw.check_rx_gain_change(args, 'rx_rel_gain'):
            ret = commonicw.FR1_RxRelGain(int((float(args[1]))))
            print("FR1 Rx Rel Gain Change ", args[1])

    def do_set_rx_gain_idx(self, args):
        """
        Set Icw Set Rx Gain Idx
        Usage:
        set_rx_gain_idx gset <gset value> rx_path_bitmask <bitmask value>
        Range of rx gset values supported:
            Gain diff(dB) in 0 to 64
        Range of rx path bitmask values supported:
            Gain diff(dB) in 0 to 15
        """
        args = parsestr(args)

        if icw.check_rx_gain_idx(args, 'set_rx_gain_idx'):
            ret = commonicw.FR1_RxGainIndex(int(args[1]),int(args[3]))
            print("FR1 gSet Rx Value ", args[1])
            print("FR1 Rx Path Bitmask", args[3])

    def do_set_qec_loopback(self, args):
        """
        Set Tx-Rx QEC loopback
        Usage:
	set_qec_loopback enable <en/dis> path_id <path_id> tx_lo_freq <tx_freq> rx_lo_freq <rx_freq>
	enable options:
	    en or dis
        path_id supported:
	    tx1_rx1 or tx2_rx2
	tx_lo_freq:
	    3645000
	rx_lo_freq:
	    3600000
        """
        args = parsestr(args)

        if icw.check_qec_lpbk_args(args, 'set_qec_loopback'):
            if args[1] == 'en':
               qec_lpbk_en = 1
            elif args[1] == 'dis':
               qec_lpbk_en = 0
            else:
               print("Incorrect value for argument 'enable'")

            if args[3] == 'tx1_rx1':
               qec_lpbk_path = 1
            elif args[3] == 'tx2_rx2':
               qec_lpbk_path = 2
            else:
               print("Incorrect value for argument 'path_id'")

            icw.FR1_SetQecLoopback(int(qec_lpbk_en), int(qec_lpbk_path), int(args[5]), int(args[7]))
            print("QEC Loopback is set for path: ", args[3])

    def do_set_dpd_loopback(self, args):
        """
        Set Tx-Rx DPD loopback
        Usage:
	set_dpd_loopback enable <en/dis> path_id <path_id>
	enable options:
	    en or dis
        path_id supported:
	    tx1_rx1 or tx2_rx2
        """
        args = parsestr(args)

        if icw.check_dpd_lpbk_args(args, 'set_dpd_loopback'):
            if args[1] == 'en':
               dpd_lpbk_en = 1
            elif args[1] == 'dis':
               dpd_lpbk_en = 0
            else:
               print("Incorrect value for argument 'enable'")

            if args[3] == 'tx1_rx1':
               dpd_lpbk_path = 1
            elif args[3] == 'tx2_rx2':
               dpd_lpbk_path = 2
            else:
               print("Incorrect value for argument 'path_id'")

            icw.FR1_SetDPDLoopback(int(dpd_lpbk_en), int(dpd_lpbk_path))
            print("DPD Loopback is set for path: ", args[3])

    def do_test_fr1api(self, args):
        """ Test FR1 APIs on the specified Core
            Ex: test_fr1api 0
            Ex: test_fr1api 5
        """
        args = parse(args)
        assert 0 <= args[0] <= 5 , "Valid core are (0-5)"
        ret = rfif.test_fr1_api(args[0])
    
    def do_ver(self, args):
        """Get ICW version
        Usage : 
        ver    (Displays ICW version) """
        ret, hw_ver, min_ver, maj_ver, bld_nr = icw.API_GetVersion()
        print("ICW Version Details ")
        print(" HW Version       :" + str(hex(hw_ver)))
        print(" SW Major Version :" + str(maj_ver))
        print(" SW Minor Version :" + str(min_ver))
        print(" SW Build nr      :" + str(hex(bld_nr)))
    
    def do_info(self, args):
        """Dumps ICW Information
        Usage : 
        info    (Displays ICW Info) """

        ret, freq_khz, txbw, rxbw, txgain_idx, rxgain_idx, dpd_loopback, qec_loopback,gset_tx, gset_rx, txgain_db, rxgain_db, pa_ctrl_en, lna_ctrl_en, txrelgain_db, rxrelgain_db , rssi1, rssi2, rssi3, rssi4, agc_blocker, gset_rx1, gset_rx2, gset_rx3, gset_rx4 = icw.API_GetCurData()
        print("FR1(ICW) INFO")
        print("    --- Version ---")
        prompt.do_ver([])
        print("    --- Frequency ---")
        print("  Frequency : " + str(freq_khz) + "Khz") #tx or rx
        print("    --- Bandwidths ---")
        print("  TxBw(Khz) : " + str(txbw))
        print("  RxBw(Khz) : " + str(rxbw))
        print("    --- Gains---")
        print("  Tx Gain in dBm   : " + str(txgain_db))
        print("  Rx Gain in dB    : " + str(rxgain_db))
        print("  Tx gSet Value    : " + str(gset_tx))
        print("  Rx gSet Value    : " + str(gset_rx))
        print("  PA Status        : " + str(pa_ctrl_en))
        print("  PreDriver Status : " + str(lna_ctrl_en))
        print("  RX1 RSSI Value   : " + str(rssi1))
        print("  RX2 RSSI Value   : " + str(rssi2))
        print("  RX3 RSSI Value   : " + str(rssi3))
        print("  RX4 RSSI Value   : " + str(rssi4))
        print("  AGCBlocker Status: " + str(agc_blocker))
        print("  RX1 Path gSet    : " + str(gset_rx1))
        print("  RX2 Path gSet    : " + str(gset_rx2))
        print("  RX3 Path gSet    : " + str(gset_rx3))
        print("  RX4 Path gSet    : " + str(gset_rx4))
        print("    --- Loop Backs---")
        print("  DPD Loopback : " + "Disabled" if dpd_loopback == 0 else "Enabled")
        print("  QEC Loopback : " + "Disabled" if qec_loopback == 0 else "Enabled")

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
        """Called when an empty line is entered in response to the prompt.

        If this method is not overridden, it repeats the last nonempty
        command entered.

        """
        if self.lastcmd:
            self.lastcmd = ""
            return self.onecmd('\n')
        
    def do_loglevel(self, args):
        """ Set Log level to any of 0,1,2,3
        Usage:
            loglevel [0|1|2|3] (0 : ERR, 1 : WARN, 2 : INFO, 3 : DBG)"""
        if self.check_loglevel(args, 'loglevel') :
            args = parse(args)
            rfif.rflib_set_loglevel(args[0])
            log.setLevel(LogLevel[args[0]])
            for handler in log.handlers:
                handler.setLevel(LogLevel[args[0]])

    def do_cmdloglevel(self, args):
        """ Set host commands Log level to any of 0,1,2,3
        Usage:
            loglevel [0|1|2|3] (0 : ERR, 1 : WARN, 2 : INFO, 3 : DBG)"""
        if self.check_loglevel(args, 'cmdloglevel') :
            args = parse(args)
            rfif.rflib_set_cmdloglevel(args[0])

    def do_modinfo(self, args):
        "prints all pci devices available"
        rfif.print_modinfo()

    def do_rf_init(self,args):
        args = parsestr(args)
        curr_path = get_my_path()
        parent_path = reduce(lambda x, f: f(x), [os.path.dirname]*2, curr_path)
        assert args[0] == "fr1_def_config.json" , "wrong config file given"
        req_path = os.path.join(parent_path,"fr1", "fr1_def_config.json")
        conf = load_json_file(req_path)
        lo_freq_khz = conf["lo_freq_khz"]
        tx_gain_idx = conf["tx_gain_idx"]
        rx_gain_idx = conf["rx_gain_idx"]
        rx_path_bitmask = conf["rx_path_bitmask"]
        cal_data = conf["cal_data"]
        script_file_path = os.path.join(parent_path, "fr1", "cal_reader")
        cmd = " cd {};sh cal_reader.sh {}".format(script_file_path,cal_data)
        (output, errors) = subprocess.Popen("%s" % cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).communicate()
        if output == b'': output = errors
        print(output.decode("utf-8"))
        ret = icw.FR1_RF_Init(lo_freq_khz, tx_gain_idx, rx_gain_idx,rx_path_bitmask)
                
    def do_get_socver(self, args):
        "Get SOC version of given modem valid modem id range 0-3"
        modid = 0
        if len(args) != 0:
            modid = int (args[0])
        rfif.get_socver(modid)
    
    def do_q(self, args):
        """Quits the program."""
        print("Quitting.")
        rfif.common_rf_deinit()
        raise SystemExit
    
    def do_EOF(self, args):
        return True

if __name__ == '__main__':
    rfif.rflib_set_loglevel(rfif.LL_ERR)
    logging.basicConfig(level=logging.ERROR)
    icw = Icw()
    commonicw = IcwCommon()
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
