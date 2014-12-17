#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#


import io, os, shutil, sys, stat, datetime, time
from fileManagement_class import FileManagement
from getdirInfo_class import GetListOfTextFiles
from csv_helper_class import CsvHelpers
from timeStamp_class import TimeStamp


''' this is the code that runs the redelivery script'''


hotfolder_location = ['/Volumes/RemoteFS/Summer/Nike_Storage/Z_SimplerTools/Redelivery_in_a_Box']


# these go two folders deep
paths_to_images_Catalog_tif  = ['/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Catalog/tif']
paths_to_images_Catalog_png  = ['/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Catalog/png']
paths_to_images_OnBody_Catalog  = ['/Volumes/RemoteFS/Summer/Nike_Storage/OnBody_Catalog/tif']
paths_to_images_OnBody_Catalog_png  = ['/Volumes/RemoteFS/Summer/Nike_Storage/OnBody_Catalog/png']


listOfFilesToProcess = GetListOfTextFiles(hotfolder_location[0])
filesInFolder = listOfFilesToProcess.getfileTxtFileNames()

#creates a temp file  and checks if cron is running if a temp file exists the script is running and it will not run again
num =['a']
for i in num:
	if os.path.isfile(hotfolder_location[0] + '/temp.txt'):
		break
	else:
		fo = open(hotfolder_location[0] + '/temp.txt', "w")
		fo.write ("I am a temp file I merely exist. Please leave me be." + '\n')
		fo.close()
		#processes Redelivery .txt files
		for i in filesInFolder:
			if 'Redelivery' in i:
				fileName = i
				f = [fileName[:-4]]
				# time stamp start
				timeStampObjct = TimeStamp()
				startTime = timeStampObjct.getTime('Start Time: \n')


				#csv object
				Csv_fo = CsvHelpers()
				# fileManagement object
				fmo =FileManagement('','')

				# gets source path of test file
				readMe = hotfolder_location[0] + '/' + fileName
				#reads the text file
				myCsvFile = Csv_fo.readCsvFile(readMe)
				myCsvFile = Csv_fo.cleanXtraReturns(myCsvFile)
				col_a = Csv_fo.getColumn(myCsvFile,0)

				col_b = Csv_fo.getColumn(myCsvFile, 1)
				# gets sub dir names from columns in test file
				subdir1 = fmo.spliceFileName(col_a,0, 2)
				subdir2 = fmo.spliceFileName(col_a, 2, 4)

				# puts together the sourcepaths folders
				# tiffs
				tiff_cat_path_to_subdir1 = fmo.GetFirstSubdirectoryNames(paths_to_images_Catalog_tif[0], subdir1)
				tiff_cat_path_to_subdir2 = fmo.GetAdditionalSubDirNames(tiff_cat_path_to_subdir1,subdir2)
				#pngs
				png_cat_path_to_subdir1 = fmo.GetFirstSubdirectoryNames(paths_to_images_Catalog_png[0], subdir1)
				png_cat_path_to_subdir2 = fmo.GetAdditionalSubDirNames(png_cat_path_to_subdir1,subdir2)

				#on body tiffs
				OnBody_cat_path_to_subdir1 = fmo.GetFirstSubdirectoryNames(paths_to_images_OnBody_Catalog[0], subdir1)
				OnBody_cat_path_to_subdir2 = fmo.GetAdditionalSubDirNames(OnBody_cat_path_to_subdir1,subdir2)

				# Onbody PNG
				OnBody_cat_path_to_subdir1_png = fmo.GetFirstSubdirectoryNames(paths_to_images_OnBody_Catalog_png[0], subdir1)
				OnBody_cat_path_to_subdir2_png = fmo.GetAdditionalSubDirNames(OnBody_cat_path_to_subdir1_png,subdir2)
				print(OnBody_cat_path_to_subdir2_png)

				#make dir to copy files to
				folder = [f[0]]
				finalDestinationPath = fmo.GetFirstSubdirectoryNames(hotfolder_location[0], folder)
				makeDirToCopyFilesTo = fmo.makeDestinationDirctory(finalDestinationPath)

				# copy files from source to destination
				tiff_grabFiles = fmo.MoveCopyStuff(tiff_cat_path_to_subdir2, finalDestinationPath, col_a)
				png_grabFiles = fmo.MoveCopyStuff(png_cat_path_to_subdir2, finalDestinationPath, col_a)
				onBody_grabFiles = fmo.MoveCopyStuff(OnBody_cat_path_to_subdir2, finalDestinationPath, col_a)
				onBody_grabFiles_png = fmo.MoveCopyStuff(OnBody_cat_path_to_subdir2_png, finalDestinationPath, col_a)


				# rename files
				renameMe = fmo.rename(finalDestinationPath[0] ,col_a, col_b)
				# write errors to log
				saveLog = fmo.LogFile(f, finalDestinationPath)

				# move org file
				shutil.move(readMe, finalDestinationPath[0])

				# time stamp end and write to log file
				timePath = finalDestinationPath[0] + '/' + f[0] + '_log.txt'
				endTime = timeStampObjct.getTime('End Time: \n')
				totalTime = timeStampObjct.getTimeDiffrence(startTime, endTime, 'Total processing Time: \n')
				saveStamptoFile = timeStampObjct.saveTimeToFile(timePath)

		#removes the temp file
		os.remove(hotfolder_location[0] + '/temp.txt')

