from flask_login import UserMixin
from sqlalchemy.orm import validates
from wine.wine import db, login_manager


@login_manager.user_loader
def find_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    wine_added = db.relationship('Wine', backref='added_by', lazy=True)
    wine_favorite = db.relationship('FavoriteWine', backref='favored_by', lazy=True)
    wine_comment = db.relationship('WineComment', backref='commented_by', lazy=True)

    def get_id(self):
        return (self._id)


class Wine(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(40), nullable=False)
    winery = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    province = db.Column(db.String(100), nullable=True)
    variety = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=True)
    user_favored = db.relationship('FavoriteWine', backref='favored_wine', lazy=True)
    user_comment = db.relationship('WineComment', backref='commented_on', lazy=True)

    @validates('user_id')
    def empty_string_to_null(self, key, value):
        if isinstance(value, str) and value:
            return None
        else:
            return value

class FavoriteWine(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine._id'), nullable=False)


class WineComment(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine._id'), nullable=False)
