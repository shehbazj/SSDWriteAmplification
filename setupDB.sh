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

if [ $(id -u) -ne 0 ];
then
   echo "Please run as root";
   exit 1
fi

fsType=${1:-ext4}
bm=${2:-filebench}

# create a file system

yes | sudo mkfs.$fsType /dev/vda
#sudo mount /dev/vda /mnt

# run the benchmark from scripts folder

if [ $bm = "filebench" ]; then
else
	echo "cmd $bm not implemented"
fi

#sudo umount /mnt
