
def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in allowed_extensions

            
def create_thumbnail(imgFile, size):
    return imgFile.thumbnail(size)