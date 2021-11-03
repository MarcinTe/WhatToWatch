import requests
import json
from insertion_db import insert_genre_to_db, insert_movies_to_db
import models
from __init__ import db, app

with app.app_context():
    url_details = "https://imdb8.p.rapidapi.com/title/get-details"
    url_genres = "https://imdb8.p.rapidapi.com/title/get-genres"
    url_award = "https://imdb8.p.rapidapi.com/title/get-awards-summary"

    headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': "fe775a9a02msh4ba0e56b2eaabd3p1cc4e6jsnaff5244bfc35"
        }

    querystring = {"tconst": "tt0000001"}

    ids = []
    for i in range(1877833, 1877837):
        value_str = str(i)
        no_digits = len(value_str)
        ids.append('tt' + (7 - no_digits) * '0' + value_str)

    for id in ids:
        new_id = {"tconst":id}
        querystring.update(new_id)

        response_movies = requests.request("GET", url_details, headers=headers, params=querystring)
        response_genre = requests.request("GET", url_genres, headers=headers, params=querystring)
        response_award = requests.request("GET", url_award, headers=headers, params=querystring)

        response_movies_dict = json.loads(response_movies.text)
        response_genres = json.loads(response_genre.text)
        response_award_dict = json.loads(response_award.text)

        got_genres = insert_genre_to_db(response_genres)

        title = response_movies_dict['title']
        year = response_movies_dict['year']
        award = response_award_dict['awardsSummary']

        is_oscar = False
        try:
            award_name = response_award_dict['awardsSummary']['highlighted']['awardName']
        except KeyError:
            print("No oscar here")
        else:
            if award_name == 'Oscar':
                is_oscar = True

        movie_id = insert_movies_to_db(id, title, year, is_oscar)

        for genre_id in got_genres:
            movieGenre = models.MovieGenre(movie_id, genre_id)
            db.session.add(movieGenre)
            db.session.commit()
