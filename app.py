from flask import Flask, render_template, session, redirect, request
from functools import wraps
import pymongo

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

client = pymongo.MongoClient(
    'mongodb+srv://root:Root1234@cluster0.tz22tii.mongodb.net/?retryWrites=true&w=majority')
db = client.get_database('user_login_system')
user_collection = db.users
code_collection = db.code

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/signin')

    return wrap


# Routes
from user import routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signin')
def signin():
    return render_template('home.html')

@app.route('/dashboard/')
@login_required
def dashboard():
    cursor = code_collection.find()
    return render_template('dashboard.html', result = cursor)

@app.post('/dashboard/<id>/delete')
def delete_snippet(id):
    code_collection.delete_one({"_id": id})
    return redirect('/dashboard/')

# @app.route('/search_result/', methods=['POST'])
# def search_res():
#     return render_template('search_result.html')