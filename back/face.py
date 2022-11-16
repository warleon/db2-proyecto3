import face_recognition as fr
import os
import numpy as np
from rtree import index

allowedExtensions = [".jpg"]

dataPath = "../data/"
indexPath="../index/Rtree"
config =index.Property()
config.dimension = 128
idx = index.Rtree(indexPath,properties=config,interleaved=False)

def toPoint(vec):
	c = np.zeros((vec.size + vec.size), dtype=vec.dtype)
	c[0::2] = vec
	c[1::2] = vec#+np.finfo(np.float32).eps
	return c

def doIndexing(rootdir):
	count = 0
	for subdir, dirs, files in os.walk(rootdir):
		for file in files:
				filename, fileExtension = os.path.splitext(file)
				if fileExtension.lower() in allowedExtensions:
					path = os.path.join(subdir, file)
					img = fr.load_image_file(path)
					enc = fr.face_encodings(img)
					for e in enc:
						count+=1
						p = toPoint(e)
						idx.insert(count, p,obj=path)
						print("indexed:",path,"with id",count)


#if __name__=="__main__":
	#index already done :v
	#doIndexing(dataPath)