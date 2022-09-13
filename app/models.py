from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    pieces = db.relationship('Piece', backref='artist', lazy='dynamic')
    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Save the password as the hashed version of the password
        self.set_password(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)
        db.session.commit

#LoginManager takes in id and stores it across requests. This callback is used to reload the user object
@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Piece(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String, unique=True, nullable=False)
    # prev_versions = db.Column()
    title = db.Column(db.String(250), nullable=False)
    comments = db.Column(db.String)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # user = db.relationship('Artist', backref='pieces', lazy='dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    # def update(self, **kwargs):
    #     for key, value in kwargs.items():
    #         if key in {"first_name","last_name", "phone_number", "street_address", "city", "state", "country", "zip_code"}:
    #             setattr(self, key, value)
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()


# class Comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String(1000), nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     piece = db.Column(db.Integer, db.ForeignKey('piece.id'))

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         db.session.add(self)
#         db.session.commit()

#     def update(self, **kwargs):
#         for key, value in kwargs.items():
#             # if self.comment.id == self.user
#             if key in {"body"}:
#                 setattr(self, key, value)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()


