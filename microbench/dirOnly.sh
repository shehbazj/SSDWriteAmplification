# this benchmark creates only directories in the file system.
# it benchmark is used in order to determine the amount of file system
# write amplification that is caused due to metadata updates.

# 1. hdparam - secure cleanup the file system - by securely erasing the SSD
# 2. dd if=/dev/zero of=/dev/sdd bs=128M

usage()
{
	echo "python dirOnly.py <pcDiskCapacity> <pcDelete>"
	echo ""
	echo "pcDiskCapacity - percentage Disk Capacity [ 1 - 100 ]"
	echo "pcDelete - percentage of directories to be deleted, among those that were created [ 0 - 100 ]"
	echo ""
}

if [[ "$#" -lt 1 ]]; then
	usage
	exit
fi

pcDiskCapacity=$1
pcDelete=${2:-0}

if [[ "$pcDiskCapacity" -lt 1 || "$pcDiskCapacity" -gt 99 ]]; then
	usage
fi

# invoke workload.py recursively with request to create 100 directories using mkdir -p command.
# delete a certain percentage of the above created directories. where number of removed directories 
# is given by pcDelete

# keep creating 100 directories provided by the workload tool, after randomization
# check if disk capacity has reached pcDiskCapacity.

# if yes, terminate
# if no, continue creating 100 directories and deleting pcDelete directories.

diskUsage=0

#while [[ "$diskUsage" -lt "$pcDiskCapacity" ]];
#do
	python workload.py create --maxDirDepth 8 --numFiles 100 --dirOnly True > currCmd

	# sort currCmd based on directory hierarchy
	# lowest directory depth first, followed by higher directory depth

	awk '{print gsub("/","/"), $0}' < currCmd | sort -rn | cut -d' ' -f2- | tac > sortedCurrCmd
	mv sortedCurrCmd currCmd

	if [[ "$pcDelete" -ne 0 ]]; then
		echo "$pcDelete percent delete"
		# 1. get num directories. 
		numDirs=`wc -l currCmd | cut -d" " -f1`

		# 2. generate sequence number of directories to be deleted
		delDirNum=$(($numDirs * $pcDelete / 100))
		rm -rf delDirSeqNum currDelCmd
		for i in `seq 1 $delDirNum`;
		do
			echo "$(($RANDOM % $numDirs))" >> delDirSeqNum
		done
		sort -n delDirSeqNum > d_delDirSeqNum
		mv d_delDirSeqNum delDirSeqNum
		
		# 3. generate list of rm commands
		while read line;
		do
			head -$line currCmd | tail -1 | sed 's/mkdir/rm -rf/'  >> currDelCmd
		done < delDirSeqNum
	fi

	# sort currDelCmd based on directory hierarchy
	#directory with the longest depth first, followed by higher directory

	awk '{print gsub("/","/"), $0}' < currDelCmd | sort -rn | cut -d' ' -f2- > sortedDelCmd
	mv sortedDelCmd currDelCmd
	cat currDelCmd >> currCmd

	while read line;
	do
		eval "$line"
	done < currCmd
	sync
	diskUsage=`df /dev/sdd | tail -1 | rev | cut -d" " -f2 | cut -d"%" -f2`
	echo "diskUsage = $diskUsage"
#done
