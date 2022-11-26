import face_recognition as fr
import os
import numpy as np
from rtree import index
import time
import heapq
from heapq import heappush, heappop
from sklearn.neighbors import KDTree
import pandas as pd

allowedExtensions = [".jpg"]
encoding_results = list()
encoding_directory = list()
direction = "/content/db2-proyecto3/data/"
dataPath = "../data/"
indexPath="../index/Rtree"
config =index.Property()
config.dimension = 128
idx = index.Rtree(indexPath,properties=config,interleaved=False)

def toEnc(vec):
    c = vec[0::2]
    return c
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

def doIndexing1(rootdir, N=10):
    count = 0
    i=0
    for subdir, dirs, files in os.walk(rootdir):
        if i==N:
           break
        for file in files:
                filename, fileExtension = os.path.splitext(file)
                if fileExtension.lower() in allowedExtensions:
                     path = os.path.join(subdir, file)
                     img = fr.load_image_file(path)
                     enc = fr.face_encodings(img)
                     encoding_results.append(enc[0])
                     encoding_directory.append(path)
        i = i + 1

def sequential_search(image_encoding, k):
    global encoding_directory
    priority_queue = []
    distances = fr.face_distance(encoding_results, image_encoding[0])
    for i in range(len(distances)):
        heappush(priority_queue, (-distances[i], encoding_directory[i]))
        if(len(priority_queue) > k):
            heappop(priority_queue)
    answers = sorted(priority_queue, key=lambda tup: tup[0], reverse=True)
    return answers

def range_search(image_encoding, r):
    global encoding_directory
    result = list()
    distances = fr.face_distance(encoding_results, image_encoding[0])
    for i in range(len(distances)):
        if distances[i]<=r:
            result.append((distances[i],encoding_directory[i]))
    result.sort(key = lambda tup: tup[0]) 
    return result


def knn_sequential(image_directory, k):
    image_encoding = fr.face_encodings(fr.load_image_file(image_directory))
    t1= time.time()
    sequential_results = sequential_search(image_encoding, k)
    t2 = time.time()
    ans = [x[1] for x in sequential_results]
    return (ans, round(t2-t1,6))

def knn_range(image_directory, r):
    image_encoding = fr.face_encodings(fr.load_image_file(image_directory))
    t1 = time.time()
    range_results = range_search(image_encoding, r)
    t2 = time.time()
    ans = [x[1] for x in range_results]
    return (ans, round(t2-t1,6))

def time_knn_rtree(N=10):
    i=0
    rindex = index.Rtree(properties=config,interleaved=False)
    last =None
    for subdir, dirs, files in os.walk(rootdir):
        if i==N:
           break
        for file in files:
            path = os.path.join(subdir, file)
            img = fr.load_image_file(path)
            enc = fr.face_encodings(img)
            for e in enc:
                p = toPoint(e)
                rindex.insert(0, p)
                last =p
                i = i + 1
    t1 = time.time()
    rtree.nearest(p,8)
    t2 = time.time()
    return round(t2-t1,6)

def generate_table():
   df = pd.DataFrame(encoding_results)
   df['paths'] = encoding_directory 
   return df


def KDTree_HighD(image_name, k):
    t1= time.time()
    image = fr.load_image_file(image_name)
    faces = fr.face_encodings(image)
    kd_tree = KDTree(df[df.columns[:-1]])
    result = kd_tree.query([faces[0]], k)
    ans = result[1][0]
    t2= time.time()
    return ([df.iloc[ans[i], -1] for i in range(k)],round(t2-t1,6))


#if __name__=="__main__":
	#index already done :v
	#doIndexing1(direction,10)
	#df = generate_table()
	#doIndexing(dataPath)
