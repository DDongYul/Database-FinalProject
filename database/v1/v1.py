import pymysql
from selenium import webdriver


URL = 'https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver'

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
def main():
    browser = webdriver.Chrome(executable_path='C:\Users\junsub\공부\2022 1학기\데이터베이스\과제#4\src\database\v1')
    browser.get(url=URL)
    box = browser.find_elements_by_class_name('directory_item_other > tr > td > a')
    for e in box:
        print(e.text)
    
    
if __name__ == '__main__':
    main()