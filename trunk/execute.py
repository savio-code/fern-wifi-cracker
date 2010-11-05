import os
import sys
import commands

variable = sys.argv[0]
direc = variable.replace('execute.py',"")
os.system('cd %s \n python fern.py'%(direc))

