# Homework 01
Crawl PTT Beauty板  
  
四種功能：
* `crawl`  
* `push`   
* `popular`   
* `keyword`     
1. Python 0516041.py crawl  
-> 爬2017年一整年文章  
-> Input: N/A  
-> Output: 1. all_articles.txt (所有文章)  
           2. all_popular.txt (所有爆文)  
           
2. Python 0516041.py push start_date end_date  
-> 數推文噓文和找出前10名最會推跟噓的人
-> Input: start_date end_date  
   E.g. Python 0516041.py push 101 1231  
-> Output: push[start_date-end_date].txt  
   E.g. push[101-1231].txt
   
3. Python 0516041.py popular start_date end_date  
-> 找爆文和圖片URL   
-> Input: start_date end_date  
   E.g. Python 0516041.py popular 101 201  
-> Output: popular[start_date-end_date].txt  
   E.g. popular[101-201].txt  
   
4. Python 0516041.py keyword {keyword} start_date end_date   
-> 找內文中含有{keyword}的文章中的所有圖片  
-> Input: {keyword}(欲尋找的關鍵字) start_date end_date  
   E.g. Python 0516041.py keyword 正妹 101 201  
-> Output: keyword({keyword})[start_date-end_date].txt  
   E.g. keyword(正妹)[101-201].txt  
   
使用的模組：  
beautifulsoup4==4.6.3  
certifi==2018.8.24  
chardet==3.0.4  
idna==2.7  
lxml==4.2.5  
pkg-resources==0.0.0  
requests==2.19.1  
urllib3==1.23
