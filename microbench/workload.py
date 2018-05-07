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
#	minFileSize, maxFileSize
#	syncFreq (by default 100)
#	this command would open, update (append or overwrite) existing file.

import argparse
import sys
import subprocess
import random
from random import randint

def getRandom():
        x=''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ/') for i in range(1000))
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
		if dirs.endswith("/") or dirs is '' or dirs is None:
			continue
		parent += dirs
		parent += '/'
		print ('sudo -- sh -c \'mkdir ' + parent + '\'')

def getAvailableDiskSpace():
	cmd = ['df','/dev/sdd']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = p.communicate()
        return (int(out.split('\n')[1].split()[3]) * 1024)

def createFile(dirName,minFile, maxFile,fileNumber):
	fileName='/mnt/'+dirName+'/file'+str(fileNumber)
	fileSize=fsize(minFile,maxFile)
	count=((fileSize + 4095) / 4096)
	print ('sudo -- sh -c \'dd if=/dev/urandom of=' + fileName + ' bs=4096 count='+str(count)+'\'')
	return fileSize

def overWriteFile(fileName, startIndex, endIndex):
	seekOffset = startIndex / 4096
	count = (endIndex - startIndex) / 4096
	print ('sudo -- sh -c \'dd if=/dev/urandom of='+fileName+' bs=4096 count='+str(count)+' seek='+str(seekOffset)+' conv=notrunc\'')

def getFileSize(fileName):
	cmd = ['stat','--printf=\"%s\"',fileName]
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
        out,err = p.communicate()
	out = out.replace('"','')
	#print(out.split(' '))
	return int(out)

def updateFile(fileName,updateType,minFileSize,maxFileSize):
	fileSize = getFileSize(fileName)
	#print type(fileSize)
	if updateType == 0:
		# same size
		overWriteFile(fileName, 0 , fileSize )
	elif updateType == 1:
		# append
		overWriteFile(fileName, fileSize , randint(fileSize, min(fileSize + maxFileSize, maxFileSize)))
	elif updateType == 2:
		# different size
		overWriteFile(fileName, 0 , randint(minFileSize, maxFileSize))
	elif updateType == 3:
		# random blocks within same file
		overWriteFile(fileName, randint(0, fileSize / 2) , randint( (fileSize + 2) / 2, fileSize))

def getAllDirList():
	cmd = [ 'ls','-R' ,'/mnt/']
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
	out , err = p.communicate()
#	print (out)
	out = list(out.split('\n'))
#	print(out)
	allDirs = []
	for element in out:
	#	print(element)
		if ':' in element:
			allDirs.append(element.split(':')[0])
	return allDirs

#def getRandomDir(dirList):	

def getAllFileList():
	cmd = [ 'find', '/mnt', '-type', 'f' ]
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE,stdin=subprocess.PIPE,stderr=subprocess.PIPE)
	out , err = p.communicate()
	return list(out.split('\n'))
	return allFiles

def deleteFile(fileName):
	print ('sudo -- sh -c \'rm '+ fileName + '\'')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate Shell Commands for creating/reading and writing data')
	subparsers = parser.add_subparsers(help='create|fillSpace|delete|update help',dest='command')

	# create

	parser_create = subparsers.add_parser('create', help='creates files and directories in an empty file system')
	parser_create.add_argument('--maxDirDepth',type=int,default=5)
	parser_create.add_argument('--numFiles',type=int,required=True)
	parser_create.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')	
	parser_create.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_create.add_argument('--totalSpaceAllocation',type=str,default='1GB',help='Amount of disk that needs to be filled, default 1GB')
	parser_create.add_argument('--fileOnly',type=bool, default=False)
	parser_create.add_argument('--dirOnly',type=bool, default=False)
	parser_create.add_argument('--syncFreq',type=int,default=100)

	# fillSpace (does not take numFiles)

	parser_fillSpace = subparsers.add_parser('fillSpace', help='needs a file system that already has data')
	parser_fillSpace.add_argument('--size',type=int,required=True, help=' percentage of remaining space to be filled (between 1-99)',choices=range(1,100))
	parser_fillSpace.add_argument('--maxDirDepth',type=int,default=5)
	parser_fillSpace.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')
	parser_fillSpace.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_fillSpace.add_argument('--syncFreq',type=int,required=True)

	# delete (does not take minFileSize)
	parser_delete = subparsers.add_parser('delete', help='needs a filesystem that already has data')
	parser_delete.add_argument('--size',type=int,help='Percentage of disk that needs to be filled (in %)', required=True, choices=range(1,100))
	# update (does not take minFileSize, takes syncFreq)
	parser_update = subparsers.add_parser('update', help='needs a filesystem that already has data')
	parser_update.add_argument('--size',type=int,help='Percentage of disk that needs to be filled', required=True, choices=range(1,100))
	parser_update.add_argument('--minFileSize',type=str,default='4096', help=' (add KB, MB or GB. defaults to bytes)')
	parser_update.add_argument('--maxFileSize',type=str,default='1MB',help=' (add KB, MB or GB. defaults to bytes)')
	parser_update.add_argument('--syncFreq',type=int,required=True)

	args = parser.parse_args()
	command = args.command

##############################################################################################

# parsing complete

#	print args.maxDirDepth
#	print args.syncFreq

# if create:

	if command == "create":
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
		# 	TODO syncFrequency
		# 	sort the print commands in increasing order of '/' count.
		#	add sync command after each syncFrequency interval
		#	if i % syncFreq == 0:
		#		printSyncCommand()

#if fillSpace
	elif command == "fillSpace":
		totalSpaceAllocation = (args.size * getAvailableDiskSpace()) / 100
		minFileSize = getSize(args.minFileSize)
		maxFileSize = getSize(args.maxFileSize)
		syncFreq = args.syncFreq
		allDirs = getAllDirList()
		fileIndex = 99999

		while totalSpaceAllocation > 0:
			ftype = fileOrDir(False,False)
			dirName = allDirs[randint(1,len(allDirs) - 1)]
			fileSize = createFile(dirName, minFileSize, maxFileSize, fileIndex)
			fileIndex += 1
			totalSpaceAllocation -= fileSize
	
# if delete:
	elif command == "delete":
		deletePercentage = args.size	
		allFiles = getAllFileList()
		numFilesToDelete = len(allFiles) * deletePercentage / 100
		for i in range(1, numFilesToDelete):
			deleteFile(allFiles[randint(1,len(allFiles) - 1)])

# if update:
	# overwrite file completely, of the same size.
	# append to file.
	# overwrite file completely, of different size.
	# overwrite few blocks of file
	elif command == "update":
	#	print('update')
		size = args.size
		minFileSize = getSize(args.minFileSize)
		maxFileSize = getSize(args.maxFileSize)
		syncFreq = args.syncFreq
		allFiles = getAllFileList()
		numFiles = (len(allFiles) * size) / 100
		for i in range(0,numFiles - 1):
			fileName = allFiles[randint(0, len(allFiles) - 1)]
			updateFile(fileName,randint(0,4),minFileSize,maxFileSize)
	else:
		print("Please enter a valid command")
