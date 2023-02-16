import os
from flask import Flask, render_template, request, url_for, send_from_directory, flash, redirect
from werkzeug.utils import secure_filename
from helpers import allowed_file
from PIL import Image

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['jpeg', 'png', 'jpg']
THUMBNAIL_SIZE = (128, 128)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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

        print(f"OS.PATH : {os.path.join(app.config['UPLOAD_FOLDER'], filename)}")

        return render_template("index.html", img_url = img_url)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)


@app.route('/thumbnail', methods=["GET", "POST"])
def thumbnail():
    if request.method == "POST":
        img_url = request.form.get("image")
        target = "." + img_url

        with Image.open(target) as im:

            # Create a thumbnail image
            im.thumbnail(THUMBNAIL_SIZE)
            
            # Naming the end file
            names = img_url.replace("/uploads/", "").rsplit(".")
            thumbnail_name = names[0] + "_thumbnail." + names[1]
            
            # Save image to uploads folder
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_name))
        
        return download_file(thumbnail_name)

