# Import flask libs
from flask import Blueprint, render_template, redirect, flash, url_for, \
                  session, abort, jsonify

# Import the database object from the main app module
from app import db

# Import library to convert item name and category name in url-safe and
# readable/indexable slugs
from slugify import slugify

# Import module models (i.e. Categories, Items ...)
from .models import Category, Item

# Import module forms
from .forms import AddCategoryForm, DeleteCategoryForm, AddItemForm

# Define blueprint
mod_catalog = Blueprint('catalog', __name__, url_prefix='/catalog')


# helper functions

def add_slugify(items):
    """
    Add slugified item names and category names to list of items
    """
    new_list = []

    class NewItem(object):
        pass

    # Loop through items and add to new list then return it
    for item in items:
        new_item = NewItem()
        new_item.slugified_title = slugify(item.title)
        new_item.slugified_category = slugify(item.name)
        new_item.name = item.name
        new_item.id = item.id
        new_item.title = item.title
        new_list.append(new_item)

    return new_list


# returns the user_id or shows 403 if not logged in
def check_user():
    if 'user_id' in session:
        return int(session['user_id'])
    else:
        abort(403)


@mod_catalog.route('/index/')
@mod_catalog.route('/')
def catalog():
    """
    Handle requests to the /category/ and /catalog/index/ route
    List latest items and all categories
    """
    categories = Category.get_categories()
    latest_items = Item.query.join(Category)\
                             .add_columns(Category.name, Item.title,
                                          Item.date_created, Item.id)\
                             .order_by(Item.date_created.desc())\
                             .limit(10)

    slugified_items = add_slugify(latest_items)

    return render_template('catalog/catalog.html', items=slugified_items,
                           categories=categories, title='Latest Items',
                           item_title='Items')


@mod_catalog.route('/category/index/')
@mod_catalog.route('/category/')
def categories_list():
    """
    Handle requests to /catalog/category/ and /catalog/category/index/
    List all categories
    """
    categories = Category.get_categories()
    return render_template('catalog/category/list.html',
                           categories=categories,
                           title='Categories')


@mod_catalog.route('/category/add/',
                   methods=['GET', 'POST'])
def category_add():
    """
    Handle requests to the /catalog/category/add/ route
    Add an category to the database
    """
    # check if user is logged in and get user id
    loggedin_user = check_user()

    form = AddCategoryForm()
    if form.validate_on_submit():
        if (form.submit.data):
            category = Category(name=form.name.data)
            # add category to db
            db.session.add(category)
            db.session.commit()
            flash('You have successfully added the category "' +
                  form.name.data + '".')
            form.name.data = ''

        # redirect to the categories page
        return redirect(url_for('catalog.categories_list'))

    return render_template('catalog/category/add.html',
                           form=form,
                           title='Add Category')


@mod_catalog.route('/category/edit/<category_id>',
                   methods=['GET', 'POST'])
def category_edit(category_id):
    """
    Handle requests to the /catalog/category/add/ route
    Add an category to the database
    """
    # check if user is logged in and get user id
    loggedin_user = check_user()

    category = Category.query.filter_by(id=category_id).first_or_404()
    form = AddCategoryForm(obj=category)
    if form.validate_on_submit():
        if (form.submit.data):
            # update category name in
            form.populate_obj(category)
            db.session.commit()
            flash('You have successfully updated the category "' +
                  form.name.data + '".')

        # redirect to the categories page
        return redirect(url_for('catalog.categories_list'))

    return render_template('catalog/category/add.html',
                            form=form,
                            title='Edit Category')


@mod_catalog.route('/category/delete/<category_id>',
                   methods=['GET', 'POST'])
def category_delete(category_id):
    """
    Handle requests to the /catalog/category/delete/<page_id> route
    Delete a category from the db
    """
    # check if user is logged in and get user id
    loggedin_user = check_user()

    # get the category to show name and also check if it really exists
    category = Category.query.filter_by(id=int(category_id)).first_or_404()
    form = DeleteCategoryForm()

    # Do not allow to delete category if it has items!
    if (Item.query.filter_by(category_id=category_id).count() > 0):
        flash('Category "' + category.name +
              '" is not empty! Please delete all items in category first.')
        return redirect(url_for('catalog.categories_list'))

    if form.validate_on_submit():
        if (form.delete.data):
            db.session.delete(category)
            db.session.commit()

            flash('You have successfully deleted the category "' +
                  category.name + '".')
        else:
            flash('Category not deleted.')

        # redirect to categories page
        return redirect(url_for('catalog.categories_list'))

    return render_template('catalog/delete.html',
                           form=form,
                           title='Delete Category "' + category.name +
                                 '" ???')


@mod_catalog.route('/i/<category_slug>/<item_slug>/<item_id>/')
def item_show(category_slug, item_slug, item_id):
    """
    Handle requests to the /catalog/i/i/<category>/<item>/<item_id> route
    Show an item from the catalog
    """
    item = Item.query.filter_by(id=int(item_id)).first_or_404()

    return render_template('catalog/item/index.html',
                           title=item.title,
                           item=item)


