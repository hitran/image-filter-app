from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from werkzeug.utils import secure_filename
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=["GET","POST"])
def upload():
    if request.method == "POST":
        
        # Check if file exists
        if not request.files['image']:
            return render_template("index.html", error = "No file received")
        
        file = request.files['image']
        filename = secure_filename(file.filename)

        # Create an uploads folder if that folder doesn't exist
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'].rsplit("/")[1])
        
        imageSrc = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(imageSrc)

        return render_template("resize_image.html", imageName = filename, imageSrc = imageSrc)
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
        
        img_size = (int(height), int(width))

        # open and process image:
        with Image.open(os.path.join(app.config['UPLOAD_FOLDER'],filename)) as image:
            image.thumbnail(img_size)
            
            # make sure uploads folder exists
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            
            thumbnail_filename = f"{width}x{height}_{filename}"
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnail_filename))
        return send_file(thumbnail_filename)
    else:
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
