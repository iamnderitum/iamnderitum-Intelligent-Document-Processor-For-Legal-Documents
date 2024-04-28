import functools
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint("ner", __name__, url_prefix="/ner")


@bp.route("/upload")
def entity_recognition():
    return render_template("upload_file.html")

@bp.route("/upload", methods=["POST"])
def upload_file():
    uploaded_file = request.files["file"]
    if uploaded_file.filename != "":
        uploaded_file.save(os.path.join("static/images"))

    return(url_for("ner"))

def ner():
    image_path = "../uploads/"
    return render_template("ner.html")

