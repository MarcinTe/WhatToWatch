import random
from flask import render_template, redirect, url_for, Blueprint, request, session, flash
from .models import Users, Genre, MovieGenre, Movies
from . import db
from datetime import date
import datetime

home_blueprint = Blueprint('home_blueprint', __name__)
sing_up_blueprint = Blueprint('sing_up_blueprint', __name__)
login_blueprint = Blueprint('login_blueprint', __name__)
account_blueprint = Blueprint('account_blueprint', __name__)
settings_blueprint = Blueprint('settings_blueprint', __name__)
how_it_works_blueprint = Blueprint('how_it_works_blueprint', __name__)
result_blueprint = Blueprint('result_blueprint', __name__)


@home_blueprint.route("/", methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@sing_up_blueprint.route('/sing_up', methods=['POST', 'GET'])
def sing_up():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        new_user = Users.query.filter_by(name=name, email=email, password=password).first()

        if not new_user:
            register_data = date.today()
            new_user = Users(name=name, email=email, password=password, register_data=register_data)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_blueprint.login'))

        flash("The email you entered is already taken. Try another one")
        return redirect(url_for('sing_up_blueprint.sing_up'))

    if request.method == 'GET':
        return render_template('sign_up.html')


@login_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        session.update({'name': request.form['name']})
        found_user = Users.query.filter_by(name=name, password=password).first()
        if found_user:
            return redirect(url_for('account_blueprint.account', name=name))

    return render_template('login.html')


@account_blueprint.route('/account', methods=['POST', 'GET'])
def account():
    current_data = datetime.datetime.today()
    name = session.get('name')
    user = Users.query.filter_by(name=name).first()
    register = user.register_data
    dif = current_data - register
    name = request.args['name']
    return render_template('account.html', name=name, dif=dif)


@settings_blueprint.route('/settings', methods=['POST', 'GET'])
def settings():
    if request.method == 'POST':
        genre_form = request.form['category']
        years = request.form['time_interval']
        oscar = request.form['oscar']
        if oscar == 'Yes':
            int_oscar = 1
        elif oscar == 'No':
            int_oscar = 0

        year1 = int(years[:4])
        year2 = int(years[6:])

        found_genre_id = Genre.query.filter_by(name=genre_form).first().id
        movie_genre_records = MovieGenre.query.filter_by(id_genre=found_genre_id).all()
        movie_ids = []
        movies = []
        final_movies = []
        for movieGenre in movie_genre_records:
            movie_ids.append(movieGenre.id_movie)
        for movie_id in movie_ids:
            movie = Movies.query.filter_by(id=movie_id).first()
            movies.append(movie)
        for movie in movies:
            if movie.oscar_rewarded == int_oscar and movie.year in range(year1, year2):
                final_movies.append(movie)

        movie_choice = "Such movie not found :("
        if len(final_movies) != 0:
            movie_choice = random.choice(final_movies)

        return redirect(url_for('result_blueprint.result', movie_choice=movie_choice))
    return render_template('settings.html')


@result_blueprint.route('/result', methods=['POST', 'GET'])
def result():
    movie_choice = request.args['movie_choice']
    return render_template('result.html', movie_choice=movie_choice)


@how_it_works_blueprint.route('/how_it_works', methods=['POST', 'GET'])
def how_it_works():
    return render_template('how_it_works.html')