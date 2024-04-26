"""Server for movie ratings app."""

from flask import (Flask, render_template, request, flash, session,redirect)
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.app_context().push()
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def home():

    return render_template("home.html")

@app.route("/movies")
def all_movies():

    movies = crud.get_movies()

    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def show_movies(movie_id):

    movie = crud.get_movie_by_id(movie_id)

    return render_template("movie_details.html", movie=movie)

@app.route('/users')
def all_users():

    users = crud.get_users()

    return render_template("all_users.html", users=users)


# Replace this with routes and view functions!


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
