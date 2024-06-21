from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cafe")
def cafe():
    return render_template("cafe.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")






if __name__ == '__main__':
    app.run(debug=True)