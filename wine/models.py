from flask_login import UserMixin
from wine import db, login_manager


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
    country = db.Column(db.String(20), unique=True, nullable=False)
    winery = db.Column(db.String(40), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    province = db.Column(db.String(50), nullable=True)
    variety = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    user_favored = db.relationship('FavoriteWine', backref='favored_wine', lazy=True)
    user_comment = db.relationship('WineComment', backref='commented_on', lazy=True)


class FavoriteWine(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine._id'), nullable=False)


class WineComment(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user._id'), nullable=False)
    wine_id = db.Column(db.Integer, db.ForeignKey('wine._id'), nullable=False)