# This should be run on the guest OS

# create a file system on /dev/vda

# select the file system among the following:

# ext4
# f2fs
# btrfs

# select the workload among the following

# fio
# tpcc
# oltp

fsType="ext4"
bm="fio"

# create a file system

mkfs.$fsType /dev/vda

# run the benchmark from scripts folder

./scripts/google_compute
./scripts/aws_ebs

