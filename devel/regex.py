from Tkinter import *
import re


results = open("sample_results.txt", "r")

for line in results:
    if re.match("(.*)test(.*)", line):
        print line
    if re.match("(.*)number(.*)", line):
        print line
    if re.match("(.*)status(.*)", line):
        print line
    if re.match("(.*)length(.*)", line):
        print line