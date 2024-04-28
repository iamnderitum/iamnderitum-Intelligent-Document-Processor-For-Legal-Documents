import os

from flask import Flask, render_template, request, send_from_directory,url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
from . import ner

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(

    )
    app.config["SECRET_KEY"] = "iamnderitu-007"
    app.config["UPLOADED_PHOTOS_DEST"] = "uploads"

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    #app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024
    #app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
    #app.config['UPLOAD_PATH'] = 'uploads'
    app.register_blueprint(ner.bp)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    @app.route('/home')
    def home():
        return "Hello NLP"
    
    class UploadForm(FlaskForm):
        photo = FileField(
            validators = [
                FileAllowed(photos, "Only Images allowed"),
                FileRequired("File field should not be empty")
            ]
        )
        
        submit = SubmitField("Upload")

    @app.route("/uploads/<filename>")
    def get_file(filename):
        return send_from_directory(app.config["UPLOADED_PHOTOS_DEST"], filename)

    @app.route("/", methods = ["GET", "POST"])
    def upload_image():
        form = UploadForm()
        if form.validate_on_submit():
            filename = photos.save(form.photo.data)
            file_url = url_for("get_file", filename=filename)

        else:
            file_url = None
        return render_template("upload_file.html",form=form, file_url=file_url)
    
    return app