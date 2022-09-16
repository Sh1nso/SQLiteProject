import json
import sqlite3

import flask


def get_movie_by_name(name):
    with sqlite3.connect("netflix.db") as connection:
        data = ["title", "country", "release_year", "genre", "description"]
        cur = connection.cursor()
        a = (name,)
        cur.execute(
            'SELECT title, country, release_year, listed_in, description '
            'FROM netflix '
            'WHERE title = ? AND type = "Movie"'
            , a)

        executed_query = cur.fetchone()
        movie = [i for i in executed_query]
        movie_to_json = dict(zip(data, movie))
    return movie_to_json


def get_movie_by_years(year_one, year_two):
    with sqlite3.connect("netflix.db") as connection:
        list_of_movies = []
        data = ["title", "release_year"]
        cur = connection.cursor()
        a = (year_one, year_two)
        cur.execute(
            'SELECT title, release_year FROM netflix WHERE release_year BETWEEN ? AND ? AND type = "Movie" LIMIT 100'
            , a)
        executed_query = cur.fetchall()
        for movie in executed_query:
            list_of_movies.append(dict(zip(data, movie)))
    return list_of_movies


def get_movie_by_rating(rating):
    with sqlite3.connect("netflix.db") as connection:
        list_of_movies = []
        data = ["title", "rating", "description"]
        cur = connection.cursor()
        a = (rating,)
        cur.execute(
            'SELECT title, rating, description '
            'FROM netflix WHERE rating = ? AND type = "Movie"'
            , a)
        executed_query = cur.fetchall()
        for movie in executed_query:
            list_of_movies.append(dict(zip(data, movie)))
    return list_of_movies


def get_movie_by_genre(genre):
    with sqlite3.connect("netflix.db") as connection:
        list_of_movies = []
        data = ["title", "description"]
        cur = connection.cursor()
        a = ("%" + genre + "%",)
        cur.execute(
            'SELECT title, description FROM netflix '
            'WHERE listed_in LIKE ? ORDER BY release_year DESC LIMIT 10', a)
        executed_query = cur.fetchall()
        for movie in executed_query:
            list_of_movies.append(dict(zip(data, movie)))
    return list_of_movies


# get_cast('Rose McIver', 'Ben Lamb')


def get_movie_by_year_type_genre(genre, movie_type, year):
    with sqlite3.connect("netflix.db") as connection:
        list_of_movies = []
        data = ["title", "description"]
        cur = connection.cursor()
        a = ("%" + genre + "%", movie_type, year)
        cur.execute(
            'SELECT title, description'
            'FROM netflix '
            'WHERE listed_in LIKE ? '
            'AND type = ?'
            'AND release_year = ?', a)
        executed_query = cur.fetchall()
        for movie in executed_query:
            list_of_movies.append(dict(zip(data, movie)))
        list_of_movies_to_json = json.dumps(list_of_movies)
        return list_of_movies_to_json


def get_cast(name1, name2):
    with sqlite3.connect("netflix.db") as connection:
        list_of_actors = []
        format_list = []
        cur = connection.cursor()
        a = ("%" + name1 + ', ' + name2 + "%",)
        cur.execute(
            'SELECT "cast" FROM netflix WHERE "cast" LIKE ?', a)
        executed_query = cur.fetchall()
        [list_of_actors.append(*actor) for actor in executed_query]
        for actor in list_of_actors:
            for i in actor.split(', '):
                if i != name1 and i != name2:
                    format_list.append(i)
        finale_list_of_actors = set([actor for actor in format_list if format_list.count(actor) > 2])

        return list(finale_list_of_actors)


print(get_cast('Rose McIver', 'Ben Lamb'))
