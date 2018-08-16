#!usr/bin/python

import os 
import sys
import chardet

count = 0
if sys.getdefaultencoding() != "utf-8":
	reload(sys)
	sys.setdefaultencoding("utf-8")
gb = ['gbk', 'gb2312', 'gb18030']


def usage():
	print "---------------Instruction----------------------"
	print "-----1  python coding.py xxx(file)--------------"
	print "-----2  python coding.py xxx(dir) --------------"
	print "-----3  python coding.py xxx(dir) R(recursive)--"
	print "------------------------------------------------"


def reading(path):
	try:
		f = open(path, "rb") 
                #Using rb reading the binary code, aviod coding transfer eror
		data = f.read()
		f.close()
		preEncoding = chardet.detect(data)['encoding'].lower()
		# print preEncoding
                if preEncoding in gb:
			uData = data.decode('gb18030')
			return 1, uData
                else:
                        if preEncoding == 'utf-8': # if file encoding is utf-8, do nothing
                        	return 0, 0
                        else:
                                uData = data.decode(preEncoding)
				return 1, uData
	except:
		return -1, False


def writing(path, data):
	try:
		f = open(path, "w")
		f.write(data)
		f.close()
		return 1
	except:
		return -1


def main(path, recursive=False):
	if os.path.isfile(path):
		if os.path.splitext(path)[1] == '.txt':
			# print "File---"+path
			global count
			count += 1
			status_read, uData = reading(path)
			if status_read == 1:
				try:
					data = uData.encode("utf-8")
				except:
					print "Data Encode error! \n\tFile: %s"%path
					return 0
				status_write = writing(path, data)
				if status_write == 1:
					print "Finish convertCoding!"

				elif status_write == -1:
					print "Writing error! \n\tFile: %s"%path
					return 0
			elif status_read == -1:
				print "Reading error! \n\tFile: %s"%path
				return 0		
	elif os.path.isdir(path) == True:
		print "----Directory----: "+path
		for i in os.listdir(path):
			subPath = os.path.join(path, i)
			if os.path.isdir(subPath) and recursive:
				main(subPath, recursive)
			elif os.path.isfile(subPath):
				main(subPath)


if __name__ == '__main__':
	if len(sys.argv) == 1 or len(sys.argv) > 3:
		usage()
		exit()
	path = sys.argv[1]
	if not os.path.exists(path):
		print "This file or dir is not exist!"
		exit()
	recursive = (len(sys.argv) == 3 and sys.argv[2] == 'R')
	main(path, recursive)
	print  count
