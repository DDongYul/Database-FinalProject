
from sqlite3 import Cursor
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_css_select(driver : webdriver.Chrome, css_path : str):
    try:
        driver.find_element_by_css_selector(css_path)
    except NoSuchElementException:
        return False
    return True

def login(driver : webdriver.Chrome):
    email = 'junsublee0617'
    pwd = 'jgtmapm3876'
    driver.find_element_by_css_selector('#gnb_login_button > span.gnb_txt').click()
    driver.find_element_by_css_selector('#id').click()
    pyperclip.copy(email)
    driver.find_element_by_css_selector('#id').send_keys(Keys.CONTROL, 'v')
    time.sleep(0.3)   
    driver.find_element_by_css_selector('#pw').click()
    pyperclip.copy(pwd)
    driver.find_element_by_css_selector('#pw').send_keys(Keys.CONTROL, 'v')
    time.sleep(0.3)
    driver.find_element_by_css_selector('#log\.login').click() 

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn : pymysql.Connection, cur : Cursor):
    cur.close()
    conn.close()

if __name__ == '__main__':
    browser = webdriver.Chrome('C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    browser.get('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&tg=0&date=20220605')
    base_movie_url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code='
    login(browser)
    
    conn, cur = open_db()
    conn2, cur2 = open_db()
    cur.execute('select movie_id from movie;')
    
    record = cur.fetchone()
    while record:
        movie_id = str(record['movie_id'])
        movie_url = '"' + base_movie_url + movie_id + '"'
        exceution = 'window.open(' + movie_url + ')'
        browser.execute_script(exceution)
        browser.switch_to.window(browser.window_handles[-1])
        if check_exists_by_css_select(browser, '#content > div.article > div.section_group.section_group_frst > div > div > div.story_area > p'):
            story = browser.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst > div > div > div.story_area > p').text
            cur2.execute('update movie set story = %s where movie_id = %s',(story, movie_id))
            conn2.commit()
            
        browser.close()
        browser.switch_to.window(browser.window_handles[-1])
        record = cur.fetchone()
    
    
    
    close_db(conn, cur)
    close_db(conn2, cur2)