import numpy as np
import pandas as pd
import os
import glob





indir = 'TestResults/Compression/dataAnalysis'
for root, dirs, filenames in os.walk(indir):
	for f in filenames:
		f2 = open('TestResults/Compression/dataAnalysis/'+f,'r')
		for line in f2:
			if 'Data:' in line:
				print(line)

	#end of each text file


#f = open('TestResults/Compression/dataAnalysis/8323.txt')
#for line in f:
#	print(line)