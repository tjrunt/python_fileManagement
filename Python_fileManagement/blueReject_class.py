#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski 

import io, os, shutil


''' This class is to help process blue reject specific file processing'''
class blueReject_helpers():

	def __init__(self):
		self.logInfo = []

	#deletes files from one place and places a copy else where aka its moving files
	# this also takes an alt_destination path specifically to move some files that end with the '.png' that are in the same source folder to a diffrent location
	def blueRejectMove(self, sourcepaths, destinations, alt_destination, searchCol):
		count = -1
		for i in searchCol:
			count += 1
			files = os.listdir(sourcepaths)
			for file in files:
				if i in file:
					f = sourcepaths + '/' + file
					if f.endswith('.png'):
						try:
							shutil.move(f, alt_destination)
						except:
							self.logInfo.append('cannot move {} it already exists in this location {} \n'.format(f, alt_destination))
					else:
						try:
							shutil.move(f, destinations[count])
						except:
							self.logInfo.append('cannot move {} it already exists in this location {} \n'.format(f, destinations[count]))


	# Moves anything
	def blueRejectMove2(self, sourcepaths, destinations, searchCol):
		count = -1
		for i in searchCol:
			count += 1
			files = os.listdir(sourcepaths)
			for file in files:
				if i in file:
					f = sourcepaths + '/' + file
					try:
						shutil.move(f, destinations[count])
					except:
						self.logInfo.append('cannot move {} it already exists in this location {} \n'.format(f, destinations[count]))


	#checks for errors to see if anything was found in the dest folder that matches the search input
	def blueRejectResultsLog(self, path):
		self.logInfo.append('Found files directory summary: \n')
		for root, dirs, files in os.walk(path):
			self.logInfo.append('directory: {} \n'.format(root))
			self.logInfo.append(' files: {} \n'.format(files))
		return self.logInfo

		#write log to file
	def LogFile(self, logName, destination):
		logName = logName[0] + '_log.txt'
		destination = destination + '/'+ logName
		fo = open(destination, "w")
		for i in self.logInfo:
			fo.write(i)
		fo.close()
		self.logInfo = []
