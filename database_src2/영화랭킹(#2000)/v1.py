import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup

exception_page = '1'
exception_movie_id = '191613'
page_is_ok = False
movie_is_ok = False

def crawling_one_movie(id, driver):
    one_movie_inform_tuple = []
    

def login(driver):
    email = 'junsublee0617'
    pwd = 'jgtmapm3876'
    driver.find_element_by_css_selector('#gnb_login_button > span.gnb_txt').click()
    driver.find_element_by_css_selector('#id').click()
    pyperclip.copy(email)
    driver.find_element_by_css_selector('#id').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)   
    driver.find_element_by_css_selector('#pw').click()
    pyperclip.copy(pwd)
    driver.find_element_by_css_selector('#pw').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    driver.find_element_by_css_selector('#log\.login').click() 
       
def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
def url_to_id(cur_url):
    return cur_url.split('code=')[1]

def main():
    global exception_page
    global exception_movie_id
    global page_is_ok
    global movie_is_ok
    
    #6월 5일 기준
    ranking_url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220605&page=1'
    conn, cur = open_db()
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get(url=ranking_url)
    
    #로그인
    login(driver=driver)
    

    while 1:#하나의 랭킹 웹페이지에서 모든 영화 크롤링 하기
        movie_link_list = driver.find_elements_by_css_selector('#old_content > table > tbody > tr > td.title > div > a')
        for movie_link in movie_link_list:#하나의 영화 웹페이지 들어가서 그 영화에 대해서 크롤링하기
            #영화 웹페이지 새탭에 띄우고 탭 바꾸기
            movie_link.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[1])
            
            #crawling......
            crawling_one_movie(url_to_id(driver.current_url), driver)
            
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        
        #다음 페이지가 있으면 넘어가기
        if driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a'):
            driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
        else:
            break
    
    
        
    driver.quit()
    close_db(conn,cur)


if __name__ == '__main__':
    main()