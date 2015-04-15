#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski
#

import os
import shutil
import csv
import sys
import io
import time
from fileManagement_class import FileManagement
from getdirInfo_class import GetListOfTextFiles
from csv_helper_class import CsvHelpers
from blueReject_class import blueReject_helpers
from timeStamp_class import TimeStamp


## afp paths for if you need to run from idle on a mac
#hotfolder_location = ['/Volumes/Nike_Production/Z_SimplerTools/BlueRejects']
##files are searched for here
#image_location_path = ['/Volumes/Nike_Production/Approved_Images']
# tiff files that are found are moved here - these are moved not copied--- this is also the path for screen grabs
#tiff_move_location_path = ['/Volumes/Nike_Production/0_Nike_to_PostProduction/_GCS/5_ReWorks/BlueRejection/__BlueRejects_InProgress']
## all found png's go here
#png_move_location_path = ['/Volumes/Nike_Production/0_Nike_to_PostProduction/_GCS/5_ReWorks/BlueRejection/__BlueRejects_InProgress/png_Dump/']



#  Live paths
hotfolder_location = ['/Volumes/RemoteFS/Summer/Nike_Storage/Z_SimplerTools/BlueRejects']
#files are searched for here
image_location_path = ['/Volumes/RemoteFS/Summer/Nike_Storage/Approved_Images']
# tiff files that are found are moved here -- these are moved not copied--
tiff_move_location_path = ['/Volumes/RemoteFS/Summer/Nike_Storage/0_Nike_to_PostProduction/_GCS/5_ReWorks/BlueRejection/__BlueRejects_InProgress']
# all found png's go here
png_move_location_path = ['/Volumes/RemoteFS/Summer/Nike_Storage/0_Nike_to_PostProduction/_GCS/5_ReWorks/BlueRejection/__BlueRejects_InProgress/png_Dump/']


# gets list of .txt files to process
txt_files = GetListOfTextFiles(hotfolder_location[0])
file_Name = txt_files.getfileTxtFileNames()

# creates object instances of imported classes
fmo = FileManagement('','')
bro = blueReject_helpers()

# loops through text files in hotfolder
for i in file_Name:
	if 'BlueRejects' in i:


		# time stamp start
		timeStampObjct = TimeStamp()
		startTime = timeStampObjct.getTime('Start Time: \n')

		name = hotfolder_location[0] + '/' + i
		final_folder_name = [i[:-4]]
		final_folder_location = tiff_move_location_path[0] + '/' + final_folder_name[0]
		# create instance of CsvHelpers() object
		Csv_fo = CsvHelpers()

		# create instance of FileManagement() object to use its methods
		blue_fileManagement = FileManagement(image_location_path, tiff_move_location_path)

		# reading the .txt file and storing it as columns
		myCsvFile = Csv_fo.readCsvFile(name)
		myCsvFile = Csv_fo.cleanXtraReturns(myCsvFile)
		col_a = Csv_fo.getColumn(myCsvFile,0)
		col_b = Csv_fo.getColumn(myCsvFile, 1)

		# removes any white space probaly not needed but just in case
		strip_col_a = Csv_fo.removeWhiteSpace(col_a)
		strip_col_b = Csv_fo.removeWhiteSpace(col_b)

		#make folder names
		folderNames = Csv_fo.joinTwoCols(strip_col_a, strip_col_b)

		destFolder = [final_folder_location]
		# make a folder based on the .txt file name to move everything to
		makeDestFolder = blue_fileManagement.makeDestinationDirctory(destFolder)


		# getting dir info
		getFolderPaths = blue_fileManagement.GetFirstSubdirectoryNames(destFolder[0], folderNames)
		makeFolders = blue_fileManagement.makeDestinationDirctory(getFolderPaths)

		# Searching for and moving files
		move = bro.blueRejectMove(image_location_path[0], getFolderPaths, png_move_location_path[0], col_a)
		move_screenGrabs = bro.blueRejectMove2(tiff_move_location_path[0], getFolderPaths,  col_a)

		#move org .txt file into new directory
		shutil.move(name, destFolder[0])

		#log errors and info
		resultsLog = bro.blueRejectResultsLog(destFolder[0])

		saveLog = bro.LogFile(final_folder_name, destFolder[0])


		# time stamp end and write to log file
		timePath = destFolder[0] + '/' + final_folder_name[0] + '_log.txt'
		endTime = timeStampObjct.getTime('End Time: \n')
		totalTime = timeStampObjct.getTimeDiffrence(startTime, endTime, 'Total processing Time: \n')
		saveStamptoFile = timeStampObjct.saveTimeToFile(timePath)






def main():
	pass
if __name__ == "__main__": main()


