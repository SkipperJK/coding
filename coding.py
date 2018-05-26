#!usr/bin/python

import os 
import sys
import chardet

count = 0
if sys.getdefaultencoding() != "utf-8":
	reload(sys)
	sys.setdefaultencoding("utf-8")


def reading(path):
	try:
		f = open(path, "r")
		data = f.read()
		# ***
		# data.replace('\r\n', '\n')


		f.close()
		preEncoding = chardet.detect(data)['encoding'].lower()
		# print preEncoding
		if(preEncoding == 'gb2312' or preEncoding == 'gbk' or preEncoding == 'gb18030'):
			uData = data.decode('gb18030')
			return 1, uData
		else:
			return 0, False
	except:
		# print "Reading Error!"
		return -1, False


def writing(path, data):
	try:
		f = open(path, "w")
		f.write(data)
		f.close()
		return 1
	except:
		return -1


def convertCoding(path, recursive=False):
	if os.path.isfile(path):
		if os.path.splitext(path)[1] == '.txt':
			# print "File---"+path
			global count
			count += 1
			status_read, uData = reading(path)
			if status_read == 0:
				print "Already UTF-8 encoding!"
				return 0

			elif status_read == -1:
				print "Reading error!"
				print path
				return 0

			elif status_read == 1:
			# if  uData:
				try:
					data = uData.encode("utf-8")
				# print data
				except:
					print "Data Encode error!"
					print path
					return 0

				status_write = writing(path, data)
				if status_write == 1:
					print "Finish convertCoding!"

				elif status_write == -1:
					print "Writing error!"
					print path
					return 0
					
	elif os.path.isdir(path) == True:
		print "Directory--"+path
		for i in os.listdir(path):
			subPath = os.path.join(path, i)
			# print subPath
			# convertCoding(subPath)
			if recursive:
				convertCoding(subPath, recursive)
			else:
				convertCoding(subPath)

		



def usage():
	print "---------------instruction----------------"
	print "-----1--python xxx(file)------------------"
	print "-----2--python xxx(dir) ------------------"
	print "-----3--python xxx(dir) recursive---------"
	print "------------------------------------------"



if __name__ == '__main__':
	if len(sys.argv) == 1:
		usage()
		exit()
	if len(sys.argv) > 3:
		usage()
		exit()
	path = sys.argv[1]
	if not os.path.exists(path):
		usage()
		print "This file or dir is not exist!"
		exit()
	# cnt = 0
	recursive = (len(sys.argv) == 3 and sys.argv[2] == 'recursive')
	convertCoding(path, recursive)
	print  count


