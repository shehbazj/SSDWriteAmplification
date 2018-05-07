# master script, runs each of the microbenchmarks

usage()
{
	echo "./runCommand.sh <fileSystem>"
}

fileSystem=${1:-ext4}
initFS=false

# initialize the device

if [[ $initFS ]]; then
	sudo umount -l /mnt
	# hdparam command
	# hdparm --user-master u --security-set-pass pass /dev/sdd
	
	sudo hdparm --user-master u --security-erase pass /dev/sdd
	
	# write zero on device
	sudo pv < /dev/zero > /dev/sdd
	
	# mkfs on device
	sudo mkfs.$fileSystem -f /dev/sdd
fi

# mount the device
sudo umount -l /mnt
sudo mount /dev/sdd /mnt

# initialize disk counter
sudo ./diskStat.sh 5 /dev/sdd | tee diskUsage.log &

# TODO
# call microbenchmark with parameters

./create10000

# to see if GC kicks in
sleep 60

# unmount the device
sudo umount -l /dev/sdd

# terminate disk counter
sudo kill -9 `pgrep diskStat.sh`

# draw the graph
