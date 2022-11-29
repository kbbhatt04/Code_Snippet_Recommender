from flask import Flask, render_template, request, redirect, session
from app import app, code_collection, login_required
from user.models import User, Code, Search


@app.route('/user/signup', methods=['POST'])
def signup():
    return User().signup()


@app.route('/user/signout')
def signout():
    return User().signout()


@app.route('/user/login', methods=['POST'])
def login():
    return User().login()

@app.route('/dashboard/', methods=['POST'])
def code_submit():
    return Code().submit_code_snippet()

@app.route('/', methods=['POST'])
def search():
    global templist
    templist = Search().search_code()
    return Search().search_code()

@app.route('/search_result/', methods=['GET','POST'])
def search_snippet():
    templist = Search().search_by_keyword()
    return render_template('search_result.html', result = templist, length = len(list(templist)))

@app.route("/search_result/upvote/<id>", methods=["GET","POST"])
@login_required
def upvote(id):
    #snippet = code_collection.find({"id": id})
    if request.args.get("upvote"):
        myquery = { "_id": id }
        newvalues = { "$inc": { "votes": 1 } }

        code_collection.find_one_and_update(myquery, newvalues)
    
    templist = Search().search_by_keyword()
    
    return redirect("/search_result/")
    #return render("view_post.html")
    
@app.route("/search_result/downvote/<id>", methods=["GET","POST"])
@login_required
def downvote(id):
    #snippet = code_collection.find({"id": id})
    if request.args.get("downvote"):
        myquery = { "_id": id }
        newvalues = { "$inc": { "votes": -1 } }

        code_collection.find_one_and_update(myquery, newvalues)
    
    templist = Search().search_by_keyword()
    
    return redirect("/search_result/")
