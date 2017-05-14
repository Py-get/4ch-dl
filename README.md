# 4ch-dl

Simple image scraper that downloads images from the imageboard 4chan. Ideal usage is downloading from specific threads.

## Installation:
Download latest executable off of the Releases page. I recommend using Cygwin and copying the file to ```C:\cygwin64\bin``` however you can copy the executable to your System32 directory as well and then run 4ch-dl in cmd. Otherwise you can open the executable through your command prompt of choice.

Linux users see Warnings and Credits, however hopefully the .py file should run through your terminal as long as you have the requirements installed.

## Usage:

To mass download images from specific thread:
```
4ch-dl -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2 -o C:\Users\UserName\Downloads\cm\ImageScraped\testrun
```
To append prefix to filename, allowing for easy sorting and/or labelling character names:
```
4ch-dl -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2 -o C:\Users\UserName\Downloads\cm\ImageScraped\testrun -p 9s
```
To output to current directory:
```
4ch-dl -u http://boards.4chan.org/cm/thread/3103477/nier-automata-9s-pt2
```
Long command names for the easily forgetful:
```
--help
--url
--output
--prefix
```


## Warnings and Credits:

**Please Note:** 
Due to technical limitations I have been unable to test this on a Unix environment and cannot guarantee it will work. The only OS this has been run on is Windows 7. 

Huge thanks to reddit user destiny_functional for helping me troubleshoot the script and convert to grequests.


### Fun Fact:
The first version of this script was created in under a day. It was later updated to be PEP-8 compliant the following day, and over the next two days rewritten from the ground up to work with command line arguments and grequests.
