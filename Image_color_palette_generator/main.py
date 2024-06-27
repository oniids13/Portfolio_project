from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap5
import datetime
import os
import cv2
from sklearn.cluster import KMeans
from collections import Counter


app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/images/uploads/'

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

def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))
def extract_colors(image_path):
    image = cv2.imread(image_path)
    if image is None:
        return None
    image = cv2.imread(image_path)

    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # Perform k-means clustering to find the top 10 colors
    kmeans = KMeans(n_clusters=10, random_state=0)
    kmeans.fit(image)

    # Get the cluster centers (the top 10 colors)
    colors = kmeans.cluster_centers_
    counts = Counter(kmeans.labels_)

    sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    sorted_colors = [colors[i[0]] for i in sorted_counts]

    hex_colors = [rgb_to_hex(color) for color in sorted_colors]

    return hex_colors
@app.route('/', methods=['GET', 'POST'])
def home():
    year = datetime.datetime.now()
    year = year.year
    filepath = None
    sample_path = "C:/Users/Dice08/PycharmProjects/Portfolio_project/Image_color_palette_generator/static/images/sample.jpg"
    colors = extract_colors(sample_path)

    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect('home')
        file = request.files['file']
        if file.name == "":
            return redirect('home')

        filepath = save_upload_file(file, app.config['UPLOAD_FOLDER'])
        if filepath:
            absolute_path = os.path.abspath(filepath)
            print(f"Absolute path of uploaded file: {absolute_path}")
            colors = extract_colors(absolute_path)
            filepath = os.path.relpath(filepath, 'static/images/uploads')

    return render_template("index.html", filepath=filepath, year=year, colors=colors)


if __name__ == '__main__':
    app.run(debug=True)