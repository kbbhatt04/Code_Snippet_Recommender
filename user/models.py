from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
from app import user_collection, code_collection
import uuid


class User:

    def start_session(self, user):
        del user['password']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def signup(self):
        print(request.form)

        # Create the user object
        user = {
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "password": request.form.get('password')
        }
        print(user)
        # Encrypt the password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        # Check for existing email address
        if user_collection.find_one({"email": user['email']}):
            return jsonify({"error": "Email address already in use"}), 400

        if user_collection.insert_one(user):
            return self.start_session(user)

        return jsonify({"error": "Signup failed"}), 400

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):

        user = user_collection.find_one({
            "email": request.form.get('email')
        })

        if user and pbkdf2_sha256.verify(request.form.get('password'), user['password']):
            return self.start_session(user)

        return jsonify({"error": "Invalid login credentials"}), 401


class Code:
    def submit_code_snippet(self):
        print(request.form)
        
        code = {
            "_id": uuid.uuid4().hex,
            "user_email": session["user"]["email"],
            "language": request.form.get('language'),
            "keywords": request.form.get('keywords').lower(),
            "description": request.form.get('description'),
            "snippet": request.form.get('snippet'),
            "votes": 0
        }
        print(code)
        
        if code_collection.insert_one(code):
            return jsonify(code), 200
        
        return jsonify({"error": "Error Submitting Code Snippet"}), 200
        

class Search:
    def logic(self, text):
        keywords = set(text.split())
        
        languages = []
        for i in keywords:
            if(i[0] == "#"):
                languages.append(i[1:].lower())
        
        print(languages)
        
        match_list = []
        cursortemp = list(code_collection.find())
        
        cursor = []
        
        if(len(languages) > 0):
            for i in cursortemp:
                if(i['language'].lower() in languages):
                    cursor.append(i)
        else:
            cursor = cursortemp
        
        for count, record in enumerate(cursor):
            match_list.append([0, count])
        
        if(len(languages) == len(keywords)):
            for count, record in enumerate(cursor):
                match_list[count][0] += 1
        else:
            for key in keywords:
                for count, record in enumerate(cursor):
                    if(key in record['keywords']):
                        match_list[count][0] += 1
        
        match_list.sort(reverse=True)
        
        final_list = []
        for i in match_list:
            if(i[0] == 0):
                break
            else:
                final_list.append(cursor[i[1]])
        
        print("*" * 50)
        print("Match List:")
        print(match_list)
        print("*" * 50)
        print("Final List:")
        print(final_list.sort(key=lambda x: x['votes'], reverse=True))
        print("*" * 50)
        
        return final_list
    
    def search_code(self):
        keywords = {
            "keys": request.form.get('keywords')
        }
        if(keywords["keys"] == None):
            keywords["keys"] = ""
        #print(keywords)
        session['keyword'] = keywords["keys"]
        mylist = self.logic(session['keyword'])
        # cursor = code_collection.find()
        # self.logic(session['keyword'])
        # for record in cursor:
        #     if(session['keyword'] in record['keywords']):
        #         mylist.append(record)
    
        #print(mylist)
        
        return mylist
    
    def search_by_keyword(self):
        mylist = self.logic(session['keyword'])
        # cursor = code_collection.find()
    
        # for record in cursor:
        #     if(session['keyword'] in record['keywords']):
        #         mylist.append(record)
    
        #print(mylist)
        
        return mylist