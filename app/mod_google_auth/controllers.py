# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Import the database object from the main app module
from app import db

# Import the CSRF library
from flask_wtf.csrf import CSRFProtect

# Imports for the Google Connect ...
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# Import libraries for the json http requests
from flask import make_response
import httplib2
import json
import requests

# Import model
from .models import User

# Get Google Cliend ID secret from json file
CLIENT_ID = json.loads(
    open('app/config/client_secrets.json', 'r').read())['web']['client_id']

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_google_auth = Blueprint('google_auth', __name__,
                            url_prefix='/google_auth')


# Logout and redirect to home page
@mod_google_auth.route('/logout/')
def logout():
    session.clear()
    flash('You have successfully logged out.')
    return redirect('/')


# Show login page with Google connect button
@mod_google_auth.route('/login/')
def login():
    # Google Auth ID
    googleauth_id = '<YOUR GOOGLE OAUTH CLIENT ID HERE>'

    return render_template("google_auth/login.html",
                           googleauth_id=googleauth_id,
                           title='Login')


# google connect url (called by javscript on login page)
@mod_google_auth.route('/gconnect', methods=['GET', 'POST'])
def gconnect():
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('app/config/client_secrets.json',
                                             scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = session.get('credentials')
    stored_gplus_id = session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is ' + \
                                            'already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    session['access_token'] = credentials.access_token
    session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    # store user data from google in session
    session['username'] = data['name']
    session['email'] = data['email']

    # Check user.id in db - or create new user if not exists
    login_user = User.query.filter_by(username=data['email']).first()

    if login_user is None:
        # user does not exist - create in db
        new_user = User(data['email'])
        db.session.add(new_user)
        db.session.commit()
        session['user_id'] = str(new_user.id)
    else:
        session['user_id'] = str(login_user.id)

    flash("You are now logged in as %s" % session['email'])

    return 'Ready.'
