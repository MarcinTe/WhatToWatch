from . import db


class Users(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(50))
    register_data = db.Column(db.DateTime, nullable=False)

    def __init__(self, name, email, password, register_data):
        self.name, self.email, self.password, self.register_data = name, email, password, register_data


class Genre(db.Model):
    __tablename__ = "genre"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    moviesGenres = db.relationship('MovieGenre', backref='Genre', lazy=True)

    def __init__(self, name):
        self.name = name


class Movies(db.Model):
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(100))
    year = db.Column(db.Integer)
    oscar_rewarded = db.Column(db.Boolean)
    moviesGenres = db.relationship('MovieGenre', backref='Movies', lazy=True)

    def __init__(self, id, title, year, oscar_rewarded):
        self.id, self.title, self.year, self.oscar_rewarded = id, title, year, oscar_rewarded

    def __str__(self):
        return self.title


class MovieGenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_movie = db.Column(db.String(20), db.ForeignKey(Movies.id))
    id_genre = db.Column(db.Integer, db.ForeignKey(Genre.id))

    def __init__(self, id_movie, id_genre):
        self.id_movie, self.id_genre = id_movie, id_genre





