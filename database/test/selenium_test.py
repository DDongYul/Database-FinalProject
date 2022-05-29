import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip

#각 영화의 페이지 들어가는 것 까지

URL = 'https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver'
email = 'junsub_lee@naver.com'
pwd = 'uisbahuiah3876@!'

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
    
def main():
    #webdriver 설치한 절대경로에 따라 변경해주기, 자동입력 우회pyperclip사용
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database/test/chromedriver.exe')
    driver.get(url=URL)
    #로그인하기
    driver.find_element_by_css_selector('#gnb_login_button').click()
    driver.find_element_by_css_selector('#id').click()
    pyperclip.copy(email)
    driver.find_element_by_css_selector('#id').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    
    driver.find_element_by_css_selector('#pw').click()
    pyperclip.copy(pwd)
    driver.find_element_by_css_selector('#pw').send_keys(Keys.CONTROL, 'v')
    time.sleep(1)
    driver.find_element_by_css_selector('#log\.login').click()
    
    box = driver.find_elements_by_css_selector('#old_content > table > tbody > tr > td > a')
    i = 0
    for e in box:
        #해당 년도 링크 타고 들어가고(새탭에서) 그 새탭으로 들어가기     
        e.send_keys(Keys.CONTROL + '\n')
        driver.switch_to.window(driver.window_handles[1])

        while 1:
            lst = driver.find_elements_by_css_selector('#old_content > ul > li > a')
            time.sleep(1)
            for element in lst:
                element.send_keys(Keys.CONTROL + '\n')
                driver.switch_to.window(driver.window_handles[2])
                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
            if driver.find_elements_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a'):
                driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
            else:
                break

        #탭 닫고 다시 맨 처음 페이지로 이동
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        time.sleep(1)
        i = i + 1
        if(i == 10):
            break
        
    
if __name__ == '__main__':
    main()