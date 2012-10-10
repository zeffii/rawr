# domocless.py
import os, shutil

#print(dir(os))

#a = item for item in os.listdir() if item.
#print(a)
am = shutil.os.walk(".")

while(True):
	try:
		print(next(am))
	except:
		pass