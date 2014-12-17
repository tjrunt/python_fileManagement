#!/usr/bin/python3
#
# This is part of the  Nike file copy scripts. 2014
# Written by Timothy j. Kleszczewski <Timothy.Kleszczewski@sgkinc.com>
# Project Owner Ann Eidson <Ann.Eidson@schawk.com>
#

import io, os, shutil, sys, stat
from fileManagement_class import FileManagement
from getdirInfo_class import GetListOfTextFiles
from timeStamp_class import TimeStamp
from csv_helper_class import CsvHelpers



''' This runs 10 simular scripts that were origanaly applescripts'''

# live server paths
hotfolderLocation = ('/Volumes/RemoteFS/Summer/Nike_Storage/Z_SimplerTools/fred_gets')
path_tiff = ('/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Catalog/tif')
path_png = ('/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Catalog/png')
path_OnBody_Catalog_png = ('/Volumes/RemoteFS/Summer/Nike_Storage/OnBody_Catalog/png')
path_OnBody_Catalog_tff =('/Volumes/RemoteFS/Summer/Nike_Storage/OnBody_Catalog/tif')
path_Nike_Lineart_Library = ('/Volumes/RemoteFS/Summer/Nike_Storage/Nike_Lineart_Library')
path_FredGetEps = ('/Volumes/RemoteFS/Autumn/Nike_Storage/Nike/Masters/Global_Illustration_Library')


# gets the names of .txt files to process
listOfFilesToProcess = GetListOfTextFiles(hotfolderLocation)
filesInFolder = listOfFilesToProcess.getfileTxtFileNames()

#these are the main functions that call the suporting classes
try:
	def getNewFiles(fileName, path, processMe):
		#main function calls
		# time stamp start
		timeStampObjct = TimeStamp()
		startTime = timeStampObjct.getTime('Start Time: \n')

		#main calles on classes
		f = [file[:-4]]
		processMe = f
		processMe = FileManagement(path, hotfolderLocation, fileName)
		savedTextfile = processMe.SaveTxtToFile()
		RemovedCharsSavedTextfile = processMe.removeCharaters(savedTextfile)
		subdir1 = processMe.spliceFileName(RemovedCharsSavedTextfile,0, 2)
		subdir2 = processMe.spliceFileName(RemovedCharsSavedTextfile, 2, 4)
		rootSearchDir = processMe.mainSourceFilesPath
		path_to_subdir1 = processMe.GetFirstSubdirectoryNames(rootSearchDir, subdir1)
		path_to_subdir2 = processMe.GetAdditionalSubDirNames(path_to_subdir1,subdir2)
		finalDestinationPath = processMe.GetFirstSubdirectoryNames(hotfolderLocation, f)
		makeDirToCopyFilesTo = processMe.makeDestinationDirctory(finalDestinationPath)
		grabFiles = processMe.MoveCopyStuff(path_to_subdir2, finalDestinationPath, RemovedCharsSavedTextfile)
		not_found= processMe.AdditionalErrors(RemovedCharsSavedTextfile,finalDestinationPath)
		log = processMe.LogFile(f, finalDestinationPath)
		finish = processMe.MoveOrgFile( hotfolderLocation, finalDestinationPath, file )

		# time stamp end
		timePath = finalDestinationPath[0] + '/' + f[0] + '_log.txt'
		endTime = timeStampObjct.getTime('End Time: \n')
		totalTime = timeStampObjct.getTimeDiffrence(startTime, endTime, 'Total processing Time: \n')
		saveStamptoFile = timeStampObjct.saveTimeToFile(timePath)


	def fredGet_lineart(fileName, path, processMe):
		#main function calls

		# time stamp start
		timeStampObjct = TimeStamp()
		startTime = timeStampObjct.getTime('Start Time: \n')
		#main calles on classes
		f = [file[:-4]]
		processMe = f
		processMe = FileManagement(path, hotfolderLocation, fileName)
		savedTextfile = processMe.SaveTxtToFile()
		RemovedCharsSavedTextfile = processMe.removeCharaters(savedTextfile)
		subdir1 = processMe.spliceFileName(RemovedCharsSavedTextfile,0, 2)
		rootSearchDir = processMe.mainSourceFilesPath
		path_to_subdir1 = processMe.GetFirstSubdirectoryNames(rootSearchDir, subdir1)
		finalDestinationPath = processMe.GetFirstSubdirectoryNames(hotfolderLocation, f)
		makeDirToCopyFilesTo = processMe.makeDestinationDirctory(finalDestinationPath)
		grabFiles = processMe.MoveCopyStuff(path_to_subdir1, finalDestinationPath, RemovedCharsSavedTextfile)
		not_found= processMe.AdditionalErrors(RemovedCharsSavedTextfile,finalDestinationPath)
		log = processMe.LogFile(f, finalDestinationPath)
		finish = processMe.MoveOrgFile(hotfolderLocation, finalDestinationPath, file )

		# time stamp end
		timePath = finalDestinationPath[0] + '/' + f[0] + '_log.txt'
		endTime = timeStampObjct.getTime('End Time: \n')
		totalTime = timeStampObjct.getTimeDiffrence(startTime, endTime, 'Total processing Time: \n')
		saveStamptoFile = timeStampObjct.saveTimeToFile(timePath)










