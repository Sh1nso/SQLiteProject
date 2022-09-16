from flask import Flask, jsonify
from utils import *

app = Flask(__name__)


@app.route('/movie/<title>')
def show_movie_by_name(title):
    data = get_movie_by_name(title)
    return jsonify(data)


@app.route('/movie/<year_one>/to/<year_two>')
def show_movie_by_years(year_one, year_two):
    return jsonify(get_movie_by_years(year_one, year_two))


@app.route('/rating/children')
def show_movies_for_children():
    return jsonify(get_movie_by_rating('G'))


@app.route('/rating/family')
def show_movies_for_family():
    all_movies_for_family = *get_movie_by_rating('G'), *get_movie_by_rating('PG'), *get_movie_by_rating('PG-13')
    return jsonify(all_movies_for_family)


@app.route('/rating/adult')
def show_movies_for_adult():
    all_movies_for_family = *get_movie_by_rating('R'), *get_movie_by_rating('NC-17')
    return jsonify(all_movies_for_family)


@app.route('/genre/<genre>')
def show_movies_by_genre(genre):
    return jsonify(get_movie_by_genre(genre))


if __name__ == "__main__":
    app.run()
