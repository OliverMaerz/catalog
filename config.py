# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Define the database - we are working with
# SQLite for this example
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# DATABASE_CONNECT_OPTIONS = {}

# Define the database - Postgres
SQLALCHEMY_DATABASE_URI = 'postgresql://vagrant:vagrant@localhost/catalog'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = '4+1n^mi5avp-#xw0#8#-9z@pr@)#zjn#5(*e(8n(-2#ki!656g'

# Secret key for signing cookies
SECRET_KEY = 'g32+@tkf28nt%jocz_4rb(4rjy_@c^*ll@z7lsu@%#-*6mjz)f'