	#
	def fredGetEps(fileName, path, processMe):
		#main function calls
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
		processMe = hotfolder_location[0] + '/' + fileName
		#reads the text file
		myCsvFile = Csv_fo.readCsvFile(processMe)
		myCsvFile = Csv_fo.cleanXtraReturns(myCsvFile)
		col_a_season_dir = Csv_fo.getColumn(myCsvFile,0)
		col_b_img_num = Csv_fo.getColumn(myCsvFile, 1)

		# gets sub dir names from columns in test file
		subdir1 = fmo.spliceFileName(col_b_img_num,0, 2)
		subdir2 = fmo.spliceFileName(col_b_img_num, 2, 4)
