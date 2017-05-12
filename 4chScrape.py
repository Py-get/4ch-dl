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
#gets url to pars into 4ch class				
url1 = input("Input thread url: \n")
initialscrape = scrape4ch(url1, "^//i.4cdn", "http:")

#y = position in list. Starting with first.
y = 0
#Allows for inputting custom prefix eg. character names
customfilename = input('Use custom file name prefix? Y/N \n')
if customfilename.lower() == 'y':
	definecustomfilename = input('Enter custom filename prefix: \n')
	print('Using prefix %s ' % (definecustomfilename))
else:
	print('Will not use custom filename prefix')
#Sets up path to download to
myPath = input("Input folder to download to: \n")

#Main loop to run code in	
for urlget in initialscrape.memelist:
	#Grabs from list of urls in position y which is increased per repeat
	url2 = initialscrape.memelist[y]
	#splits up results in order to grab final file name
	urlfilename = url2.split('/')
	#increases list position by 1
	y = y + 1
	#Lets user know when is downloading
	try:
		if customfilename.lower() == 'y':
			print('Downloading: ' + definecustomfilename + urlfilename[-1])
			#Joins to requested path, filename is the final name hosted on 4ch
			fullfilename = os.path.join(myPath, definecustomfilename + urlfilename[-1])
			runcommand = urllib.request.urlretrieve(url2, fullfilename)
			print('File has been succesfully downloaded!')
		else:
			print('Downloading: ' + urlfilename[-1])
			fullfilename = os.path.join(myPath, urlfilename[-1])
			runcommand = urllib.request.urlretrieve(url2, fullfilename)
			print('File has been succesfully downloaded!')
	except:
		print('File could not be downloaded')
