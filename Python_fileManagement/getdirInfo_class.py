#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#

import io, os, shutil

class GetListOfTextFiles:
	''' gets a list of files in the hot folder'''

	def __init__(self, mainSourceFilesPath = [],mainSourcePathOfDirectories = [], listOfFiles = [] ):
		self.mainSourceFilesPath = mainSourceFilesPath
		self.listOfFiles = listOfFiles
		self.mainSourcePathOfDirectories = mainSourcePathOfDirectories

	def getfileTxtFileNames(self):
		dir_ = self.mainSourceFilesPath
		dir_ = os.listdir(dir_)
		for file in dir_:
			if file.endswith(".txt"):
				self.listOfFiles.append(file)
		return self.listOfFiles

	# GetListOfFoldersInDir and returns a list of the folders as paths
	def GetListOfFoldersInDir(self):
		path = self.mainSourcePathOfDirectories
		subDirectories = os.listdir(path)
		folders_ = []
		listOFolders = []
		tempFolderName = []
		for i in subDirectories:
			if not i.startswith("."):
				folders_.append(i)
		for i in folders_:
			tempFolderName = path + '/' + i
			listOFolders.append(tempFolderName)
		return listOFolders
