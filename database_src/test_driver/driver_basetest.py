import time
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
from bs4 import BeautifulSoup

URL = 'https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver'
email = 'junsublee0617'
pwd = 'jgtmapm3876'

def selenium_base():
    global URL
    global email
    global pwd
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src/chromedriver.exe')
    driver.get(url=URL)
    
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
                
                #하나의 영화 웹페이지 들어가서 할 code
                actor_tab_exist_test(driver)    
                
                
                #현재 탭(하나의 영화에 대한 웹페이지) 닫고 이전 탭(영화 리스트 페이지)로 돌아간다.
                driver.close()
                driver.switch_to.window(driver.window_handles[1])
            
            if driver.find_elements_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a'):
                driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
            else:
                break  
        #해당 년도에 대한 탭(웹페이지) 닫고 다시 맨 처음 웹페이지로 돌아가기       
        driver.close()
        driver.switch_to.window(driver.window_handles[0])                                                 
    #chromedriver닫기
    driver.quit()
    
def actor_tab_exist_test(driver):
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    if soup.select_one('#movieEndTabMenu > li:nth-child(2) > a > em').text != '배우/제작진':
        print(driver.current_url)
        quit()
    driver.find_element_by_css_selector('#movieEndTabMenu > li:nth-child(2) > a').send_keys(Keys.CONTROL + '\n')
    driver.switch_to.window(driver.window_handles[3])
    time.sleep(0.5)
    driver.close()
    driver.switch_to.window(driver.window_handles[2])

if __name__ == '__main__':
    selenium_base()