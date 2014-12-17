#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#


import os
import shutil
import csv
import sys
import io
from fileManagement_class import FileManagement
from getdirInfo_class import GetListOfTextFiles
from nike_FileManagement_classes import nikeStuff
from csv_helper_class import CsvHelpers
from timeStamp_class import TimeStamp

'''
This is processing a tab delimited text file and in this python script it is being read as a
tab-separated excel file using the csv library
'''


##  test server folder paths
hotfolder_location = ['/Volumes/RemoteFS/Summer/Nike_Storage/Z_SimplerTools/Nike_Vars']
# this go two folders deep
paths_to_images_Catalog_tif  = ['/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Catalog/tif']
# only search if image contains perm
paths_to_images_OnBody_Catalog  = ['/Volumes/RemoteFS/Summer/Nike_Storage/OnBody_Catalog/tif']
# line art is only one folder deep, this go two folders deep
line_art_paths_to_images  = ['/Volumes/RemoteFS/Summer/Nike_Storage/Nike_Lineart_Library']

num =['a']
#checks for a temp file and doesnt run if it finds one. If no temp file exists it will create one and run the script on and other .txt file
for i in num:
	if os.path.isfile(hotfolder_location[0] + '/temp.txt'):
		break
	else:
		fo = open(hotfolder_location[0] + '/temp.txt', "w")
		fo.write ("I am a temp file I merely exist. Please leave me be." + '\n')
		fo.close()

		#getting list of .txt files to process
		FileNames_nike_object = GetListOfTextFiles(hotfolder_location[0])
		nike_file_Name = FileNames_nike_object.getfileTxtFileNames()

		#  making an isnatnce of FileManagement object to use the functions
		nfo = FileManagement('x','xx')

		# looping through the list for files in the hot folder
		for i in nike_file_Name:
			#checking if  the file is the temp file if so skip it
			if i == 'temp.txt':
				pass
			else:
				org_txt_file_name = i
				name = hotfolder_location[0] + '/' + org_txt_file_name


				# time stamp start
				timeStampObjct = TimeStamp()
				startTime = timeStampObjct.getTime('Start Time: \n')
				# create  CsvHelpers object and read the file
				Csv_fo = CsvHelpers()
				myCsvFile = Csv_fo.readCsvFile(name)
				myCsvFile = Csv_fo.cleanXtraReturns(myCsvFile)
				nike_fo = nikeStuff()
				#  add a blank row at the end
				myCsvFile.append(['','',''])
				# this saves the file as columns
				col_a = Csv_fo.getColumn(myCsvFile,0)
				col_b = Csv_fo.getColumn(myCsvFile, 1)
				col_c = Csv_fo.getColumn(myCsvFile, 2)

				# removes any white space otherwise we will get the wrong priority
				strip_col_c = Csv_fo.removeWhiteSpace(col_c)


				folderNamePrefix = nike_fo.seperator(strip_col_c, '_')

				#E.X. GLBLNET_666174_612-010_407_810 the first underscore
				col_d_second_part_folderNames = nike_fo.getFolderName(folderNamePrefix,col_b, '-')

				# compares and counts duplicates to be used later to figure out what indexs to search foe files and where to copy them to
				rowCounts = nike_fo.getRowCountForSearches(col_d_second_part_folderNames)
				# returns a list of col_a's last 3 characters to be used for the folder names
				third_part_of_folder_name = nfo.spliceFileName(col_a, -3)
				#
				forth_part_of_folder_name = nike_fo.folderNamePart2(third_part_of_folder_name, rowCounts)
				# returns a list of the Filnal folder names for each row
				Final_folder_names = nike_fo.folderNameToEachCol(rowCounts, col_d_second_part_folderNames, forth_part_of_folder_name)


				new_sub_hotfolder_location = [name[0:-4]]
				makeMy_new_sub_hotfolder = nfo.makeDestinationDirctory(new_sub_hotfolder_location)

				# final folder paths
				destinationFolderPaths = nfo.GetSubdirectoryNamesMultiplePaths(new_sub_hotfolder_location, Final_folder_names)

				# filters out duplicates of folder names
				filteredDestinationFolderPaths = Csv_fo.filteredListOfcol(destinationFolderPaths)
				# at last creates the folders
				makeMyfolders = nfo.makeDestinationDirctory(filteredDestinationFolderPaths)

				# removing the last index the last was a blank needed for counting the first is the header row from the tab separated.txt file
				col_a.pop()
				col_b.pop()
				col_c.pop()


				##  for col_A only
				##
				# separate PREM paths and Col_A from non PREM
				col_a_into_two_groups = nike_fo.break_col_in_two(col_a)
				#sepatate PREM destination folders from NON PREM destination FOLDERS
				dest_folders_two_groups = nike_fo.break_col_in_two(destinationFolderPaths)

				# removes '-PREM' for image search
				remove_PREM_col_a = nike_fo.remove_text(col_a_into_two_groups[0])

				# col_a PREM source folders
				PREM_sub_1_col_a = nfo.spliceFileName(col_a_into_two_groups[0], 0, 2)
				PREM_sub_2_col_a = nfo.spliceFileName(col_a_into_two_groups[0], 2, 4)


				# this search code is not needed at this time
				#PREM_sub1_col_a_paths_to_images_1 = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_Catalog_tif, PREM_sub_1_col_a)
				#PREM_sub2_col_a_paths_to_images_1 = nfo.GetAdditionalSubDirNames(PREM_sub1_col_a_paths_to_images_1, PREM_sub_2_col_a)


				PREM_OnBody_sub1_col_a_paths_to_images = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_OnBody_Catalog, PREM_sub_1_col_a)
				PREM_OnBody_sub2_col_a_paths_to_images = nfo.GetAdditionalSubDirNames(PREM_OnBody_sub1_col_a_paths_to_images, PREM_sub_2_col_a)

				PREM_col_a_paths_to_line_art_images = nfo.GetSubdirectoryNamesMultiplePaths(line_art_paths_to_images, PREM_sub_1_col_a)


				# col_a NOT_PREM source folders
				NOT_PREM_sub_1_col_a = nfo.spliceFileName(col_a_into_two_groups[1], 0, 2)
				NOT_PREM_sub_2_col_a = nfo.spliceFileName(col_a_into_two_groups[1], 2, 4)

				NOT_PREM_sub1_col_a_paths_to_images_1 = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_Catalog_tif, NOT_PREM_sub_1_col_a)
				NOT_PREM_sub2_col_a_paths_to_images_1 = nfo.GetAdditionalSubDirNames(NOT_PREM_sub1_col_a_paths_to_images_1, NOT_PREM_sub_2_col_a)


				NOT_PREM_OnBody_sub1_col_a_paths_to_images = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_OnBody_Catalog, NOT_PREM_sub_1_col_a)
				NOT_PREM_OnBody_sub2_col_a_paths_to_images = nfo.GetAdditionalSubDirNames(NOT_PREM_OnBody_sub1_col_a_paths_to_images, NOT_PREM_sub_2_col_a)

				NOT_PREM_col_a_paths_to_line_art_images = nfo.GetSubdirectoryNamesMultiplePaths(line_art_paths_to_images, NOT_PREM_sub_1_col_a)

				# copy files col_a
				# col A PREM copy images
				# search code not needed at this time
				#PREM_search1_cat_col_a = nike_fo.NikeCopyFiles(PREM_sub2_col_a_paths_to_images_1, dest_folders_two_groups[0], remove_PREM_col_a)


				PREM_search3_lineArt_col_a = nike_fo.NikeCopyFiles(PREM_col_a_paths_to_line_art_images, dest_folders_two_groups[0], remove_PREM_col_a)


				# col A   NOT_PREM copy images

				# this search is not needed at this time
				#NOT_PREM_search_cat_col_a = nike_fo.NikeCopyFiles(NOT_PREM_sub2_col_a_paths_to_images_1, dest_folders_two_groups[1], col_a_into_two_groups[1])


				NOT_PREM_search_lineArt_col_a = nike_fo.NikeCopyFiles(NOT_PREM_col_a_paths_to_line_art_images, dest_folders_two_groups[1], col_a_into_two_groups[1])


				###
				### for Col_B copy only
				#separate PREM paths and Col_B from non PREM
				col_b_into_two_groups = nike_fo.break_col_in_two(col_b)

				# is not needed at this time it was removing '-PREM' for an additional image search
				#remove_PREM_col_b = nike_fo.remove_text(col_b_into_two_groups[0])



				# col_b PREM source folders
				PREM_sub_1_col_b = nfo.spliceFileName(col_b_into_two_groups[0], 0, 2)
				PREM_sub_2_col_b = nfo.spliceFileName(col_b_into_two_groups[0], 2, 4)

				PREM_sub1_col_b_paths_to_images_1 = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_Catalog_tif, PREM_sub_1_col_b)
				PREM_sub2_col_b_paths_to_images_1 = nfo.GetAdditionalSubDirNames(PREM_sub1_col_b_paths_to_images_1, PREM_sub_2_col_b)


				PREM_OnBody_sub1_col_b_paths_to_images = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_OnBody_Catalog, PREM_sub_1_col_b)
				PREM_OnBody_sub2_col_b_paths_to_images = nfo.GetAdditionalSubDirNames(PREM_OnBody_sub1_col_b_paths_to_images, PREM_sub_2_col_b)

				PREM_col_b_paths_to_line_art_images = nfo.GetSubdirectoryNamesMultiplePaths(line_art_paths_to_images, PREM_sub_1_col_b)

				# col_b NOT_PREM source folders
				NOT_PREM_sub_1_col_b = nfo.spliceFileName(col_b_into_two_groups[1], 0, 2)
				NOT_PREM_sub_2_col_b = nfo.spliceFileName(col_b_into_two_groups[1], 2, 4)

				NOT_PREM_sub1_col_b_paths_to_images_1 = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_Catalog_tif, NOT_PREM_sub_1_col_b)
				NOT_PREM_sub2_col_b_paths_to_images_1 = nfo.GetAdditionalSubDirNames(NOT_PREM_sub1_col_b_paths_to_images_1, NOT_PREM_sub_2_col_b)


				NOT_PREM_OnBody_sub1_col_b_paths_to_images = nfo.GetSubdirectoryNamesMultiplePaths(paths_to_images_OnBody_Catalog, NOT_PREM_sub_1_col_b)
				NOT_PREM_OnBody_sub2_col_b_paths_to_images = nfo.GetAdditionalSubDirNames(NOT_PREM_OnBody_sub1_col_b_paths_to_images, NOT_PREM_sub_2_col_b)

				NOT_PREM_col_b_paths_to_line_art_images = nfo.GetSubdirectoryNamesMultiplePaths(line_art_paths_to_images, NOT_PREM_sub_1_col_b)

				# copy files col_b
				# col b PREM copy images

				## ??? comment out line 196 currently dont need to search here
				#PREM_search1_cat_col_b = nike_fo.NikeCopyFiles(PREM_sub2_col_b_paths_to_images_1, dest_folders_two_groups[0], remove_PREM_col_b)
				PREM_search2_OnBody_col_b = nike_fo.NikeCopyFiles(PREM_OnBody_sub2_col_b_paths_to_images, dest_folders_two_groups[0], col_b_into_two_groups[0])


				# col b   NOT_PREM copy images
				NOT_PREM_search_cat_col_b = nike_fo.NikeCopyFiles(NOT_PREM_sub2_col_b_paths_to_images_1, dest_folders_two_groups[1], col_b_into_two_groups[1])



				##log code here
				logName = [org_txt_file_name[:-4]]
				loggy_the_log_file_col_a = nike_fo.NikeAdditionalErrors(col_a, destinationFolderPaths)
				loggy_the_log_file_col_b = nike_fo.NikeAdditionalErrors(col_b, destinationFolderPaths)
				save_loggy_the_log_file = nike_fo.NikeLogFile(logName, new_sub_hotfolder_location)
				move_txt_file = nfo.MoveOrgFile(hotfolder_location[0], new_sub_hotfolder_location ,org_txt_file_name)

				# time stamp end and write to log
				timePath = new_sub_hotfolder_location[0] + '/' + logName[0] + '_log.txt'
				endTime = timeStampObjct.getTime('End Time: \n')
				totalTime = timeStampObjct.getTimeDiffrence(startTime, endTime, 'Total processing Time: \n')
				saveStamptoFile = timeStampObjct.saveTimeToFile(timePath)


		#removes the temp file
		os.remove(hotfolder_location[0] + '/temp.txt')



def main():
	pass
if __name__ == "__main__": main()




