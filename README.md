# Accupass-shorturl
實作一個短網址服務
且擁有下列功能
短網址服務:簡易網頁
- 任意網址轉換成固定長度的短網址路徑
- 短網址的路徑 (pathname) 不超過五個字元
- 支援超過一千萬個短網址
- 支援短網址預覽:顯示原本網址但不跳轉
- 單元測試

# logic
短網址預覽:顯示原本網址但不跳轉
1. 圖片
  * 偵測該頁面是否含有 <img> 
  * 有的話就檢查是否有src的資訊
  * if 有 src 資訊
    * 顯示src內容
  * else:
    * 往下尋找下一個
2. 預覽文字
  * 偵測該頁面是否含有標題 <h1>  
  * 有的話就檢查text是否為空
  * if text != ""
    * 顯示h1.text內容
  * else:
    * 往下尋找下一個
 
# load docker image from local file
docker load --input accupass.tar

# Run Docker image
docker run -d -p 80:8000 jason/accupass

the service will be automatic running on http://0.0.0.0/
http://0.0.0.0/ is the short url service
