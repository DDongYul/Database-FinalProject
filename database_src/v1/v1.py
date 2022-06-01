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
    one_movie_inform_tuple = []
    #list of tuples, all elements append to table_buf
    one_movie_scope_tuples = []
    one_movie_actor_tuples = []
    
    #id
    one_movie_inform_tuple.append(id)
    #one_movie_infomr_tuple.size == 1
    
    #title
    #content > div.article > div.mv_info_area > div.mv_info > h3 > a
    title = main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
    if(len(title) > 30):
        title = title[0 : 30]
    one_movie_inform_tuple.append(title)
    #one_movie_infomr_tuple.size == 2
   
    #info_spec.....
    
    #info_spec의 dd tag리스트 개요 감독 출연 등급 흥행....
    infospec_dd_list = main_soup.select('content > div.article > div.mv_info_area > div.mv_info > dl > dd')
    
    #개요
    #infospec_dt_step1 = main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step1')
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step1') is not None: #개요에 해당하는 칸이 웹페이지에 존재, 무조건 존재해야한다.
        #개요를 분류에 맞게 parsing해야함
        infospec_dd_summary = infospec_dd_list.pop(0)
        infospec_dd_summary_span_list = infospec_dd_summary.select('p > span')
        infospec_dd_summary_span_inform_list = [None, None, None]
        for infospec_dd_summary_span in infospec_dd_summary_span_list:
            if infospec_dd_summary_span.select_one('a') is None: #playtime에 대한 span tag, 상영시간은 spantag에 바로 text가 붙어있음
                infospec_dd_summary_span_inform_list[1] = infospec_dd_summary_span.text[:-1]
            elif infospec_dd_summary_span.text.find('개봉') != -1: #openingdate에 대한 span tag, scope와 country의 domain에 '개봉'이 들어가는 경우 없음
                opening_date_str_list = infospec_dd_summary_span.select('a')
                opening_date_str = ''
                for opening_date_str_list_e in opening_date_str_list:#20220530 or 2023등의 문자열 형태로 DB에 저장됨                    
                    opening_date_str = opening_date_str + opening_date_str_list_e.text.replace('.','')
                infospec_dd_summary_span_inform_list[2] = opening_date_str
            elif infospec_dd_summary_span.select_one('a').attrs['href'].find('nation') != -1:#coutnry에 대한 spantag
                infospec_dd_summary_span_inform_list[0] = infospec_dd_summary_span.select_one('a').text
            else:#scope에 대한 tuple(id,scope)를 one_movie_scope_tuples에 차례대로 저장
                infospec_dd_summary_spanofscope_a_list = infospec_dd_summary_span.select('a')
                for infospec_dd_summary_spanofscope_a in infospec_dd_summary_spanofscope_a_list:
                    one_movie_scope_tuples.append((id, infospec_dd_summary_spanofscope_a.text))
        one_movie_inform_tuple.extend(infospec_dd_summary_span_inform_list)
    else:#scope, country, playtime, opendate가 존재 x
        one_movie_inform_tuple.extend([None,None,None])
    #one_movie_infomr_tuple.size == 5    
        
    
    #감독
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step2') is not None: #감독에 해당하는 칸이 웹페이지에 존재하는지?
        infospec_dd_director = infospec_dd_list.pop(0)
        one_movie_inform_tuple.append(infospec_dd_director.select_one('p > a').text)
    else:
        one_movie_inform_tuple.append(None)
    #size 6
    
    #등급
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step4') is not None:#등급엡 해당하는 칸이 웹페이지에 존재하는가?
        infospec_dd_movirate = infospec_dd_list.pop(0)
        one_movie_inform_tuple.append(infospec_dd_movirate.select_one('p > a').text)
    else:
        one_movie_inform_tuple.append(None)
    #size7
    
    #흥행
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step9') is not None:#흥행(누적 관객수에 해당하는 칸이 웹페이지에 존재하는가?)
        infospec_dd_audiencecount = infospec_dd_list.pop(0)
        one_movie_inform_tuple.append(infospec_dd_audiencecount.select_one('div > p > span').previous_sibling.replace(',','').replace('명',''))
    else:
        one_movie_inform_tuple.append(None)
    #size8
    
    #배우 배우칸은 항상 존재(?)
    #배우에 대한 정보창 새탭에 띄우기
    driver.find_element_by_css_selector('#movieEndTabMenu > li:nth-child(2) > a').send_keys(Keys.CONTROL + '\n')
    driver.switch_to.window(driver.window_handles[3])
    actor_html = driver.page_source
    actor_soup = BeautifulSoup(actor_html,'html.parser')
    if actor_soup.select_one('#content > div.article > div.section_group.section_group_frst > div > div.made_people') is not None:#배우에 대한 section이 존재한다.
        li_tag_actor_list = actor_soup.select('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li')
        for li_tag_actor in li_tag_actor_list:
            one_movie_actor_tuples.append((id,li_tag_actor.select_one('div > a').text))   
    #새탭 닫기, 배우에 대한 정보 모두 수집 완료
    driver.close()
    driver.switch_to.window(driver.window_handles[2])
    
    #photo link
    
    
    
    
    
    
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
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src/chromedriver.exe')
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
                
            #다음 버튼 없을시 break    
            if driver.find_elements_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a'):
                driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
            else:
                break
        #해당 년도에 대한 탭(웹페이지) 닫고 다시 맨 처음 웹페이지로 돌아가기       
        driver.close()
        driver.switch_to.window(driver.window_handles[0])        
                
    #db닫기            
    close_db(conn,cur)
    #chromedriver닫기
    driver.quit()
    
if __name__ == '__main__':
    main()