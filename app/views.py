from app import app
from flask import render_template

@app.route("/")      #default page will be
def index():
    return render_template("index.html")


@app.route("/download")      #default page will be
def download():
    return render_template("download.html")


@app.route("/all")      #default page will be
def all():
    return render_template("all.html")


@app.route("/series")      #default page will be
def series():
    return render_template("series.html")


@app.route("/episode")      #default page will be
def episode():
    return render_template("episode.html")