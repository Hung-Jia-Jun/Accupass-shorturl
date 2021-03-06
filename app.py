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
import requests
from bs4 import BeautifulSoup
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
	check_Url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', _url)
	
	#define return json format
	res = {}
	res["message"] = ""
	res["url"] = ""
	res["paragraph"] = "目前尚無可預覽文字"
	res["image"] = ""

	if len(check_Url) == 0:
		res["message"] = "URL錯誤，請輸入正確的網址"
		res["url"] = ""
		res_json = json.dumps(res, ensure_ascii=False)
		return Response(response=res_json,
				status=200,
				mimetype="application/json")
	findExistURL = shortURL.query.filter_by(MappingURL=_url).first()
	if findExistURL == None:
		#26^5=11881376個短網址可以配給，以這個Project來說是夠用了
		#剩下就是DB的query latency問題，到時候可以用cluster或是選用效能較好的DB解決
		randomString = [random.choice(string.ascii_uppercase) for i in range(5)]
		compileURL = ''.join(randomString)
		shortURL_DB = shortURL(URL = compileURL,MappingURL = _url)
		db.session.add(shortURL_DB)
		db.session.commit()
		pass
	else:
		compileURL =  findExistURL.URL
	
	#取得網址預覽
	#預覽方案 : 
	# 1.網頁的第一段文字
	# 2.網頁的前1/3的第一張圖片(連結)
	#   2-1 : 因為網頁前面可能有一些網站icon雜圖
	r = requests.get(_url)
	r.encoding = 'utf-8'
	if r.status_code != 200 :
		#雖然網址預覽失敗，但還是一樣縮網址給他
		res["message"] = "網址預覽失敗"
		res["url"] = compileURL
	else:
		soup = BeautifulSoup(r.text, 'html.parser')
		
		imgTagLi = soup.select('img')
		imgLi = []
		for img in imgTagLi:
			try:
				if img["src"] != "":
					imgLi.append(img["src"])
			except KeyError:
				pass
		pageImgLength = len(imgLi)
		previewImageIndex = int(pageImgLength/3)

		#檢查網頁前1/3的圖片是否有src的資訊，沒有的話就往下一張圖片找下去
		#直到找到為止
		for i in range(pageImgLength - previewImageIndex):
			try:
				url = imgLi[previewImageIndex + i]
				#檢查圖片src有沒有空值，有的話就繼續往下找
				if url!= "":
					check_Url = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', url)
					if len(check_Url) > 0:
						res["image"] = url
					break
				else:
					continue
			except KeyError:
				pass
		
		for item in soup.findAll('h1'):
			text = item.text.replace("\n","").replace("\r","")
			if text != "":
				res["paragraph"] = text
				break
		res["message"] = "OK"
		res["url"] = compileURL

	res_json = json.dumps(res, ensure_ascii=False)
	return Response(response=res_json,
			status=200,
			mimetype="application/json")

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
	app.run(host='0.0.0.0',port=8000)
