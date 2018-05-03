# Script generates a list of commands for creation, updation or deletion of file and/or directories
#
# create
#	maxDirDepth (specify 0 for no directories), 
#	minFileSize, maxFileSize
#	numFiles
#	totalSpaceAllocation (%)
#	fileOnly, dirOnly
#	syncFreq (by default 100)

# fillSpace
#	X% of disk
#	minFileSize, maxFileSize
#	syncFreq (by default 100)
#	given a location, the script creates files of variable sizes to fill upto X% of the disk
#	files could be located anywhere in any directory of the disk

# delete
#	X% of disk
#	this command would choose random list of files from the device and delete them.

# update
#	X% of disk
#	syncFreq (by default 100)
#	this command would open, update (append or overwrite) existing file.
