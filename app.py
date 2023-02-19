import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
from helpers import allowed_file
from constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

@app.errorhandler(413)
def request_entity_too_large(error):
    return render_template("index.html", error = "File is too large!")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=["GET","POST"])
def upload():
    if request.method == "POST":
        
        file = request.files['image']
        # Check if file exists
        if not file:
            return render_template("index.html", error = "No file received")
        
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):

            filename = secure_filename(file.filename)

            # Create an uploads folder if that folder doesn't exist
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'].rsplit("/")[1])
            
            imageSrc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(imageSrc)
            
            return render_template("resize-image.html", imageName = filename, imageSrc = imageSrc)

        elif not allowed_file(file.filename, ALLOWED_EXTENSIONS):
            return render_template("index.html", error = "Invalid file type")
    else:
        return redirect("/")



@app.route('/resize-image', methods=["GET", "POST"])
def resize_image():

    if request.method == "POST":

        # Check if values exists:
        if not request.form.get("width"):
            return render_template("resize-image.html", error = "Missing Width Input")

        if not request.form.get("height"):
            return render_template("resize-image.html", error = "Missing Height Input")
        
        if not request.form.get("image"):
            return render_template("resize-image.html", error = "No file received")
        
        width = request.form.get("width")
        height = request.form.get("height")
        filename = secure_filename(request.form.get("image"))
        
        (img_width, img_height) = (int(height), int(width))

        # open and process image:
        with Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as image:
            resized_image = image.resize((img_width, img_height))
            
            # make sure uploads folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            resized_filename = f"{width}x{height}_{filename}"
            resized_image.save(os.path.join(app.config['UPLOAD_FOLDER'], resized_filename))
        return send_file(resized_filename)
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
