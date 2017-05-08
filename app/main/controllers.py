from flask import Blueprint, render_template, flash, redirect, url_for

from flask_wtf import FlaskForm

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return redirect(url_for('catalog.catalog'))
