# Import  database object (db) from main application module
from app import db

# Import library to convert item name and category name in url-safe and
# readable/indexable slugs
from slugify import slugify

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

    def __init__(self, name):
        """
        New instance instantiation procedure
        """
        self.name = name

    def __repr__(self):
        """
        Return represantation <Category ...>
        """
        return '<Category %r>' % (self.name)

    @staticmethod
    def exists(category_id):
        """
        Check if a dategory defined by category_id exists in db
        """
        if Category.query.filter_by(id=category_id):
            return True
        else:
            return False

    @staticmethod
    def get_items_in_category(category_id):
        """
        Get all items from a given category
        """
        return Item.query.filter_by(category_id=category_id)\
                         .join(Category)\
                         .add_columns(Category.name,
                                      Item.title,
                                      Item.date_created,
                                      Item.id).order_by(
                                          Item.date_created.desc())

    @staticmethod
    def get_categories():
        """
        Query and return all categories from db and add slugified names
        """
        categories = Category.query.order_by(Category.name)

        new_list = []

        class NewCategory(object):
            pass

        # now loop through the categories and add slugified name
        for category in categories:
            new_category = NewCategory()
            new_category.slugified_name = slugify(category.name)
            new_category.name = category.name
            new_category.id = category.id
            new_list.append(new_category)

        return new_list


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
