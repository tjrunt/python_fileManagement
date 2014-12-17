#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#

import io, os, shutil, csv

''' This class is to help process csv file'''
class CsvHelpers():
	def __init__(self):
		pass

	#reads a csv file and returns a list
	def readCsvFile(self, file_path, d = 'excel-tab'):
		# dialect='excel-tab'
		with open(file_path, 'r') as f:
			reader = csv.reader(f, dialect = d)
			rows =[row for row in reader]
		return rows

	#returns the data in a column of a csv file
	def getColumn(self, csv_data, column):
		col = [row[column] for row in csv_data]
		return col

	#get a filtered list use to create folders
	def filteredListOfcol(self, column):
		filtered_col_list = []
		for i in column:
			if i not in filtered_col_list:
				filtered_col_list.append(i)
		return filtered_col_list

	def combine_columns(self, col_1 = None, col_2 = None):
		all_names = col_1 + col_2
		all_names2 = []
		for i in all_names:
			if i != '':
				all_names2.append(i)
			else:
				pass
		return all_names2

	#strip white space
	def removeWhiteSpace(self, col):
		new_col = [i.strip(' ') for i in col]
		return new_col

	# remove and paragraph returns
	def cleanXtraReturns(self, data):
		x =[]
		for i in data:
			if i != []:
				x.append(i)
		return x

	def joinTwoCols(self, col1, co2 , separator = '_' ):
		count = 0
		joinedCols = []
		for i in col1:
			joinedCols.append(i + separator + co2[count])
			count += 1
		return joinedCols
