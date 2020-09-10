import os
import tempfile

import pytest
from app import app
from flask_sqlalchemy import SQLAlchemy
import json
@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True

    with app.test_client() as client:
        #應該要create一個假的DB來做測試用的，不然每次測試就會產生一筆資料
        #不是一個正常的unitest模式
        #找過網路上關於flask的教學，這一段支援好像不太友善
        #無奈時間不夠，不然就會嘗試修復這個問題
        #Todo: add fake db to unitest 
        #init_db()
        yield client
def test_index_page(client):
    #http get method to check html page.
    rv = client.get('/')
    #檢查HTML是否含有想顯示的內容
    #短網址
    assert "response" in str(rv.data)
    #預覽文字段落
    assert "paragraph" in str(rv.data)
    #預覽圖
    assert "previewImg" in str(rv.data)

#測試錯誤的URL parameter 但網站正確，是否會回報錯誤
def test_UserShortUrl_failURL(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https://google.com/asdfsd'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)
    assert responsejson["url"] != ""
    assert responsejson["message"] == "網址預覽失敗"
    assert responsejson["paragraph"] =="目前尚無可預覽文字"
    assert responsejson["image"] == ""

#測試錯誤的URL 連網址都輸入錯誤
def test_UserShortUrl_failURL_1(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https:asdfdsf.com/asdfsd'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)
    assert responsejson["url"] == ""
    assert responsejson["message"] == "URL錯誤，請輸入正確的網址"
    assert responsejson["paragraph"] =="目前尚無可預覽文字"
    assert responsejson["image"] == ""

#測試真實的URL
def test_UserShortUrl_TrueURL(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https://github.com/'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)

    #假設已知Github版面一定有h1這個tag，因為此服務使用h1 title來做為網址預覽
    assert responsejson["url"] != ""
    assert responsejson["message"] == "OK"
    assert responsejson["paragraph"] != ""
    assert responsejson["image"] != ""
   
#測試真實的URL，但沒有h1這個tag的情況，會導致抓不到預覽內文
#也沒有找到img這個tag的時候圖片應該就不會顯示出來了
def test_UserShortUrl_TrueURL_1(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https://www.google.com'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)

    assert responsejson["url"] != ""
    assert responsejson["message"] == "OK"
    assert responsejson["paragraph"] == "目前尚無可預覽文字"
    assert responsejson["image"] == ""
   
#測試真實的URL，沒有找到img這個tag的時候圖片就不應該顯示
def test_UserShortUrl_TrueURL_2(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https://www.runoob.com/python3/python3-tutorial.html'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)

    assert responsejson["url"] != ""
    assert responsejson["message"] == "OK"
    assert responsejson["paragraph"] != ""
    assert responsejson["image"] == ""
   
#測試真實的URL，沒有找到img這個tag的時候圖片就不應該顯示
def test_redirect(client):
    #http get method to check html page.
    rv = client.get('/UserShortUrl', query_string=dict(url='https://github.com/'))
    rv.encoding = 'utf-8'
    responseData = rv.data.decode('utf8').replace("'", '"')
    responsejson = json.loads(responseData)

    #取得URL，並且去確認是否有收到302 redirect status
    assert responsejson["url"] != ""

    r = client.get(responsejson["url"])
    assert r.status_code == 302

if __name__ == "__main__":
    import os
    os.system("pytest")