import pymongo
from flask import Flask, render_template, request, redirect, url_for
from certifi import where
from uuid import uuid4
from flask import json


client = pymongo.MongoClient("mongodb://esha:esha123@ac-z2tehsh-shard-00-00.syivvqb.mongodb.net:27017,ac-z2tehsh-shard-00-01.syivvqb.mongodb.net:27017,ac-z2tehsh-shard-00-02.syivvqb.mongodb.net:27017/?ssl=true&replicaSet=atlas-iahcah-shard-0&authSource=admin&retryWrites=true&w=majority", tls = True, tlsCAFile= where())
db = client.userlogin

app = Flask(__name__)

@app.route("/register", methods = [ 'POST' , 'GET' ])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        data = request.form
        user = {
            '_id': str(uuid4()).replace('-',''),
            'UserName': data.get('UserName'),
            'FirstName':data.get('FirstName'),
            'LastName':data.get('LastName'),
            'Age':data.get('Age'),
            'Email':data.get('Email'),
            'Password':data.get('Password')
        }
        doc = db['Register'].insert_one(user)
        return render_template('register.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.form
        user = {
            'Email':data.get('Email'),
            'Password':data.get('Password')
        }
        print(user)
        doc = db['Register'].find_one({'Email':data.get('Email')})
        print(doc)
        if doc == None:
            return json.jsonify({
                'error':'Not Found',
            }),404

        else:
            if data.get('Password') == doc['Password']:
                return redirect(url_for('page1', data=doc['_id']))

@app.route('/page1/<data>')
def page1(data):
    user = db['Register'].find_one({'_id':data})
    FirstName = user.get('FirstName')
    return render_template('page1.html', FirstName=FirstName)

if __name__ == "__main__":
    app.run(debug=True, port = 8080)


