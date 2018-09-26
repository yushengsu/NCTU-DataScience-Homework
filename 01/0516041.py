from bs4 import BeautifulSoup
import requests
import urllib3
import time
import sys
import operator

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
res = requests.get("https://www.ptt.cc/bbs/Beauty/index.html", verify = False)
soup = BeautifulSoup(res.text,features="lxml")

def main():
    if sys.argv[1] == "crawl":
        start_time = time.time()
        crawl()
        print("--- %s seconds ---" % (time.time() - start_time))
    elif sys.argv[1] == "push":
        start_time = time.time()
        push(sys.argv[2], sys.argv[3])
        print("--- %s seconds ---" % (time.time() - start_time))
    elif sys.argv[1] == "popular":
        start_time = time.time()
        popular(sys.argv[2], sys.argv[3])
        print("--- %s seconds ---" % (time.time() - start_time))
    elif sys.argv[1] == "keyword":
        start_time = time.time()
        keyword(sys.argv[2], sys.argv[3], sys.argv[4])
        print("--- %s seconds ---" % (time.time() - start_time))
    
        
def crawl():
    file1 = open("all_articles.txt", mode = "w", encoding = "utf-8")
    file2 = open("all_popular.txt", mode = "w", encoding = "utf-8")

    href_check = """https://www.ptt.cc/bbs/Beauty/M.1490936972.A.60D.html
                    https://www.ptt.cc/bbs/Beauty/M.1494776135.A.50A.html
                    https://www.ptt.cc/bbs/Beauty/M.1503194519.A.F4C.html
                    https://www.ptt.cc/bbs/Beauty/M.1504936945.A.313.html
                    https://www.ptt.cc/bbs/Beauty/M.1505973115.A.732.html
                    https://www.ptt.cc/bbs/Beauty/M.1507620395.A.27E.html
                    https://www.ptt.cc/bbs/Beauty/M.1510829546.A.D83.html
                    https://www.ptt.cc/bbs/Beauty/M.1512141143.A.D31.html
                 """

    for page in range(1992, 2341): # 1992 : 2017第一篇 2340 : 2017最後一篇
            
        url = "https://www.ptt.cc/bbs/Beauty/index" + str(page) + ".html"
        res = requests.get(url, verify = False)
        soup = BeautifulSoup(res.text,features="lxml")

        for article in soup.select(".r-ent"):

            if len(article.select(".title")[0].find_all('a')):

                href = article.select(".title")[0].find_all('a')[0]["href"]
                href = "https://www.ptt.cc/bbs/Beauty/" + href[12:]               
                title = article.select(".title")[0].text
                date = article.select(".date")[0].text
                push = article.select(".nrec")[0].text
                
                if not push:
                    push = "0"
                if push == "爆":
                    push = "101"
                if push[0] == "X":
                    push = "-10"
                push = int(push)
                            
                date = date.replace('/','')
                date = date.replace(' ','')
                title = title.strip('\n')
                total = date + ',' + title + ',' + href + '\n'

                if not (date == "1231" and page == 1992) and not (date == "101" and page == 2340) and href not in href_check:
                    if "公告" not in title[0:4]:
                        file1.write(total)
                        # print(total)
                        if push >= 100:
                            file2.write(total)
        time.sleep(0.5)
    file1.close()
    file2.close()


