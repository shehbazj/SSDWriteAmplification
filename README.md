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

[1] Securely erasing your SSD - 
https://askubuntu.com/questions/42266/what-is-the-recommended-way-to-empty-a-ssd

[2] Importing HDD directly to QEMU device using virsh command
https://askubuntu.com/questions/144894/add-physical-disk-to-kvm-virtual-machine
https://help.ubuntu.com/community/KVM/Managing
