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
    file = request.files['image']
    print(file)
    filename = secure_filename(file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    img = fr.load_image_file(path)
    enc = fr.face_encodings(img)
    for e in enc:
        print(e)
    return "ta bien"


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)