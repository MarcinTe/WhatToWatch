import models
from __init__ import db


def insert_genre_to_db(response_genres):
    got_ids = []
    for genre in response_genres:
        if found_genre := models.Genre.query.filter_by(name=genre).first():
            got_ids.append(found_genre.id)
        else:
            new_genre = models.Genre(genre)
            db.session.add(new_genre)
            db.session.commit()
            got_ids.append(new_genre.id)

    return got_ids


def insert_movies_to_db(id, title, year, is_oscar):
    movie = models.Movies(id, title, year, is_oscar)
    db.session.add(movie)
    db.session.commit()
    return movie.id
