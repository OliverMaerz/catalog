# Import Form
from flask_wtf import FlaskForm

# Import Form elements
from wtforms import PasswordField, StringField, SubmitField,\
                    ValidationError, BooleanField

# Import Form validators
from wtforms.validators import InputRequired, DataRequired,\
                               Email, EqualTo

# Import QuerySelectField for drop downs
from wtforms.ext.sqlalchemy.fields import QuerySelectField

# Import Item and Category
from .models import Item, Category


class AddCategoryForm(FlaskForm):
    """
    Form to add a category to catalog
    """
    name = StringField('Category Name')
    submit = SubmitField('Save Category')
    cancel = SubmitField('Cancel')

    def validate_name(self, field):
        if (Category.query.filter_by(name=field.data).first() and not
           (self.cancel.data)):
            raise ValidationError('Category name is already in use.')
        if not (field.data) and not (self.cancel.data):
            raise ValidationError('Please fill out the field.')


class DeleteCategoryForm(FlaskForm):
    """
    Form to confirm deletion of a category (just a button)
    """
    back = SubmitField('No, go back.')
    delete = SubmitField('Yes, delete forever!')


class AddItemForm(FlaskForm):
    """
    Form to add or edit an item
    """
    def enabled_categories():
        return Category.query.order_by(Category.name)

    title = StringField('Item Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    category = QuerySelectField('Category',
                                query_factory=enabled_categories,
                                get_label='name',
                                allow_blank=False)
    submit = SubmitField('Save Item')
