from flask import Flask,request,redirect
from flask import render_template,Response
import time
import re
import sys
import os
import json
from flask_sqlalchemy import SQLAlchemy
import threading
import datetime
import os
from flask_migrate import Migrate
from flask_cors import cross_origin,CORS
import string
import random
#------------------------------------------------------------------------------------------------------
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class shortURL(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	URL = db.Column(db.String(255))
	MappingURL = db.Column(db.String(255))
  
	def __init__(self,URL,MappingURL):
		self.URL = URL
		self.MappingURL = MappingURL


@app.route("/")
def index():
	return render_template('index.html')

#取得用戶輸入的網址
@app.route("/UserShortUrl")
def UserShortUrl():
	_url = request.args.get('url')
	regex = "(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	check_Url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', _url)
	if len(check_Url) == 0:
		return "URL錯誤，請輸入正確的網址"
	findExistURL = shortURL.query.filter_by(MappingURL=_url).first()
	if findExistURL == None:
		#26^5=11881376個短網址可以配給，以這個Project來說是夠用了
		#剩下就是DB的query latency問題，到時候可以用cluster解決
		randomString = [random.choice(string.ascii_uppercase) for i in range(5)]
		compileURL = ''.join(randomString)
		shortURL_DB = shortURL(URL = compileURL,MappingURL = _url)
		db.session.add(shortURL_DB)
		db.session.commit()
		pass
	else:
		return findExistURL.URL
	return compileURL

@app.route("/<url_key>")
def redirect_to_url(url_key):
    """
    Check the url_key is in DB, redirect to original url.
    """
    url = shortURL.query.filter_by(URL=url_key).first()
    if url is None:
        return False
    return redirect(url.MappingURL)

if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80)
