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

fsType=${1:-ext4}
bm=${2:-fio}

# create a file system

yes | mkfs.$fsType -f /dev/vda
mount /dev/vda /mnt

# run the benchmark from scripts folder

if [[ $bm == "fio" ]]; then
	./scripts/google_compute.sh 
	#./scripts/aws_ebs.sh
else
	echo "cmd $bm not implemented"
fi

sudo umount /mnt
