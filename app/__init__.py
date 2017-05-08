# Import flask and template operators
from flask import Flask, render_template, flash

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Import Flask-Bootstrap for wtf and utils libraries
from flask_bootstrap import Bootstrap

# Import the CSRF library
from flask_wtf.csrf import CSRFProtect

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Import modules / components using their blueprint handler
from app.mod_google_auth.controllers import mod_google_auth \
                                            as google_auth_module
from app.main.controllers import main as main_module
from app.mod_catalog.controllers import mod_catalog as catalog_module

# Initiate Flask-Bootstrap ...
Bootstrap(app)

# Initiate CSRF
csrf = CSRFProtect(app)


# Some error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', title='403 Forbidden'), 404


@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html', title='403 Forbidden'), 403

# Register blueprint(s)
app.register_blueprint(google_auth_module)
app.register_blueprint(main_module)
app.register_blueprint(catalog_module)

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()
