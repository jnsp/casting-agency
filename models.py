from datetime import date

from app import db


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    release_date = db.Column(db.Date, nullable=False)

    def __str__(self):
        return f'<Movie(title={self.title}, release_date={self.release_date}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {'title': self.title, 'release_date': str(self.release_date)}


class Actor(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    def __init__(self, **kwargs):
        super(Actor, self).__init__(**kwargs)
        if self.age < 0:
            raise ValidationError('Age is negative')

    def __str__(self):
        return f'<Actor(name={self.name}, age={self.age}, ' \
                'gender={self.gender}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }


class ValidationError(ValueError):
    pass
