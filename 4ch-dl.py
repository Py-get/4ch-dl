import grequests
import requests
import functools
from bs4 import BeautifulSoup
import re
import sys
import urllib.parse
import os
import argparse

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
    def download(url, r, *args, **kwargs):
        if r.status_code != 200:
            return
        # Splits url, takes the file name from the list (final result in list)
        filename = os.path.split(urllib.parse.urlparse(url).path)[-1]
        # Checks if user requested prefix
        if args.prefix == "No prefix specified":
            print('Downloading: ' + filename)
            # If there's no output path specified
            if args.outputpath == "No output specified":
                # Writes file to disk in chunks sized 1024 each
                with open(filename, "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            else:
                # Opens custom output path
                with open(os.path.join(args.outputpath, filename), "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            print('File: ' + filename + ' downloaded succesfully!')
        else:
            print('Downloading: ' + args.prefix + filename)
            # If there's no output path specified
            if args.outputpath == "No output specified":
                with open(args.prefix + filename, "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            else:
                with open(os.path.join(args.outputpath, args.prefix + filename), "wb") as fd:
                    for chunk in r.iter_content(1024):
                        fd.write(chunk)
            print('File: ' + args.prefix + filename + ' downloaded succesfully!')
        # Prevents "Already Consumed" errors
        r._content_consumed = False

    # Exception handler
    def exc_handler(req, exc):
        print("{} gave error: {}: {}".format(req.url, type(exc).__name__, exc))

    # Defines custom command line arguments, sets -u to be required and displays it in a seperate group entitled required arguments
    parser = argparse.ArgumentParser(prog='4ch-dl', description="Scrape 4chan for files", usage='%(prog)s [options]')
    requiredarg = parser.add_argument_group('required arguments')
    requiredarg.add_argument('-u', '--url', help='Input URL', default='No URL provided')
    parser.add_argument('-o', '--output', help='Specify custom download location', default='No output specified')
    parser.add_argument('-p', '--prefix', help='Specify custom prefix for file names. E.g character names', default='No prefix specified')
    parser.add_argument('-nw', '--nowarning', help='Does not provide a warning when -o is not provided', action='store_true')
    args = parser.parse_args()
    if args.url == 'No URL provided':
        parser.error(
            args.url + '. You must provide atleast one URL using -u\n'
            'Use --help to see a list of all options')
    if args.output == 'No output specified' and args.nowarning is False:
        print('Warning! Will output file to current directory! You did not use -o to specify custom directory. Continue?')
        userinput = input("Y/N ")
        if userinput.lower() == 'y':
            print('Using current directory...')
        else:
            print('Please specify custom directory with the -o command.')
            sys.exit()

    initialscrape = scrape4ch(args.url, "^//i.4cdn")
    listset = list(set(initialscrape.imagelist))
    # Sets up lists, adds http onto them
    finishedlist = []
    for u1 in listset:
        urljoined = urllib.parse.urlparse(args.url, 'http')
        finishedlist.append(urljoined.geturl())
    print(args.url)

    # Uses headers, if it gets a response it runs download with value u.
    fullcommand = [grequests.get(u, headers=hdr, hooks={"response": functools.partial(download, u)}, stream=True) for u in finishedlist]
    grequests.map(fullcommand, exception_handler=exc_handler)
