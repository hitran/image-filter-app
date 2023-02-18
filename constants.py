UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
ACTION_LIST = [
    {
        "value": "thumbnail",
        "name": "Generate Thumbnail",
        "url": "/resize-image",
        "html": "resize-image.html"
    },
    {
        "value": "filter",
        "name": "Filter Image",
        "url": "/filter-image",
        "html": "filter-image.html"
    }
]