#/usr/bin/env python

# if a script with my name is running, kill it, then exit
# if a script with my name is not running, do stuff
# really cool !! (PK)

from os import getpid
from sys import argv, exit
import psutil  ## pip install psutil

myname = argv[0]
mypid = getpid()
for process in psutil.process_iter():
    if process.pid != mypid:
        for path in process.cmdline():
            if myname in path:
                print "process found"
                process.terminate()
                exit()

## your program starts here..
while True:
    print "I'm running"