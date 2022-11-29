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
	# c = np.zeros((vec.size + vec.size), dtype=vec.dtype)
	# c[0::2] = vec
	# c[1::2] = vec#+np.finfo(np.float32).eps
	# return c
    return np.repeat(vec,2)

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
    res = rtree.nearest(last,8)
    t2 = time.time()
    return (res,round(t2-t1,6))

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

def experimentation():
  list_answers = [[],[]]
  for i in [100,200,400,800,1600,3200,6400,12800]:
    allowedExtensions = [".jpg"]
    encoding_results = list()
    encoding_directory = list()
    doIndexing1("/content/db2-proyecto3/data/", i)
    for j in ["KNN_KDTree","knn_sequential"]:
      ans = 0
      if(j=="KNN_KDTree"):
        scaler = StandardScaler()
        scaler.fit(encoding_results)
        encodings_normalized = scaler.transform(encoding_results)
        pca = PCA(50)
        pca.fit(encodings_normalized)
        encodings_pca = pca.transform(encodings_normalized)
        df = pd.DataFrame(encodings_pca)
        df['paths'] = encoding_directory
       
        for k in range(4):
          image = fr.load_image_file('/content/db2-proyecto3/data/Dwayne_Wade/Dwayne_Wade_0001.jpg')
        
          faces = fr.face_encodings(image)
          face_norm = scaler.transform(faces[0].reshape(1, -1))
          face_pca = pca.transform(face_norm)
          a=df[df.columns[:-1]]
        
          kd_tree = KDTree(a)
          t1= time.time()
          result = kd_tree.query([face_pca[0]], 8)
          t2= time.time()
          #t = KNN_KDTree('/content/db2-proyecto3/data/Dwayne_Wade/Dwayne_Wade_0001.jpg',8)[1]
          ans = ans + round(t2-t1,6)
        ans= ans/4.0
        list_answers[1].append(ans)
      if(j=="knn_sequential"):
        for k in range(4):
        
          priority_queue = []
          image_encoding = fr.face_encodings(fr.load_image_file('/content/db2-proyecto3/data/Dwayne_Wade/Dwayne_Wade_0001.jpg'))
          distances = fr.face_distance(encoding_results, image_encoding[0])
          t1= time.time()
          for i in range(len(distances)):
              heappush(priority_queue, (-distances[i], encoding_directory[i]))
              if(len(priority_queue) > 8):
                 heappop(priority_queue)
          answers = sorted(priority_queue, key=lambda tup: tup[0], reverse=True)
          t2= time.time()
          ans = ans + round(t2-t1,6)
        ans = ans/4.0
        list_answers[0].append(ans)
    print(list_answers)  
#if __name__=="__main__":
	#index already done :v
	#doIndexing1(direction,10)
	#df = generate_table()
	#doIndexing(dataPath)
