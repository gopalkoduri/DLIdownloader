#!/usr/bin/env python

# @author: Gopala Krishna Koduri, Techsetu (http://techsetu.com)
# @date: 12/April/2010

from fnmatch import fnmatch
import platform
import urllib2
import random
import string
import sys
import os

def download_link(url, filename):
	webFile = urllib2.urlopen(url)
	localFile = open(filename, 'wb')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()
	print "Downloaded",filename

def download_book(URL):
	args = URL.split("?")[1]

	if "&" in args:
		args = args.split("&")
	else:
		print "URL not supported, please read the documentation,\
				re-check the URL and retry."
		sys.exit(0)

	details = {}

	for arg in args:
		arg = arg.split("=")
		if len(arg) == 2:
			details[arg[0].strip()] = arg[1].strip()

	for i in details.keys():
		print i,":",details[i]

	base_URL = "http://www.new.dli.ernet.in"

	for i in xrange(int(details["first"]), int(details["last"])+1):
		cur_URL = base_URL + details["path1"]+"/PTIFF/"+"%08d"%i+".tif"
		download_link(cur_URL, "../files/tiffs/page%04d.tif"%i)
	return [details["first"], details["last"], details["barcode"]]

def main():
	#proxy = urllib2.ProxyHandler({'http': 'http://ee11s077:%58ysV~Q@hproxy.iitm.ac.in:3128'})
	proxy = urllib2.ProxyHandler({'http': 'http://localhost:8123'})
	auth = urllib2.HTTPBasicAuthHandler()
	opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
	urllib2.install_opener(opener)	

	ifile = sys.argv[1]
	URLs = file(ifile, "r").readlines()
	count = 0
	for URL in URLs:
		bookDetails = download_book(URL)
		print "Downloaded a book of", bookDetails[1], "pages"
		count+=1
		if platform.system() == "Windows":
			cmd = os.path.realpath(".")+"../libs/tiff2pdf/tiffcp.exe"
			for i in xrange(int(bookDetails[0]), int(bookDetails[1])+1):
				cmd = cmd+" page%04d.tif"%i
				if i%10 == 0:
					cmd = cmd+" ../files/tiffs/temp.tiff"
					os.system(cmd)
					os.rename("../files/tiffs/temp.tiff", "../files/tiffs/intermediate.tiff")
					cmd = os.path.realpath(".")+"../libs/tiff2pdf/tiffcp.exe intermediate.tiff"
			cmd = cmd+" \"../files/tiffs/%s.tiff\""%(str(bookDetails[2]))
			print cmd
			os.system(cmd)
			os.system(os.path.realpath(".")+"../libs/tiff2pdf/tiff2pdf.exe -o \"../files/pdfs/%s.pdf\" \"../files/tiffs/%s.tiff\""%(bookDetails[2], bookDetails[2]))
		elif platform.system() == "Linux":
			os.system("tiffcp ../files/tiffs/page????.tif \"../files/tiffs/%s.tiff\""%(bookDetails[2]))
			os.system("tiff2pdf -o \"../files/pdfs/%s.pdf\" \"../files/tiffs/%s.tiff\""%(bookDetails[2], bookDetails[2]))
		print "Book binding is done, the book is named as", bookDetails[2]+".pdf", "and is placed in ../files/pdfs/"
		
		#rem = raw_input("Should I remove the temporary tiffs downloaded? (y/N): ");
		#if rem == "y":
		#	for i in os.listdir("."):
		#		if fnmatch(i, "*.tif"):
		#			os.unlink(i)
		#else:
		dirName = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6));
		os.mkdir("../files/tiffs/"+dirName);
		for i in os.listdir("../files/tiffs/"):
			if fnmatch(i, "*.tif"):
				os.rename("../files/tiffs/"+i, "../files/tiffs/"+dirName+"/"+i)
		print "Please note that all the temporary tif files (individual pages) are moved to "+dirName+" folder inside ../files/tiffs/ directory"

if __name__ == '__main__':
	main()
