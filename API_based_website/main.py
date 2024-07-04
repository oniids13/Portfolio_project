from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired



app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET"
Bootstrap5(app)

MOVIE_API = "e51b75b59a928ffc4d072a95927442c9"
MOVIE_URL = "https://api.themoviedb.org/3/search/movie"
TV_URL = "https://api.themoviedb.org/3/search/tv"
SEARCH_MOVIE_URL = "https://api.themoviedb.org/3/movie"
SEARCH_TV_URL = "https://api.themoviedb.org/3/tv"
POPULAR_MOVIE_URL = "https://api.themoviedb.org/3/movie/popular"
POPULAR_TV_URL = "https://api.themoviedb.org/3/tv/popular"
TRENDING_URL = "https://api.themoviedb.org/3/trending/all/day"

class SearchForm(FlaskForm):
    movie = StringField("Movies",validators=[DataRequired()], render_kw={"placeholder": "Movie Name"})
    submit = SubmitField()





@app.route("/", methods=["GET", "POST"])
def home():
    form = SearchForm()
    # For TOP movies
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

    # For top TV
    params2 = {
        "api_key": MOVIE_API,
        "query": 1
    }
    response2 = requests.get(POPULAR_TV_URL, params=params)
    data2 = response2.json()
    tv_result = data2["results"][:10]
    top_tv_show = []
    for result in tv_result:
        img_url = f"https://image.tmdb.org/t/p/w500{result['poster_path']}"
        title = result["original_name"]
        year = result["first_air_date"].split("-")[0]
        description = result["overview"]
        tv_id = result["id"]
        top_tv = {
            "img_url": img_url,
            "title": title,
            "year": year,
            "description": description,
            "tv_id": tv_id
        }
        top_tv_show.append(top_tv)

    # Trending
    response3 = requests.get(TRENDING_URL, params={"api_key": MOVIE_API})
    data3 = response3.json()
    result3 = data3["results"]
    trending = []
    for x in result3:
        img_url = f"https://image.tmdb.org/t/p/w500{x['poster_path']}"
        media = x["media_type"].capitalize()
        trend_id = x["id"]
        try:
            title = x["name"]
        except:
            title = x["title"]
        try:
            year = x["release_date"].split("-")[0]
        except:
            year = x["first_air_date"].split("-")[0]
        trend = {
            "img_url": img_url,
            "title": title,
            "media_type": media,
            "trend_id": trend_id,
            "year": year
        }
        trending.append(trend)

    return render_template("index.html", form=form, top_movies=top_movies, top_tv_show=top_tv_show, trending=trending)

@app.route("/search/movie", methods=["POST"])
def search_movie():
    query = request.form.get("query")
    params = {"api_key": MOVIE_API, "query": query}
    response = requests.get(MOVIE_URL, params=params)
    data = response.json()
    result = data["results"]
    movie_data = []
    for movie in result:
        title = movie["original_title"]
        year = movie["release_date"]
        movie_id = movie["id"]
        movie_data.append({
            "title": title,
            "year": year,
            "movie_id": movie_id
        })
    session['movie_data'] = movie_data
    session.pop('tv_data', None)  # Clear TV data
    return redirect(url_for('select'))


@app.route("/search/series", methods=["POST"])
def search_series():
    query = request.form.get("query")
    params = {"api_key": MOVIE_API, "query": query}
    response = requests.get(TV_URL, params=params)
    data = response.json()
    result = data["results"]
    tv_data = []
    for tv in result:
        title = tv["original_name"]
        year = tv["first_air_date"]
        tv_id = tv["id"]
        tv_data.append({
            "title": title,
            "year": year,
            "tv_id": tv_id
        })
    session['tv_data'] = tv_data
    session.pop('movie_data', None)  # Clear movie data
    return redirect(url_for('select'))



@app.route('/movie/<int:movie_id>', methods=["GET", "POST"])
def movie(movie_id):

    if movie_id:
        response = requests.get(f"{SEARCH_MOVIE_URL}/{movie_id}", params={"api_key": MOVIE_API})
        data = response.json()
        img_url = f"https://image.tmdb.org/t/p/w500{data['backdrop_path']}" if isinstance(data['backdrop_path'], str) else f"https://image.tmdb.org/t/p/w500{data['backdrop_path'][0]}"
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

        return render_template("movie.html", movie=selected_movie)


@app.route('/tv_show/<int:tv_id>', methods=["GET", "POST"])
def tv_show(tv_id):

    if tv_id:
        response = requests.get(f"{SEARCH_TV_URL}/{tv_id}", params={"api_key": MOVIE_API})
        data = response.json()
        img_url = f"https://image.tmdb.org/t/p/w500{data['backdrop_path']}" if isinstance(data['backdrop_path'], str) else f"https://image.tmdb.org/t/p/w500{data['backdrop_path'][0]}"
        title = data["name"] if isinstance(data["name"], str) else data["name"][0]
        year = data["first_air_date"].split("-")[0] if isinstance(data["first_air_date"], str) else \
        data["first_air_date"][0].split("-")[0]
        description = data["overview"] if isinstance(data["overview"], str) else data["overview"][0]
        genre = data["genres"][0]["name"]
        popularity = round(data["popularity"], 2)
        no_of_episodes = data["number_of_episodes"]
        no_of_seasons = data["number_of_seasons"]


        selected_tv = {
            "img_url": img_url,
            "title": title,
            "year": year,
            "description": description,
            "genres": genre,
            "popularity": popularity,
            "no_of_episodes": no_of_episodes,
            "no_of_seasons": no_of_seasons
        }

        return render_template("tv_show.html", tv=selected_tv)

@app.route('/select')
def select():
    movie_data = session.get('movie_data')
    tv_data = session.get('tv_data')
    return render_template("select.html", movie_data=movie_data, tv_data=tv_data)

if __name__ == '__main__':
    app.run(debug=True)