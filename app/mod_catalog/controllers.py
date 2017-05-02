from flask import Blueprint, render_template, redirect, flash, url_for

# Import the database object from the main app module
from app import db

# Import module models (i.e. Categories, Items ...)
from .models import Category

# Import module forms
from .forms import AddCategoryForm, DeleteCategoryForm


mod_catalog = Blueprint('catalog', __name__ ,url_prefix='/catalog')

@mod_catalog.route('/index/')
@mod_catalog.route('/')
def catalog():
  """
  Handle requests to the /category/ and /catalog/index/ route
  List all items with paginator
  """
  return render_template('catalog/catalog.html', title='Catalog Overview')


@mod_catalog.route('/category/index/')
@mod_catalog.route('/category/')
def categories_list():
  """
  Handle requests to the /catalog/category/ and /catalog/category/index/ route
  List all categories
  """
  categories = Category.query.order_by(Category.name)
  return render_template('catalog/category/list.html', categories=categories, title='Categories')


@mod_catalog.route('/category/add/', methods=['GET', 'POST'])
def category_add():
  """
  Handle requests to the /catalog/category/add/ route
  Add an category to the database
  """
  form = AddCategoryForm()
  if form.validate_on_submit():
    category = Category(name=form.name.data, deactivated=False)
    # add category to db
    db.session.add(category)
    db.session.commit()
    flash('You have successfully added the category "' + form.name.data + '"!')
    form.name.data=''
    # redirect to the categories page
    return redirect(url_for('catalog.categories_list'))

  return render_template('catalog/category/add.html', form=form, title='Add Category')


@mod_catalog.route('/category/edit/<category_id>', methods=['GET', 'POST'])
def category_edit(category_id):
  """
  Handle requests to the /catalog/category/add/ route
  Add an category to the database
  """
  form = AddCategoryForm()
  category = Category.query.filter_by(id=category_id).first_or_404()
  if form.validate_on_submit():
    # update category name in
    category.name = form.name.data
    db.session.commit()
    flash('You have successfully updated the category "' + form.name.data + '"!')
    # redirect to the categories page
    return redirect(url_for('catalog.categories_list'))

  form.name.data = category.name
  return render_template('catalog/category/add.html', form=form, title='Edit Category')


@mod_catalog.route('/category/delete/<category_id>', methods=['GET', 'POST'])
def category_delete(category_id):
  """
  Handle requests to the /catalog/category/delete/<page_id> route
  Delete a category from the db
  """
  # get the category to show name and also check if it really exists
  category = Category.query.filter_by(id=category_id).first_or_404()
  form = DeleteCategoryForm()

  if form.validate_on_submit():
    if (form.delete.data):
      #Category.query.filter_by(id=category_id).delete()
      db.session.delete(category)
      db.session.commit()

      flash('You have successfully deleted the category "' + category.name + '".')
    else:
      flash('Category not deleted.')

    # redirect to categories page
    return redirect(url_for('catalog.categories_list'))

  return render_template('catalog/delete.html', form=form, title='Delete Category "' + category.name + '"')

