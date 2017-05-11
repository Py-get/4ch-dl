from urllib.request import urlopen
from bs4 import BeautifulSoup
import urllib.request
import re
import random
import os

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


class scrape4ch(object):
	#Requires a url and a prefix to be provided. Provides support for broken http:// redirects but not a necessity
	def __init__(self, url, prefix, httpaddition=None):
		#Allows custom url and prefix when inputted
		self.url = url
		self.prefix = prefix
		self.httpaddition = httpaddition
		#Forces use of headers, opens url etc.
		self.req = urllib.request.Request(self.url, headers=hdr)
		self.content = urlopen(self.req).read()
		self.soup = BeautifulSoup(self.content, "html.parser")
		#creates list
		self.memelist = []
		#filters href results to match prefix
		for link in self.soup.findAll('a', attrs={'href': re.compile(self.prefix)}):
			if self.httpaddition == None:
				self.memelist.append(link.get('href'))
			else:
		#checks for optional prefix and adds, adds result onto list
				self.meme = self.httpaddition + link.get('href')
				self.memelist.append(self.meme)	
				
url1 = input("Input thread url: \n")
initialscrape = scrape4ch(url1, "^//i.4cdn", "http:")
listsize = len(initialscrape.memelist)
x = 1
y = 0
customfilename = input('Use custom file name? Y/N \n')
if customfilename.lower() == 'y':
	definecustomfilename = input('Enter custom filename prefix: \n')
	print('Using prefix %s \n' % (definecustomfilename))
else:
	print('Will not use custom filename prefix')
myPath = input("Input folder to download to: \n")
	
while True:
	url2 = initialscrape.memelist[y]
	urlfilename = initialscrape.memelist[y].split('/')
	if customfilename.lower() == 'y':
		print('Downloading: ' + definecustomfilename + urlfilename[4])
		fullfilename = os.path.join(myPath, definecustomfilename + urlfilename[4])
		runcommand = urllib.request.urlretrieve(url2, fullfilename)
	else:
		print('Downloading: ' + urlfilename[4])
		fullfilename = os.path.join(myPath, urlfilename[4])
		runcommand = urllib.request.urlretrieve(url2, fullfilename)
	y = y + 1
	x = x + 1
	listsize = listsize - 1
	print('File has been succesfully downloaded!')
	if listsize == 0:
		break