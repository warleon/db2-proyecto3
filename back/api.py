from flask import *
from werkzeug.utils import secure_filename

import os
from face import *

#dataPath = "../data/"
#indexPath="../index/Rtree"
#config =index.Property()
#config.dimension = 128
#idx = index.Rtree(indexPath,properties=config,interleaved=False)


app = Flask(__name__)
app.config['MEDIA_FOLDER'] = dataPath
app.config['UPLOAD_FOLDER'] = "./media/"

@app.get('/data/<path:path>')
def send_media(path):
    """
    :param path: a path like "posts/<int:post_id>/<filename>"
    """

    return send_from_directory(directory=app.config['MEDIA_FOLDER'], path=path)

@app.post('/analize')
def analize():
    file = request.files['imagefile']
    KNN =int(request.form['topk'])
    #print(file)
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    img = fr.load_image_file(path)
    enc = fr.face_encodings(img)
    response = []
    for e in enc:
        point = toPoint(e)
        res = idx.nearest(point,KNN,objects=True)
        neightbors = []
        #r attribs : 'bbox', 'bounds', 'get_object', 'handle', 'id', 'object', 'owned'
        for r in res:
            obj = {}
            #the distance with the same object is diferent than 0 because of floating point numbers precision being diferent in each representation
            obj["distance"]=np.linalg.norm(toEnc(r.bbox)-e)
            obj["image"]=r.object.strip("./")
            #obj["encoding"] = toEnc(r.bbox)
            neightbors.append(obj)
        response.append(sorted(neightbors, key=lambda k: k['distance']))
    #print(response)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)