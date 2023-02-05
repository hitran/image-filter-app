import os
from flask import Flask, render_template, request, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from helpers import allowed_file

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['jpeg', 'png', 'jpg']

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:

        # Check if the post request has the file part
        if 'imgFile' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        imgFile = request.files['imgFile']

        # If user doesn't select a file, the browser submits an empty file without a filename
        if imgFile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        img_url =''
        if imgFile and allowed_file(imgFile.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(imgFile.filename)
            imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = url_for('download_file', name=filename)

        return render_template("index.html", img_url = img_url)


@app.route('/upload/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)