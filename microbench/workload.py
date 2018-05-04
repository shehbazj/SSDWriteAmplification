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
import random
from random import randint

def getRandom():
        x=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/') for i in range(100))
        return x

def fileOrDir(fileOnly, dirOnly):
	if fileOnly:
		return 0
	elif dirOnly:
		return 1
	else:
        	return randint(0,1)

def getSize(sizeParam):
	if 'KB' in sizeParam:
		size = sizeParam.split('KB')[0]	
		return int(size) * 1024
	elif 'MB' in sizeParam:
		size = sizeParam.split('MB')[0]
		return int(size) * 1024 * 1024
	elif 'GB' in sizeParam:
		size = sizeParam.split('GB')[0]
		return int(size) * 1024 * 1024 * 1024
	else:
		try:
			int(sizeParam)
		except ValueError:
			print ("size " + sizeParam + " not a valid numeric ")
		return int(sizeParam)
	

def fsize(minsize, maxsize):
        return randint(minsize,maxsize)

def getDirName( maxDepth ):
        x=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/') for i in range(100))
        if x.count('/') > maxDepth - 1:
                x = x.replace("/","X")
        else:   
                while "//" in x:
                        x = x.replace("//","X")
	if x.startswith("/"):
		x = x.replace("/","X",1)
        return x

def createDir(dirName):
	allDirs = dirName.split('/')
	parent = '/mnt/'
	for dirs in allDirs:
		parent += dirs
		parent += '/'
		print ('sudo -- sh -c \'mkdir -p ' + parent + '\'')

def createFile(dirName,minFile, maxFile,fileNumber):
	fileName='/mnt/'+dirName+'/file'+str(fileNumber)
	fileSize=fsize(minFile,maxFile)
	#print ('fileSize = '+str(fileSize))
	#print ('fileSize = '+str((fileSize + 4095 ) / 4096) +' KB')
	count=((fileSize + 4095) / 4096)
	#print ('count = ' + str(count))
	print ('sudo -- sh -c \'dd if=/dev/urandom of=' + fileName + ' bs=4096 count='+str(count))
	return fileSize


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate Shell Commands for creating/reading and writing data')
	subparsers = parser.add_subparsers(help='create|fillSpace|delete|update help')

	# create

	parser_create = subparsers.add_parser('create', help='creates files and directories in an empty file system')
	parser_create.add_argument('--maxDirDepth',type=int,required=True)
	parser_create.add_argument('--numFiles',type=int,required=True)
	parser_create.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')	
	parser_create.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_create.add_argument('--totalSpaceAllocation',type=str,default='10MB',help='Percentage of disk that needs to be filled')
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
	args = parser.parse_args()

##############################################################################################

# parsing complete

#	print args.maxDirDepth
#	print args.syncFreq

# if create:

	if args.numFiles is not None:
		maxDirDepth = int(args.maxDirDepth)
		numFiles = int(args.numFiles)
		minFileSize = getSize(args.minFileSize)
		maxFileSize = getSize(args.maxFileSize)
		totalSpaceAllocation = getSize(args.totalSpaceAllocation)
		fileOnly = args.fileOnly
		dirOnly = args.dirOnly
		syncFreq = args.syncFreq

		for i in range (1,numFiles):
			if totalSpaceAllocation <= 0:
				break
			dirName = getDirName(maxDirDepth)
			ftype = fileOrDir(fileOnly, dirOnly)
			createDir(dirName)
			if ftype is 0: # file
				fileSize = createFile(dirName,minFileSize, maxFileSize,i)
				totalSpaceAllocation -= fileSize
			if i % syncFreq == 0:
				printSyncCommand()
	else:
		print 'numFiles = ' + str(args.numFiles)
			
	
# if delete:


# if update:
