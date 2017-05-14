# 4chan Image Scraper (Python)

Simple image scraper that downloads images from the imageboard 4chan. Ideal usage is downloading from specific threads.

## Usage:

To mass download images from specific thread:
```
4chScrape.py -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2 -o C:\Users\UserName\Downloads\cm\ImageScraped\testrun
```
To append prefix to filename, allowing for easy sorting and/or labelling character names:
```
4chScrape.py -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2 -o C:\Users\UserName\Downloads\cm\ImageScraped\testrun -p 9s
```
To output to current directory:
```
4chScrape.py -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2
```
Long command names for the easily forgetful:
```
--help
--url
--output
--prefix
```


### Warnings and credits:

**Please Note:** 
Due to technical limitations I have been unable to test this on a Unix environment and cannot guarantee it will work. The only OS this has been run on is Windows 7. 

Huge thanks to reddit user destiny_functional for helping me troubleshoot the script and convert to grequests.
