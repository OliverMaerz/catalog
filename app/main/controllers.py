from flask import Blueprint, render_template, flash

from flask_wtf import FlaskForm



main = Blueprint('main', __name__)


@main.route('/')
def index():

  return render_template("main/index.html")