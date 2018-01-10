import os
from flask import Flask, request, redirect, Response
from PIL import Image
import StringIO
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    print(filename)
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.filename = secure_filename(file.filename)
            filetype = file.filename.rsplit('.', 1)[1].lower()
            mimetype = 'image/jpeg'
            if filetype == 'png':
                mimetype = 'image/png'
            else:
                filetype = 'jpeg'
            im = Image.open(file)
            io = StringIO.StringIO()
            im.save(io, format=filetype)
            return Response(io.getvalue(), mimetype=mimetype)
    return '''
        <!doctype html>
        <html>
            <head>
                <title>Upload a Photo</title>
            </head>
            <body>
                <form method=post enctype=multipart/form-data>
                    <p><input type=file name=file>
                    <input type=submit value=Submit>
                </form>
            </body>
        </html>
    '''

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
