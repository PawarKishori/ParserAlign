#first create 100/300 files containing hindi sentences
#running this script will change the format of each sentence file based on '.'
#then run the hindi parser through these 100/300 files containing hindi sentences

import re
import sys
import glob

name = '/home/ashwin/Documents/tmp/CRIMEH_0/1.*/hindi_dep_parse_original.txt'  #path to separate hindi sentence
files = glob.glob(name)

for name in files:
    #print(name)
	f = open(name,"r")
	text = f.read()
	sent = re.split('(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)(\s|[A-Z].*)',text)
	f.close()
	#path = '/home/ashwin/Documents/tmp/CRIMEH_0/1.1/my_output.txt' #path to output file
	f1 = open(name,"w")

	for i in sent:
		if(i!=" "):
			f1.write(i)
			f1.write('\n')   #this will replace the file in the format
	f1.close()
