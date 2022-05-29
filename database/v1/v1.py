import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup

email = 'junsublee0617'
pwd = 'jgtmapm3876'
naver_movie_dir_url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver'
#각 테이브에 대한 buf, executemany를 위한 buf, 각 element는 table 형식에 맞는 tuple이다.
movie_list_buf = []
scope_table_buf = []
actor_table_buf = []

#하나의 영화에 대한 웹페이지의 도메인 네임에서 id추출하는 함수, code=뒤의 숫자
def url_to_id(cur_url):
    return cur_url.split('code=')[1]
    
#하나의 영화에 대하여 데이터 크롤링하는 함수 
def crawling_one_movie(id, driver):
    #전역변수 초기화
    global movie_list_buf
    global scope_table_buf
    global actor_table_buf
    
    main_html = driver.page_source
    main_soup = BeautifulSoup(main_html, 'html.parser')
    #convert to tuple, append to movie_list_buf
    one_movie_inform = []
    #list of tuples, all elements append to table_buf
    one_movie_scopes = []
    one_movie_actors = []
    
    #id
    one_movie_inform.add(id)
    
    #title
    title = main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
    if(len(title) > 30):
        title = title[0 : 30]
    one_movie_inform.add(id)
    
    #summary
    
    
    
    
    
    
    
    
    
def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
    
def main():
    #전역변수 초기화
    global movie_list_buf
    global scope_table_buf
    global actor_table_buf
    
    #conn, cur 초기화, db열기
    conn, cur = open_db()
    
    #년도별 영화 디렉토리 접속, webdriver의 경로에 대해서는 개인에 맞춰 수정
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database/chromedriver.exe')
    driver.get(url=naver_movie_dir_url)
    
    #로그인 하기
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
    
    #첫 웹페이지에서 년도별 디렉토리 웹페이지(년도별 영화 리스트 페이지)들 반복적으로 접속
    year_dir_link_lst = driver.find_elements_by_css_selector('#old_content > table > tbody > tr > td > a')
    for year_dir_link in year_dir_link_lst:
        #새탭에서 해당 년도 디렉토리 웹페이지(영화 리스트 페이지)를 열고 새롭게 연 탭으로 이동
        year_dir_link.send_keys(Keys.CONTROL + '\n')
        driver.switch_to.window(driver.window_handles[1])
        
        #한개의 영화 리스트 페이지에 대하여 영화 링크들을 리스트화한다. 이후 반복적으로 한 페이지 내의 영화들에 대한 정보를 모두 뽑아낸 후 반복적으로 다음 페이지로 넘어감. 다음 페이지가 없을시 종료
        while 1:
            movie_link_list = driver.find_elements_by_css_selector('#old_content > ul > li > a')
            for movie_link in movie_link_list:
                #한개의 영화 ....
                
                movie_link.send_keys(Keys.CONTROL + '\n')
                driver.switch_to.window(driver.window_handles[2])
                
                #id추출, 하나의 영화에 대한 메인 웹페이지의 도메인 네임의 code= 뒤의 숫자                
                #하나의 영화에 대하여 crawling 하고 buf에 넣기....
                #crawling_one_movie(url_to_id(driver.current_url), driver)
                
                # if(len(movie_list_buf > 50)):
                    #executemany sql...
                    
                
                
                #현재 탭(하나의 영화에 대한 웹페이지) 닫고 이전 탭(영화 리스트 페이지)로 돌아간다.
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
                
                
    #db닫기            
    close_db(conn,cur)
    #chromedriver닫기
    driver.quit()
    
if __name__ == '__main__':
    main()