from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
import datetime
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads/'
Bootstrap5(app)

IMG_PATH = ""

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def save_upload_file(file, upload_folder):
    if file:
        filepath = os.path.join(upload_folder, file.filename)
        file.save(filepath)
        return filepath
    return None



@app.route('/', methods=['GET', 'POST'])
def home():
    year = datetime.datetime.now()
    year = year.year
    filepath = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.name == "":
            return 'No selected file'
        filepath = save_upload_file(file, app.config['UPLOAD_FOLDER'])
        print(filepath)

    return render_template("index.html", file=filepath, year=year)






if __name__ == '__main__':
    app.run(debug=True)