def push(start_date, end_date):

    file_name = "push[" + start_date + "-" + end_date + "].txt"
    file3 = open("all_articles.txt", mode = "r", encoding = "utf-8")
    file4 = open(file_name, mode = "w", encoding = "utf-8")
    
    like = 0
    boo = 0
    like_id_list = {}
    boo_id_list = {}
    
    for line in file3:
        url = line[line.find('http'):]
        href = url.replace('\n','')
        date = line[0:line.find(',')]
        title = line[line.find(',')+1: line.find(',http')]
        if int(date) >= int(start_date) and int(date) <= int(end_date):
                        
        
            article_res = requests.get(href, verify = False)
            art_soup = BeautifulSoup(article_res.text,features="lxml")
            
            for comments in art_soup.select(".push"):
                try:
                    comments_push = comments.find_all('span')[0].text
                    comments_push = comments_push.replace('\n','')
                    
                    comments_id = comments.find_all('span')[1].text
                    
                    if "推" in comments_push:
                        if comments_id not in like_id_list:
                            like_id_list[comments_id] = 1
                        else:
                            like_id_list[comments_id] += 1
                        like += 1
                    elif "噓" in comments_push:
                        if comments_id not in boo_id_list:
                            boo_id_list[comments_id] = 1
                        else:
                            boo_id_list[comments_id] += 1
                        boo += 1 
                except:
                    pass
            print(date + ',' + title + ',' + "like:" + str(like) + ',' + "boo:" + str(boo))
        
        # time.sleep(0.5)
    print("all like:", like)
    print("all boo:", boo)
    file4.write("all like: " + str(like) + '\n')
    file4.write("all boo: " +  str(boo) + '\n')
    
    sort_like_num = sorted(like_id_list.items(), key = operator.itemgetter(1, 0), reverse = True)
    sort_like_name = sorted(sorted(sort_like_num, key = lambda x : x[0]), key = lambda x : x[1], reverse = True)

    for top in range(0,10):
        like_comment = "like #" + str(top+1) + ": "
        print(like_comment, end = '')
        file4.write(like_comment)
        print(sort_like_name[top][0],sort_like_name[top][1])
        file4.write(sort_like_name[top][0] + " " + str(sort_like_name[top][1]) + '\n')

    sort_boo_num = sorted(boo_id_list.items(), key = operator.itemgetter(1, 0), reverse = True)
    sort_boo_name = sorted(sorted(sort_boo_num, key = lambda x : x[0]), key = lambda x : x[1], reverse = True) 

    for top in range(0,10):
        boo_comment = "boo #" + str(top+1) + ": "
        print(boo_comment, end = '')
        file4.write(boo_comment)
        print(sort_boo_name[top][0],sort_boo_name[top][1])
        file4.write(sort_boo_name[top][0] + " " + str(sort_boo_name[top][1]) + '\n')
    file3.close()
    file4.close()
    

def popular(start_date, end_date):

    file_name = "popular[" + start_date + "-" + end_date + "].txt"
    file5 = open("all_popular.txt", mode = "r", encoding = "utf-8")
    file6 = open(file_name, mode = "w", encoding = "utf-8")
    
    article_num = 0
    img_url = list()

    for line in file5:

        date = line[0:line.find(',')]  
        if int(date) >= int(start_date) and int(date) <= int(end_date):
            url = line[line.find('http'):]
            href = url.replace('\n','')
            
            article_num += 1
            article_res = requests.get(href, verify = False)
            art_soup = BeautifulSoup(article_res.text,features="lxml")

            for post in art_soup.select("a"):
                try:
                    if post['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                        img_url.append(post['href'])
                except:
                    pass
        time.sleep(0.5)    
    # print("number of popular articles:", article_num)
    # for url_text in img_url:
    #     print(url_text)

    file6.write("number of popular articles: " + str(article_num) + '\n')
    for url_text in img_url:
        file6.write(url_text + '\n')
    
    file5.close()
    file6.close()


def keyword(key_word, start_date, end_date):
    key_word = key_word.strip('(')
    key_word = key_word.strip(')')
    file_name = "keyword(" + key_word +")[" + start_date + "-" + end_date + "].txt"
    img_url = list()

    file7 = open("all_articles.txt", mode = "r", encoding = "utf-8")
    file8 = open(file_name, mode = "w", encoding = "utf-8")
    
    for line in file7:
        # title = line[line.find(',')+1: line.find(',http')]
        date = line[0:line.find(',')]  
        url = line[line.find('http'):]
        href = url.replace('\n','')

        if int(date) >= int(start_date) and int(date) <= int(end_date):
            # print(title, " ", href, end = ' ')
            article_res = requests.get(href, verify = False)
            art_soup = BeautifulSoup(article_res.text,features="lxml")
            art_context = str( art_soup.find_all('div', {'id': 'main-container'}) ).split('--')[0]

            if key_word in art_context:
                
                # print(title, " ", href)

                for post in art_soup.select("a"):
                    try:
                        if post['href'].endswith(('.jpg','.jpeg','.png','.gif')):
                            img_url.append(post['href'])
                    except:
                        pass
        time.sleep(0.5)
    for url_text in img_url:
        # print(url_text)
        file8.write(url_text + '\n')    

    file7.close()
    file8.close()


if __name__ == "__main__":
    main()
