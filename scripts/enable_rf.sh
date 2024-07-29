# Copyright 2024-2025 NXP
# NXP Proprietary. This software is owned or controlled by NXP and may only
# be used strictly in accordance with the applicable license terms. By expressly accepting
# such terms or by downloading, installing, activating and/or otherwise using
# the software, you are agreeing that you have read, and that you agree to
# comply with and are bound by, such license terms. If you do not agree to
# be bound by the applicable license terms, then you may not retain,
# install, activate or otherwise use the software. 
#!/bin/sh

gpioget 2 9
gpioget 2 14
 
gpioset 0 1=1

#lspci -vv | grep Addr
#echo 1 > /sys/bus/pci/devices/0000\:01\:00.0/remove
#sleep 1
#lspci
#echo "1" > /sys/bus/pci/rescan
 
lspci -vv | grep Addr
 
echo 7 > /proc/sys/kernel/printk
unlink /home/root/backing_storage
dd if=/dev/zero of=/home/root/backing_storage bs=1M count=64
cd ~/fr1_fr2_test_tool
echo $1
./boot_vspa.sh rc30
cd ..
insmod /lib/modules/$(uname -r)/extra/sdr_gpio.ko
insmod /lib/modules/$(uname -r)/extra/sdr_lalib.ko
insmod /lib/modules/$(uname -r)/extra/sdr_daughterboard.ko
 
sleep 1
 
insmod /lib/modules/$(uname -r)/extra/sdr_mt3812.ko
echo -n "sdr_m7_v0.elf" > /sys/class/remoteproc/remoteproc0/firmware
echo stop > /sys/class/remoteproc/remoteproc0/state
echo start > /sys/class/remoteproc/remoteproc0/state
memtool 0x303D0968=0xff
 
echo 1 > /sys/kernel/rfnm_primary/tx0/reset
