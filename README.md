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

### filebench

filebench consists of a set of file system related benchmarks. Important ones
are 

* web server - reads multiple files completely (simulating html file read requests) and closes the file. for each 10th file, the webserver issues a sync operation (eg. writing user data or cookie) into a log file. it would be interesting to see how filesystems behave with high "READ" and low "WRITE" (only user data being appended to a log file) workloads.
* file server - consists of high number of users, who creates, writes, opens, appends, reads and deletes files. this resembles google-drive kind of workload. Hence, this workload is both READ and WRITE intensive.
* mail server (varmail) - simulates a mail environment. small files created i.e. create, write and sync calls made. sometimes, files are read completely, marked as read, and fsynced. previously read emails are also read. Hence, there are whole reads, large writes and small intermittent writes as well.

## Installation

### filebench

https://github.com/filebench/filebench/wiki

Some pre-installation commands required:
```
aclocal
autoheader
autoconf
libtoolize
Automake --add-missing
Install flex package
```
Another reference is here: https://github.com/firnsy/yubipam/issues/1

## References

[1] Securely erasing your SSD - 
https://askubuntu.com/questions/42266/what-is-the-recommended-way-to-empty-a-ssd

[2] Importing HDD directly to QEMU device using virsh command
https://askubuntu.com/questions/144894/add-physical-disk-to-kvm-virtual-machine
https://help.ubuntu.com/community/KVM/Managing

[3] Micron Tech Report: 
https://www.micron.com/~/media/documents/products/technical-note/solid-state-storage/tnfd23_m500_smart_attributes_calc_waf.pdf
