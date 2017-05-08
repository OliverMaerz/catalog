# Import  database object (db) from main application module
from app import db


# Define base model for other database tables to inherit
class Base(db.Model):

    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,
                              default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


# Define Category model
class Category(Base):

    __tablename__ = 'category'

    # Category name
    name = db.Column(db.String(128),  nullable=False,  unique=True)

    # New instance instantiation procedure
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % (self.name)

    # Check if a dategory defined by category_id exists in db
    @staticmethod
    def exists(category_id):
        if Category.query.filter_by(id=category_id):
            return True
        else:
            return False

    # Get all items from a given category
    @staticmethod
    def get_items_in_category(category_id):
        return Item.query.filter_by(category_id=category_id)\
                         .join(Category)\
                         .add_columns(Category.name,
                                      Item.title,
                                      Item.date_created,
                                      Item.id).order_by(
                                          Item.date_created.desc())


# Define a Item model for catalog
class Item(Base):

    __tablename__ = 'item'

    # Item title
    title = db.Column(db.String(128),   nullable=False)
    # Description field
    description = db.Column(db.String(1024), nullable=True)
    # Foreign key pointing to category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # User id of user who created item
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # New instance instantiation procedure
    def __init__(self, title, description, category_id, user_id):

        self.title = title
        self.description = description
        self.category_id = category_id
        self.user_id = user_id

    def __repr__(self):
        return '<Item %r>' % (self.title)
