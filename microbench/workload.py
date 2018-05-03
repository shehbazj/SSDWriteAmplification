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

import argparse
import sys


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate Shell Commands for creating/reading and writing data')
	subparsers = parser.add_subparsers(help='create|fillSpace|delete|update help')

	# create

	parser_create = subparsers.add_parser('create', help='creates files and directories in an empty file system')
	parser_create.add_argument('--maxDirDepth',type=int,required=True)
	parser_create.add_argument('--numFiles',type=int,required=True)
	parser_create.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')	
	parser_create.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_create.add_argument('--totalSpaceAllocation',type=int,help='Percentage of disk that needs to be filled')
	parser_create.add_argument('--fileOnly',type=bool, default=False)
	parser_create.add_argument('--dirOnly',type=bool, default=False)
	parser_create.add_argument('--syncFreq',type=int,default=100)

	# fillSpace (does not take numFiles)

	parser_fillSpace = subparsers.add_parser('fillSpace', help='needs a file system that already has data')

	parser_fillSpace.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')	
	parser_fillSpace.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_fillSpace.add_argument('--syncFreq',type=int,required=True)

	# delete (does not take minFileSize)
	parser_delete = subparsers.add_parser('delete', help='needs a filesystem that already has data')
	parser_delete.add_argument('--size',type=int,help='Percentage of disk that needs to be filled (in %)', required=True)

	# update (does not take minFileSize, takes syncFreq)
	parser_update = subparsers.add_parser('update', help='needs a filesystem that already has data')
	parser_update.add_argument('--size',type=int,help='Percentage of disk that needs to be filled', required=True)

#	parser.add_argument('--')
	args = parser.parse_args()


	print args
#	print args.maxDirDepth
#	print args.syncFreq
