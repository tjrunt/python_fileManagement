#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#

import time, os
''' Creates a time stamp and writes it to a log'''
class TimeStamp():

	def __init__(self):
		self.timeStamp = []

	#get current time
	def getTime(self, message=''):
		t = time.time()
		self.timeStamp.append(message)
		self.timeStamp.append(t)
		self.timeStamp.append('\n')
		return t
	#calculate diffrence
	def getTimeDiffrence(self, start, end, message=''):
		totalTime = end - start
		self.timeStamp.append(message)
		self.timeStamp.append(totalTime)
		return totalTime
	# save time to file
	def saveTimeToFile(self, path):
		with open(path, 'a+') as file:
			for i in self.timeStamp:
				i = str(i)
				file.write(i)
		self.timeStamp = []

