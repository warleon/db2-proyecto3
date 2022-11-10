import face_recognition as fr
import os
import numpy as np
from rtree import *

allowedExtensions = ["jpg"]

idx = index.Index()
def addPoint(data,vec):
	idx.insert(data,np.repeat(vec,2))

def doIndexing(rootdir):
	for subdir, dirs, files in os.walk(rootdir):
    for file in files:
				filename, fileExtension = os.path.splitext(file)
				if fileExtension.lower() in allowedExtensions:
					print(os.path.join(subdir, file))