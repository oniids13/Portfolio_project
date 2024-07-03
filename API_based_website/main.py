from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)

MOVIE_API = "e51b75b59a928ffc4d072a95927442c9"
MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
SEARCH_URL = "https://api.themoviedb.org/3/movie"
POPULAR_MOVIE_URL = "https://api.themoviedb.org/3/movie/popular"


class SearchForm(FlaskForm):
    movie = StringField("Movies",validators=[DataRequired()], render_kw={"placeholder": "Movie Name"})
    submit = SubmitField()





@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()

    params = {
        "api_key": MOVIE_API,
        "query": 1
    }
    response = requests.get(POPULAR_MOVIE_URL, params=params)
    data = response.json()
    movie_result = data["results"][:10]
    top_movies = []
    for result in movie_result:
        img_url = f"https://image.tmdb.org/t/p/w500{result['poster_path']}"
        title = result["original_title"]
        year = result["release_date"].split("-")[0]
        description = result["overview"]
        movie_id = result["id"]
        top_films = {
            "img_url": img_url,
            "title": title,
            "year": year,
            "description": description,
            "movie_id": movie_id
        }
        top_movies.append(top_films)



    if request.method == 'POST':
        query = request.form.get("movie")
        params={
            "api_key": MOVIE_API,
            "query": query,
        }
        response = requests.get(MOVIE_URL, params=params)
        data = response.json()
        result = data["results"]
        movie_data = []
        for movie in result:
            title = movie["original_title"]
            year = movie["release_date"]
            movie_id = movie["id"]
            selection = {
                "title": title,
                "year": year,
                "movie_id": movie_id
            }
            movie_data.append(selection)
        session['movie_data'] = movie_data
        return redirect(url_for('movie'))

    return render_template("index.html", form=form, top_movies=top_movies)


@app.route('/select/<int:movie_id>', methods=["GET", "POST"])
def select(movie_id):

    if movie_id:
        response = requests.get(f"{SEARCH_URL}/{movie_id}", params={"api_key": MOVIE_API})
        data = response.json()
        img_url = f"https://image.tmdb.org/t/p/w500{data['poster_path']}" if isinstance(data['poster_path'], str) else f"https://image.tmdb.org/t/p/w500{data['poster_path'][0]}"
        title = data["title"] if isinstance(data["title"], str) else data["title"][0]
        year = data["release_date"].split("-")[0] if isinstance(data["release_date"], str) else \
        data["release_date"][0].split("-")[0]
        description = data["overview"] if isinstance(data["overview"], str) else data["overview"][0]
        genre = data["genres"][0]["name"]
        popularity = round(data["popularity"], 2)
        runtime = data["runtime"]

        selected_movie = {
            "img_url": img_url,
            "title": title,
            "year": year,
            "description": description,
            "genres": genre,
            "popularity": popularity,
            "runtime": runtime
        }
        print(selected_movie)

        return render_template("select.html", movie=selected_movie)


@app.route('/movie')
def movie():
    movie_data = session.get('movie_data')
    return render_template("movie.html", movie_data=movie_data)

if __name__ == '__main__':
    app.run(debug=True)