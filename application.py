import random
import string
import httplib2
import json
import requests

from flask import Flask, render_template, request, redirect, url_for, g
from flask import flash, jsonify, make_response, session as login_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from movies_db_mapping import Base, Category, Movie, User
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from urllib.request import urlopen
from functools import wraps


app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Movie Catalog Application"


# Conection to DB and opening DB session
engine = create_engine('sqlite:///movies.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# !!! BEGINING LOGIN

def loginAlert():
    flash("You have to be logged in to perform this action.")
    return redirect('/login')

# Anti-Forgery State token


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "Current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state, user=login_session)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    #  Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
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
    response = urlopen(url).read().decode('utf8')
    result = json.loads(response)
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
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check to see if user is already logged in.
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    # Specify which information want to store.
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user is known and if not create it
    appuser = session.query(User).filter_by(
        email=login_session['email']).scalar()
    if appuser is None:
        appuser = User(name=login_session['username'],
                       email=login_session['email'])
        session.add(appuser)
        session.commit()
        print('New user created: [id=%s] %s'
              % (appuser.id, appuser.email))
    else:
        print('User found in user DB: [id=%s] %s'
              % (appuser.id, appuser.email))
    login_session['id'] = appuser.id

    # Creating a respons based on specified stored information
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 80px; height: 80px; border-radius: 20px;\
        -webkit-border-radius: 20px; -moz-border-radius: 20px; "> '  # NOQA
    print("Done!")
    return output


# !!! END LOGIN


# !!! BEGINING DISCONNECT


@app.route('/gdisconnect')
# Revoke a current user's token and reset their login_session
def gdisconnect():
    access_token = login_session['access_token']
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % login_session['access_token'])
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        # rest the user's session
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Successfully disconnected.")
        return redirect(url_for('showCat'))
    else:
        # If the given token was invalid:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# !!! END DISCONECT


# !!! BEGINING LOGIN REQUIRED - DECORATOR

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash('You are not allowed to access there')
            return redirect('/login')
    return decorated_function

# !!! END


# !!! BEGINING CHECK ENTITY OWNERSHIP

def isOwner(entity_id):
    if entity_id == login_session['id']:
        return True
    else:
        return False


# !!! END CHECK


# !!! BEGINING JSON


@app.route('/category/JSON')
# JSON code for application.py
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[c.serialize for c in categories])


@app.route('/category/<int:category_id>/movies/JSON')
def listOfMoviesJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Movie).filter_by(category_id=category.id).all()
    return jsonify(Movie=[i.serialize for i in items])


@app.route('/category/<int:category_id>/<int:movie_id>/JSON')
# JSON end point
def movieJSON(category_id, movie_id):
    movieItem = session.query(Movie).filter_by(id=movie_id).one()
    return jsonify(Movie=movieItem.serialize)

# !!! END JSON


# !!! BEGINING CATEGORY TABLE


@app.route('/')
# show home/main page
def index():
    return render_template('index.html', user=login_session)


@app.route('/category/')
# show all categories
def showCat():

    categories = session.query(Category).all()
    return render_template(
        'categories.html', categories=categories, user=login_session)


@app.route('/category/new', methods=['GET', 'POST'])
@login_required
# add new Category
def newCat():

    if request.method == 'POST':
        catNew = Category(name=request.form['name'],
                          creator_id=login_session['id'])
        session.add(catNew)
        session.commit()
        flash("New Category added to DB!")
        return redirect(url_for('showCat'))
    else:
        return render_template('newCategory.html', user=login_session)


@app.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
# edit Category
def editCat(category_id):

    catEdit = session.query(Category).filter_by(id=category_id).one()
    if isOwner(catEdit.creator_id) is not True:
        flash("You do not have permission to edit %s!" % catEdit.name)
        return redirect(url_for('showCat'))
    if request.method == 'POST':
        if request.form['name']:
            catEdit.name = request.form['name']
            session.add(catEdit)
            session.commit()
        flash("Category has been edited!")
        return redirect(url_for('showCat'))
    else:
        return render_template(
            'editCategory.html', category_id=category_id, category=catEdit,
            user=login_session)


@app.route('/category/<int:category_id>/delete', methods=['GET', 'POST'])
@login_required
# delete Category
def deleteCat(category_id):

    catDelete = session.query(Category).filter_by(id=category_id).one()

    if isOwner(catDelete.creator_id) is not True:
        flash("You do not have permission to delete %s!" % catDelete.name)
        return redirect(url_for('showCat'))

    if request.method == 'POST':
        session.delete(catDelete)
        session.commit()
        flash("Movie has been removed from DB!")
        return redirect(url_for('showCat', category_id=category_id))
    else:
        return render_template(
            'deleteCategory.html', category=catDelete, user=login_session)


# !!! END CATEGORY


# !!! BEGINING MOVIE TABLE


@app.route('/category/<int:category_id>/movies')
# lists movies based on selected category_id
def showMovie(category_id):
    # will show all movies within specified category
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Movie).filter_by(category_id=category.id)
    return render_template(
        'movies.html', category=category, items=items,
        category_id=category_id, user=login_session)


@app.route('/category/<int:category_id>/new', methods=['GET', 'POST'])
@login_required
#  add new Movie
def newMovieItem(category_id):

    if request.method == 'POST':
        newItem = Movie(
            title=request.form['title'],
            published=request.form['published'],
            storyline=request.form['storyline'],
            category_id=category_id,
            creator_id=login_session['id'])
        session.add(newItem)
        session.commit()
        flash("New Movie added to DB!")
        return redirect(url_for('showMovie', category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template(
            'newMovie.html',
            category_id=category_id,
            category=category,
            user=login_session)


@app.route('/category/<int:category_id>/<int:movie_id>/edit',
           methods=['GET', 'POST'])
@login_required
# edit Movie
def editMovie(category_id, movie_id):

    editedItem = session.query(Movie).filter_by(id=movie_id).one()

    if isOwner(editedItem.creator_id) is not True:
        flash("You do not have permission to edit %s!" % editedItem.title)
        return redirect(url_for('showMovie', category_id=category_id))

    if request.method == 'POST':
        if request.form['title']:
            editedItem.title = request.form['title']
        if request.form['published']:
            editedItem.published = request.form['published']
        if request.form['storyline']:
            editedItem.storyline = request.form['storyline']
            session.add(editedItem)
            session.commit()
            flash("Movie has been edited!")
        return redirect(url_for('showMovie', category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template(
            'editmovie.html', category_id=category_id, category=category,
            movie_id=movie_id, item=editedItem, user=login_session)


@app.route('/category/<int:category_id>/<int:movie_id>/delete',
           methods=['GET', 'POST'])
@login_required
# delete Movie
def deleteMovie(category_id, movie_id):

    itemDelete = session.query(Movie).filter_by(id=movie_id).one()

    if isOwner(itemDelete.creator_id) is not True:
        flash("You do not have permission to delete %s!" % itemDelete.title)
        return redirect(url_for('showMovie', category_id=category_id))

    if request.method == 'POST':
        session.delete(itemDelete)
        session.commit()
        flash("Movie has been removed from DB!")
        return redirect(url_for('showMovie', category_id=category_id))
    else:
        category = session.query(Category).filter_by(id=category_id).one()
        return render_template(
            'deleteMovie.html', category=category,
            item=itemDelete, user=login_session)


# !!! END MOVIE


# end of application
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
