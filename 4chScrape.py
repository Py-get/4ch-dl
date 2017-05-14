import grequests
import requests
import functools
from bs4 import BeautifulSoup
import re
import sys
import getopt
import urllib.parse
import os

# Sets up headers
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}


class scrape4ch(object):
    # Requires a url and a prefix to be provided.
    def __init__(self, url, prefix):
        print('Gathering links...')
        # Allows custom url and prefix when inputted
        self.url = url
        self.prefix = prefix
        # Forces use of headers, opens url etc.
        self.req = requests.get(self.url, headers=hdr)
        self.soup = BeautifulSoup(self.req.text, "html.parser")
        self.imagelist = []
        # filters href results to match prefix
        for link in self.soup.findAll('a', attrs={'href': re.compile(self.prefix)}):
            self.imagelist.append(link.get('href'))
        print('Links gathered!')


if __name__ == '__main__':
    # Ensures scrape4ch isnt being used in other program
    # Grabs system arguments
    def sysargs(argv):
        arg1 = False
        arg2 = False
        global url1
        global outputpath
        global prefix
        url1 = ''
        outputpath = ''
        prefix = ''
        try:
            opts, args = getopt.getopt(argv, "hu:o:p:", ["help", "url", "output", "prefix"])
        except getopt.GetoptError:
            print('Correct Usage: -u [thread url] -o [output path]. -h to bring up this text. Also accepts --url and --output. Optionally accepts -p or --prefix for character names etc.')
            sys.exit()
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                print('Correct Usage: -u [thread url] -o [output path]. -h to bring up this text. Also accepts --url and --output. Optionally accepts -p or --prefix for character names etc.')
                sys.exit()
            elif opt in ("-u", "--url"):
                # Sets the url to user argument
                url1 = arg
                arg1 = True
            elif opt in ("-o", "--output"):
                outputpath = arg
                arg2 = True
            elif opt in ("-p", "--prefix"):
                prefix = arg
        # Stops user from not specifying input
        if arg1 is False:
            print('Correct Usage: -u [thread url] -o [output path]. -h to bring up this text. Also accepts --url and --output. Optionally accepts -p or --prefix for character names etc.')
            sys.exit()
        # If the user didn't choose output informs them to or will output to home directory
        if arg2 is False:
            print('Warning! Will output file to current directory! You did not use -o to specify custom directory. Continue?')
            userinput = input('Y/N ')
            if userinput.lower() == 'y':
                print('Proceeding to output to current directory...')
            else:
                print('Use command -h to see help text.')
                sys.exit()

    def download(url, r, *args, **kwargs):
        if r.status_code != 200:
            return
        # Splits url, takes the file name from the list (final result in list)
        filename = os.path.split(urllib.parse.urlparse(url).path)[-1]
        # Checks if user requested prefix
        if prefix == "":
            print('Downloading: ' + filename)
            # If there's no output path specified
            if outputpath == "":
                # Writes file to disk in chunks sized 1024 each
                with open(filename, "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            else:
                # Opens custom output path
                with open(os.path.join(outputpath, filename), "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            print('File: ' + filename + ' downloaded succesfully!')
        else:
            print('Downloading: ' + prefix + filename)
            # If there's no output path specified
            if outputpath == "":
                with open(prefix + filename, "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            else:
                with open(os.path.join(outputpath, prefix + filename), "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            print('File: ' + prefix + filename + ' downloaded succesfully!')
        # Prevents "Already Consumed" errors
        r._content_consumed = False

    def exc_handler(req, exc):
        print("{} gave error: {}: {}".format(req.url, type(exc).__name__, exc))

    sysargs(sys.argv[1:])
    initialscrape = scrape4ch(url1, "^//i.4cdn")
    listset = list(set(initialscrape.imagelist))
    finishedlist = []
    for u1 in listset:
        urljoined = urllib.parse.urlparse(u1, 'http')
        finishedlist.append(urljoined.geturl())

    fullcommand = [grequests.get(u, headers=hdr, hooks={"response": functools.partial(download, u)}, stream=True) for u in finishedlist]
    grequests.map(fullcommand, exception_handler=exc_handler)