except:
	pass


## Start here
#############################################################################################
try:
	#creates a temp file to check if cron is running
	num =['a']
	for i in num:
		if os.path.isfile(hotfolderLocation + '/temp.txt'):
			break
		else:
			fo = open(hotfolderLocation + '/temp.txt', "w")
			fo.write ("I am a temp file I merely exist. Please leave me be." + '\n')
			fo.close()
			# this is where it figures out what version of the script the operator wants to run
			for file in filesInFolder:
				if 'FredGetTif_Style' in file:
					FredGetTif_Style = file
					f = [file[:-4]]
					fgts =getNewFiles(FredGetTif_Style, path_tiff, f)

				elif 'FredGetTif_Material' in file:
					FredGetTif_Material = file
					f = [file[:-4]]
					fgtm = getNewFiles(FredGetTif_Material, path_tiff, f)

				elif 'FredGetPNG_Style' in file:
					FredGetPNG_Style = file
					f = [file[:-4]]
					fgps = getNewFiles(FredGetPNG_Style, path_png, f)

				elif 'FredGetPNG_Material' in file :
					FredGetPNG_Material = file
					f = [file[:-4]]
					fgpm = getNewFiles(FredGetPNG_Material, path_png, f)

				elif 'FredGetLA_Style' in file:
					FredGetLA_Style = file
					f = [file[:-4]]
					fgls = fredGet_lineart(FredGetLA_Style, path_Nike_Lineart_Library, f)

				elif 'FredGetLA_Material' in file:
					FredGetLA_Material = file
					f = [file[:-4]]
					fglm = fredGet_lineart(FredGetLA_Material, path_Nike_Lineart_Library, f)

				elif 'FredGet_OnBody_TIF_Style' in file:
					FredGet_OnBody_TIF_Style = file
					f = [file[:-4]]
					fgotm = getNewFiles(FredGet_OnBody_TIF_Style, path_OnBody_Catalog_tff, f)

				elif 'FredGet_OnBody_TIF_Material' in file:
					FredGet_OnBody_TIF_Material = file
					f = [file[:-4]]
					fgotm = getNewFiles(FredGet_OnBody_TIF_Material, path_OnBody_Catalog_tff, f)

				elif 'FredGet_OnBody_PNG_Style' in file:
					FredGet_OnBody_PNG_Style = file
					f = [file[:-4]]
					fgops = getNewFiles(FredGet_OnBody_PNG_Style, path_OnBody_Catalog_png, f)

				elif 'FredGet_OnBody_PNG_Material' in file:
					FredGet_OnBody_PNG_Material = file
					f = [file[:-4]]
					fgopm = getNewFiles(FredGet_OnBody_PNG_Material, path_OnBody_Catalog_png, f)


				elif 'FredGetEps' in file:
					FredGetEps = file
					f = [file[:-4]]
					fgEps = getNewFiles(FredGetEps, path_FredGetEps, f)



			#removes the temp file
			os.remove(hotfolderLocation + '/temp.txt')
except:
	pass




def main():
	pass
if __name__ == "__main__": main()



