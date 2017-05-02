# Import the database object (db) from the main application module
# We will define this inside /app/__init__.py in the next sections.
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

  __abstract__  = True

  id            = db.Column(db.Integer, primary_key=True)
  date_created  = db.Column(db.DateTime, default=db.func.current_timestamp())
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                                         onupdate=db.func.current_timestamp())

# Define a Category model
class Category(Base):

  __tablename__ = 'category'

  # Category name
  name           = db.Column(db.String(128),  nullable=False,  unique=True)
  # Boolean field if category has been deativated
  deactivated    = db.Column(db.Boolean, nullable=True)

  # New instance instantiation procedure
  def __init__(self, name, deactivated):

    self.name        = name
    self.deactivated = deactivated

  def __repr__(self):
    return '<Category %r>' % (self.name)


# Define a Item model for catalog
class Item(Base):

  __tablename__ = 'item'

  # Item title
  title       = db.Column(db.String(128),   nullable=False)
  # Description field
  description = db.Column(db.String(1024), nullable=True)
  # Foreign key pointing to category
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))


  # New instance instantiation procedure
  def __init__(self, name, deactivated):

    self.name        = name
    self.deactivated = deactivated

  def __repr__(self):
    return '<Item %r>' % (self.title)