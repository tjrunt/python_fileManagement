#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski 
#

import os
import shutil
import csv

'''NIKE vars Classes stuff'''
class nikeStuff():
	#gets the last 3 digs for folder_names and returns list of  Names to creat folders from

	def __init__(self):
		self.logInfo = []

	def NikeCopyFiles(self, sourcepaths, destinations, searchCol):
		count = -1
		for i in searchCol:
			count += 1
			if os.path.isdir(sourcepaths[count]):
				files = os.listdir(sourcepaths[count])
				for file in files:
					if i in file:
						f = sourcepaths[count] + '/' + file
						chexForFile = destinations[count] + '/' + file
						if os.path.isfile(chexForFile):
							pass
						else:
							shutil.copy2(f, destinations[count])
			elif ('OnBody_Catalog' in sourcepaths[count]) and ('PREM' in searchCol[count]):
				self.logInfo.append('warning folder not found: {}  \n'.format(sourcepaths[count]))
			elif ('OnBody_Catalog' in sourcepaths[count]) and ('PREM' not in searchCol[count]):
				pass
			else:
				self.logInfo.append('warning folder not found: {}  \n'.format(sourcepaths[count]))
				return self.logInfo


	# Based on the search criteia this will return one col as two.
	def break_col_in_two(self, col, pre = 'PREM'):
		new_names = []
		col_of_prem = []
		for i in col:
			if pre in i:
				col_of_prem.append(i)
			else:
				new_names.append(i)
		return col_of_prem, new_names

	# use this to return a col with text removed
	def remove_text(self, col, pre ='-PREM'):
		replaced_col = []
		for i in col:
			x = i.replace(pre, '')
			replaced_col.append(x)
		return replaced_col
	# adds a seperator to the end of each item in a list
	def seperator(self, col, seperator = ''):
		new = []
		x = 0
		for i in col:
			temp = col[x] + seperator
			new.append(temp)
			x += 1
		return new

	#concatinates two columns and returns it as a list first col is the col you want to be first
	# the separator is added to the end
	def getFolderName(self, col1, col2, seperator = ''):
		new = []
		x = 0
		for i in col1:
			temp = col1[x] + col2[x] + seperator
			new.append(temp)
			x += 1
		return new

	# returns a list of counts to determine where a new folder search begins
	def getRowCountForSearches(self, col):
		next_cell = 1
		previous_cell = 0
		count = 1
		unique_row_count = []
		for i in col:
			temp = i
			try:
				if i == col[next_cell]:
					count += 1
					previous_cell += 1
					next_cell += 1
				else:
					unique_row_count.append(count)
					count = 1
					previous_cell += 1
					next_cell += 1
			except:
					pass
		return unique_row_count
	#gets the part of the folder names from what would be col_a i.e. '-639_553_439'
	def folderNamePart2(self, col, rowCounts):
		count = 1
		index = 0
		folderParty = []
		temp = ''
		for eachRow  in col:
			try:
				if count != rowCounts[index]:
					count += 1
					temp = temp + eachRow + 'l'

				else:
					temp = temp + eachRow
					folderParty.append(temp)
					count = 1
					index += 1
					temp = ''
			except:
				pass
		return folderParty

	# 'uniqueRowCounts'  is count of how many times a row repeats
	# 'unfilteredColNames' is the first half of the folder names. spicificly the priority and
	# image name in col_b i.e. 'PREM_' + '588544-PREM_522'
	# 'filteredNames' is the portion of the folder name that contains the other image names that will be
	# in the folder i.e. '-639_553_439' and this will return the final folder name which
	# in this example would be 'PREM_588544-PREM_522-639_553_439'
	def folderNameToEachCol(self, uniqueRowCounts, unfilteredColNames, filteredNames):
		#gets the post fix of the folder names
		count = 1
		index_filteredNames = 0
		finalFolderName = []
		index = 0
		temp = ''
		for row  in unfilteredColNames:
			try:
				if count != uniqueRowCounts[index]:
					count += 1
					temp = row + filteredNames[index]
					finalFolderName.append(temp)
				else:
					temp = row + filteredNames[index]
					finalFolderName.append(temp)
					count = 1
					index_filteredNames += 1
					index += 1
			except:
				pass
		return finalFolderName

	#write to file
	# logName should be file name of the processed file
	#destination = where do you want to save the log?
	def NikeLogFile(self, logName, destination):
		logName = logName[0] + '_log.txt'
		destination = destination[0] + '/'+ logName
		fo = open(destination, "w")
		for i in self.logInfo:
			fo.write(i)
		fo.close()
		self.logInfo = []
	#searchs for errors
	def NikeAdditionalErrors(self, searchNames, destinationpaths):
		#search = ''
		for i in searchNames:
			x = 0
			for j in destinationpaths:
				files = os.listdir(j + '/')
				for file in files:
					if i in file:
						x += 1
			if x == 0:
				self.logInfo.append('no files found for search parameter: {} \n'.format(i))
				return self.logInfo
