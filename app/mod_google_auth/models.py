# Import the database object (db) from the main application module
from app import db


# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define a Category model
class User(Base):
    __tablename__ = 'user'

    # Category name
    username = db.Column(db.String(128),  nullable=False,  unique=True)

    # New instance instantiation procedure
    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<User %r>' % (self.username)
