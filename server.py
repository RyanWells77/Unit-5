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

@app.route("/users/<user_email>")
def show_user(user_email):

    user = crud.get_user_by_email(user_email)

    return render_template("user_details.html", user= user)

@app.route("/users", methods = ["POST"])
def regester_user():
    
    email = request.form.get("email")
    password = request.form.get("password")
    
    user = crud.get_user_by_email(email)
    if user:
        flash("A user with that email already exists. Please try again.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")

@app.route("/login", methods = ["POST"])
def login_user():

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if user and user.password == password:
        session["user_email"] = user.email
        flash("Logged in!")
    else:
        flash("Invalid email or password. Please try again.")
    
    return redirect("/")


@app.route("/update_rating", methods = ["POST"])
def update_rating():
    rating_id = request.json["ratin_id"]
    update_score = request.json["Updated_score"]
    crud.update_rating(rating_id, update_score)
    db.session.commit()

    return "Rating has been updated."


@app.route("/movies/<movie_id>/ratings", methods=["POST"])
def create_rating(movie_id):
    """Create a new rating for the movie."""

    logged_in_email = session.get("user_email")
    rating_score = request.form.get("rating")

    if logged_in_email is None:
        flash("You must log in to rate a movie.")
    elif not rating_score:
        flash("Error: you didn't select a score for your rating.")
    else:
        user = crud.get_user_by_email(logged_in_email)
        movie = crud.get_movie_by_id(movie_id)

        rating = crud.create_rating(user, movie, int(rating_score))
        db.session.add(rating)
        db.session.commit()

        flash(f"You rated this movie {rating_score} out of 5.")

    return redirect(f"/movies/{movie_id}")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