@mod_catalog.route('/c/<category_slug>/<category_id>/')
def items_list(category_slug, category_id):
    """
    Handle requests to the /category/list/<category>/<category_id> route
    Show item from the catalog based on selected category
    """
    categories = Category.get_categories()

    # find the category name for the selected category id
    for category in categories:
        if int(category.id) == int(category_id):
            break
    else:
        # category not found (manipulated url?) redirect to main catalog page
        return redirect(url_for('catalog.catalog'))
    selected_category = category

    # get all items in Category
    items = Category.get_items_in_category(category_id)
    slugified_items = add_slugify(items)

    # check number of items
    num_items = len(slugified_items)

    item_title = str(num_items)+' Item'
    if num_items != 1:
        item_title = item_title + 's'

    return render_template('catalog/catalog.html',
                           categories=categories,
                           items=slugified_items,
                           title='Category '+selected_category.name,
                           hide_category=1,
                           item_title=item_title)


@mod_catalog.route('/item/edit/<item_id>/', methods=['GET', 'POST'])
def item_edit(item_id):
    """
    Handle requests to the /item/edit/<item_id> route
    Edit an item
    """
    # check if user is logged in and get user id
    loggedin_user = check_user()

    item = Item.query.filter_by(id=item_id).first_or_404()

    # Check if item was not created by user
    if item.user_id != loggedin_user:
        flash('Item "' + item.title +
              '" was created by another user. \
              You can only edit items that you have created.')
        return redirect(url_for('catalog.catalog'))

    form = AddItemForm(obj=item)
    if form.validate_on_submit():
        if (form.submit.data):
            # Now check if category really exists!
            if (Category.exists(int(form.category.data.id))):
                # update item data
                form.populate_obj(item)
                item.category_id = int(form.category.data.id)
                db.session.commit()
                flash('You have successfully updated the item "' +
                      form.title.data + '".')
                # redirect to the main catalog page

                return redirect(url_for('catalog.catalog'))
            else:
                # fake category - return error message
                flash('Please select a valid category.')

    # pre-select the category from the item.category_id field in the dropdown
    form.category.process_data(Category.query.filter_by(id=item.category_id)
                               .first_or_404())

    return render_template('catalog/item/add.html',
                           form=form,
                           title='Edit Item')


@mod_catalog.route('/item/add/', methods=['GET', 'POST'])
def item_add():
    """
    Handle requests to the /edit/item/<item_id> route
    Add an item to the database
    """
    # Make sure user is logged in and get user id
    loggedin_user = check_user()

    form = AddItemForm()
    if form.validate_on_submit():
        if (form.submit.data):
            # Now check if category really exists!
            if (Category.exists(int(form.category.data.id))):
                # set item data
                item = Item(title=form.title.data,
                            description=form.description.data,
                            category_id=int(form.category.data.id),
                            user_id=loggedin_user)
                # now store it in db
                db.session.add(item)
                db.session.commit()
                flash('You have successfully added the item "' +
                      form.title.data + '".')

                # redirect to the catalog page
                return redirect(url_for('catalog.catalog'))
            else:
                # fake category - return error message
                flash('Please select a valid category.')

    return render_template('catalog/item/add.html',
                           form=form,
                           title='Add Item')


@mod_catalog.route('/item/delete/<item_id>/',
                   methods=['GET', 'POST'])
def item_delete(item_id):
    """
    Handle requests to the /item/delete/<item_id>/ route
    Deletes an item
    """
    # check if user is logged in and get user id
    loggedin_user = check_user()

    item = Item.query.filter_by(id=item_id).first_or_404()

    # Checck if item was not created by user
    if item.user_id != loggedin_user:
        flash('Item "' + item.title +
              '"" was created by another user. You can only delete items\
              that you have created.')
        return redirect(url_for('catalog.catalog'))

    form = DeleteCategoryForm()

    if form.validate_on_submit():
        if (form.delete.data):
            # Category.query.filter_by(id=category_id).delete()
            db.session.delete(item)
            db.session.commit()

            flash('You have successfully deleted the item "' +
                  item.title + '".')
        else:
            flash('Item not deleted.')

        # redirect to categories page
        return redirect(url_for('catalog.catalog'))

    return render_template('catalog/delete.html',
                           form=form,
                           title='Delete Item "' + item.title + '" ???')


@mod_catalog.route('/json/')
def json_catalog():
    """
    Handle requests to the /catalog/json/ route
    List complete catalog in json format
    """

    whole_catalog = []
    # loop through categories and add then via new_category to whole_catalog
    for category in Category.query.all():
        item_list = []
        # loop though items and add them as 'Item' to corresponding category
        for item in Item.query.filter_by(category_id=category.id).all():
            new_item = {
                'category_id': category.id,
                'description': item.description,
                'id': item.id,
                'title': item.title
            }
            item_list.append(new_item)

        new_category = {
            'Item': item_list,
            'id': category.id,
            'name': category.name
        }
        whole_catalog.append(new_category)

    # Return the serialized structure as JSON
    return jsonify(Category=whole_catalog)
