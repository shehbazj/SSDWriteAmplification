# SSDWriteAmplification

Tests for measuring the write amplification for different file systems

## Setup

Two SSDs have been used in this setup in order to perform the experiments.
The first SSD hosts a VM. the second SSD is connected as a RAW device through
QEMU's SATA interface.

Before mounting and running any benchmark, we format existing SSD using ATA
Secure erase command[1].

hdparm --user-master u --security-erase password /dev/sdc

Once the drive has been erased securely, we can export the raw device directly
to QEMU[2] by editing the libvirt .xml file and adding the disk parameter.

## Measuring Write Amplification

Number of writes done to disk are recorded using SMART counters[3]. 
This can be done using the following equation:

WAF =  1 + (delta SMART Attribute 248 / delta SMART Attribute 247)

Where 
Attribute 248 = NAND program operations initiated by the FTL layer.
Attribute 247 = NAND program operations initiated by the host.

Note that these SMART values are only shown by Micron SSDs. Samsung SSDs do
not show this value.

## Benchmarks

### fio

fio can be run with the following parameters

* --blocksize=4k 1M
* --ioengine=sync or libaio
* --direct=1 similar to O_DIRECT, this would cause reads to happen directly from disk instead of memory (default is 0 i.e. memory) (reads, not important!!)
* --fsync=0 tells linux to sync (flush data to memory) at its own convenience. (writes, important!!)
* --fio --name=randwrite --ioengine=libaio --iodepth=1 --rw=randwrite --bs=4k --direct=0 --size=512M --numjobs=8 --runtime=240 --group_reporting

We are only interested in reporting reliability related issues. We are not interested in either performance or read operations.

## References

[1] Securely erasing your SSD - 
https://askubuntu.com/questions/42266/what-is-the-recommended-way-to-empty-a-ssd

[2] Importing HDD directly to QEMU device using virsh command
https://askubuntu.com/questions/144894/add-physical-disk-to-kvm-virtual-machine
https://help.ubuntu.com/community/KVM/Managing

[3] Micron Tech Report: 
https://www.micron.com/~/media/documents/products/technical-note/solid-state-storage/tnfd23_m500_smart_attributes_calc_waf.pdf
