# Import Form
from flask_wtf import FlaskForm

# Import Form elements
from wtforms import PasswordField, StringField, SubmitField, ValidationError, BooleanField

# Import Form validators
from wtforms.validators import InputRequired, DataRequired, Email, EqualTo


from .models import Item, Category

class AddItemForm(FlaskForm):
  """
  Form to add an item to catalog
  """
  email      = StringField('Email', validators=[DataRequired(), Email()])
  username   = StringField('Username', validators=[DataRequired()])
  first_name = StringField('First Name', validators=[DataRequired()])
  last_name  = StringField('Last Name', validators=[DataRequired()])
  password   = PasswordField('Password', validators=[
                                                     DataRequired(),
                                                     EqualTo('confirm_password')
                                                    ])
  confirm_password = PasswordField('Confirm Password')
  submit = SubmitField('Register')

  def validate_email(self, field):
    if Employee.query.filter_by(email=field.data).first():
      raise ValidationError('Email is already in use.')

  def validate_username(self, field):
    if Employee.query.filter_by(username=field.data).first():
      raise ValidationError('Username is already in use.')


class AddCategoryForm(FlaskForm):
  """
  Form to add a category to catalog
  """
  name   = StringField('Category Name', validators=[InputRequired()])
  submit = SubmitField('Save Category')

  def validate_name(self, field):
    if Category.query.filter_by(name=field.data).first():
      raise ValidationError('Category name is already in use.')


class DeleteCategoryForm(FlaskForm):
  """
  Form to confirm deletion of a category (just a button)
  """
  back   = SubmitField('No, go back.')
  delete = SubmitField('Yes, delete forever!')


