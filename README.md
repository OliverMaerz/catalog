# catalog

To setup the database with support for db migrations run in shell

export FLASK_APP=run.py 
env/bin/flask db init
env/bin/flask db migrate
env/bin/flask db upgrade
