from flask import Blueprint, render_template

mod_catalog = Blueprint('catalog', __name__ ,url_prefix='/catalog')

@mod_catalog.route('/index')
@mod_catalog.route('/')
def catalog():
    return render_template("catalog/catalog.html")