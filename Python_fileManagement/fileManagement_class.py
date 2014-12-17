#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#

import io, os, shutil, stat

'''this class helps with copying, moving, and manipulating search criteria to find images and create directories'''

# #if 'DNU' not in file:   add under line 94 if needed


class FileManagement():
	''' move copys of files around and other things'''
	def __init__(self, mainSourceFilesPath, mainFileDestination, fileName = []):
		self.mainSourceFilesPath = mainSourceFilesPath
		self.mainFileDestination = mainFileDestination
		self.fileName = fileName
		self.logInfo  = []

	# reads and returns text in a file
	def SaveTxtToFile(self):
		imageNames = []
		path = (str(self.mainFileDestination) + '/' + str(self.fileName))
		fo =  open(path)
		try:
			for line in fo:
				imageNames.append(line)
			return imageNames
		except:
			pass
		fo.close()
	# removes paragraph returns
	def removeCharaters(self,  listToRemoveChars ):
		temp = ''
		cleanList = []
		for i in listToRemoveChars:
			temp = temp + i
			cleanList = temp.split('\n')
		return cleanList
	# slices a list of data and returns a new list
	def spliceFileName(self, col, start = None, end =None):
		z = [i[start: end] for i in col]
		return z
	# use to conatinate a list of paths
	def GetFirstSubdirectoryNames(self, path, sub1 = []):
		dir1_path = []
		for sub in sub1:
			nPath = path + '/' + sub
			dir1_path.append(nPath)
		return dir1_path

	# use if you hav a list of muliple paths
	def GetSubdirectoryNamesMultiplePaths(self, paths, sub1 = []):
		dir1_path = []
		for path in paths:
			for sub in sub1:
				nPath = path + '/' + sub
				dir1_path.append(nPath)
		return dir1_path

	def GetAdditionalSubDirNames(self, dir1_path, additionalSub = [] ):
		#subdirectoryNames = subdirectoryNames
		newSubList = []
		tempName = ''
		counter = 0
		count = 0
		for i in dir1_path: #subdirectoryNames:
			if count == counter:
				tempName = i + '/' + additionalSub[counter]
				counter += 1
				count += 1
				newSubList.append(tempName)
		return newSubList

	# CreateDestinationFolder = path + folder name
	def makeDestinationDirctory(self, CreateDestinationFolder):
		temp = ''
		for i in CreateDestinationFolder:
			temp = i
			try:
				os.umask(0000)
				os.mkdir(temp, mode=0o777)
				os.fchmod(temp, 0o777)
			except:
				pass

	# this will make a copy in the desired location
	def MoveCopyStuff(self, sourcePath , destination , searchNames ):
		self.destination = str(destination)
		f = ''
		for source in sourcePath:
			source = source
			try:
				files = os.listdir(source)
			except:
				self.logInfo.append('source folder does not exist: {} \n' .format(source))
				pass
			for searchName in searchNames:
				try:
					if searchName  != '':
						for file in files:
							if searchName in file:
								f = source + '/' + file
								chexForFile = destination[0] + '/' + file
								if os.path.isfile(chexForFile):
									pass
								else:
									shutil.copy2(f, destination[0])
									self.logInfo.append('for search name \'{}\' the following image was found {} \n'.format(searchName, file))
					else:
						pass
				except:
					continue

	#write log to file
	def LogFile(self, logName, destination):
		logName = logName[0] + '_log.txt'
		destination = destination[0] + '/'+ logName
		fo = open(destination, "w")
		for i in self.logInfo:
			fo.write(i)
		fo.close()
		self.logInfo = []

	#checks to see if anything was found in the dest folder that matches the search input
	def AdditionalErrors(self, searchNames, destination):
		files = os.listdir(destination[0] + '/')
		for search in searchNames:
			x = 0
			for file in files:
				if search in file:
					x += 1
			if x == 0:
				self.logInfo.append('no files found for search parameter: {} \n'.format(search))
		return self.logInfo

	# move the original text file into the root of the final folder
	def MoveOrgFile(self, sourcePath , destination , fileName = [] ):
		sourcePath = str(sourcePath)
		fileName = str(fileName)
		moveMe = []
		source= os.listdir(sourcePath)
		try:
			if fileName in source:
				moveMe = sourcePath + '/' + fileName
				shutil.move(moveMe, destination[0])
		except:
			pass

	# takes source path and a list of old names and new names the renames files
	def rename(self, path,old,new):
		count = -1
		for i in old:
			count += 1
			for f in os.listdir(path):
				os.rename(os.path.join(path, f),
				          os.path.join(path, f.replace(old[count], new[count])))
