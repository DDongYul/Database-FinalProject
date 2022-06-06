from numpy import append
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup

goto_page = '1'
goto_movie_id = '191613'
page_is_ok = False
movie_is_ok = False

one_movie_inform_tuple_buf = ()
one_movie_nation_tuples_buf = []
one_movie_genre_tuples_buf = []
one_movie_photo_tuples_buf = []
one_movie_netizen_review_tuples_buf = []
one_movie_journal_review_tuples_buf = []
one_movie_dir_tuples_buf = []
one_movie_dir_movie_tuples_buf = []
one_movie_act_tuples_buf = []
one_movie_act_movie_tuples_buf = []

def dealing_exception(id, where, err_msg, cur, conn):
    cur.execute('insert into exception_table values (%s, %s, %s)', (id, where, err_msg))
    conn.commit()

def crawling_one_movie(id, driver, cur, conn):
    #임시 작성 실행시 delete
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    #
    
    global one_movie_inform_tuple_buf
    global one_movie_nation_tuples_buf
    global one_movie_genre_tuples_buf
    global one_movie_photo_tuples_buf
    global one_movie_netizen_review_tuples_buf
    global one_movie_journal_review_tuples_buf
    global one_movie_dir_tuples_buf
    global one_movie_dir_movie_tuples_buf
    global one_movie_act_tuples_buf
    global one_movie_act_movie_tuples_buf
    
    main_html = driver.page_source
    main_soup = BeautifulSoup(main_html,'html.parser')
    
    #영화 기본정보 크롤링 
    try:   
        #id
        one_movie_inform_list = []
        one_movie_inform_list.append(id)
        #size1
        
        #title
        title = main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
        if(len(title) > 40):
            title = title[:40]
        one_movie_inform_list.append(title)
        #size2
        
        infospec_dd_list = main_soup.select('#content > div.article > div.mv_info_area > div.mv_info > dl > dd')
        #개요
        if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step1') is not None:
            infospec_dd_summary = infospec_dd_list.pop(0)
            infospec_dd_summary_span_list = infospec_dd_summary.select('p > span')
            infospec_dd_summary_span_inform_list = [None, None]
            for infospec_dd_summary_span in infospec_dd_summary_span_list:
                if infospec_dd_summary_span.select_one('a') is None:#playtime에 대한 정보
                    infospec_dd_summary_span_inform_list[0] = infospec_dd_summary_span.text[:-2]
                elif infospec_dd_summary_span.text.find('개봉') != -1:#openingdate
                    open_date_atag_list = infospec_dd_summary_span.select('a')
                    open_date = open_date_atag_list[-2].text.lstrip() + open_date_atag_list[-1].text.replace('.','')
                    infospec_dd_summary_span_inform_list[1] = open_date
                elif infospec_dd_summary_span.select_one('a').attrs['href'].find('nation') != -1:#movie_nation
                    nation_atag_list = infospec_dd_summary_span.select('a')
                    for nation_atag in nation_atag_list:
                        one_movie_nation_tuples_buf.append((id, nation_atag.text))
                elif infospec_dd_summary_span.select_one('a').attrs['href'].find('genre') != -1:#movie_genre
                    genre_atag_list = infospec_dd_summary_span.select('a')
                    for genre_atag in genre_atag_list:
                        one_movie_genre_tuples_buf.append((id,genre_atag.text))
            one_movie_inform_list.extend(infospec_dd_summary_span_inform_list)
        else:
            one_movie_inform_list.extend([None, None])
        #size4
        
        #infospec_dd_list에서 감독에 대한 정보 제거
        if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step2') is not None:
            infospec_dd_list.pop(0)
            
        #infospec_dd_list에서 출연진에 대한 정보 제거
        if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step3') is not None:
            infospec_dd_list.pop(0)
            
        #movierate
        if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step4') is not None:
            infospec_dd_rate = infospec_dd_list.pop(0)
            movierate = infospec_dd_rate.select_one('p > a').text
            one_movie_inform_list.append(movierate)
        else:
            one_movie_inform_list.append(None)
        #size5
        
        #exp, non_exp_score 항상 존재한다.
        exp_box = main_soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score > div.exp_area > div')
        exp_score = exp_box.select_one('div.exp_info > span#interest_cnt_basic > em').next_sibling.replace(',','')
        non_exp_score = exp_box.select_one('div.exp_info > span#not_interest_cnt_basic > em').next_sibling.replace(',','')
        one_movie_inform_list.extend([exp_score, non_exp_score])
        #size7
        
        #netizen, journal score count
        score_area = main_soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score > div.score_area')
        score_count_list = [None, None, None, None]
        if score_area is not None:
            #netizen score,count
            netizen_count = score_area.select_one('div.netizen_score < div.sc_view > span.user_count > em').text.replace(',','')
            if netizen_count != '0':
                netizen_score = score_area.select_one('div.netizen_score > div.sc_view > div.star_score > em').text
                score_count_list[0] = netizen_score
                score_count_list[1] = netizen_count
            
            #journal score,count
            journal_count = score_area.select_one('div.special_score > div.sc_view > span.user_count > em').text.replace(',','')
            if journal_count != '0':
                journal_score = score_area.select_one('div.special_score > div.sc_view > div.star_score > em').text
                score_count_list[2] = journal_score
                score_count_list[3] = journal_count
        one_movie_inform_list.extend(score_count_list)
        #size11
    except Exception as e:
        dealing_exception(id, 'movie_inform_crawling', str(e), cur, conn)
        return False
    #영화 기본정보 크롤링
    
    return True    
            
    
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
    return cur_url.split('code=')[-1]

def main():
    global goto_page
    global goto_movie_id
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
        #goto
        if page_is_ok == False and driver.current_url.split('page=')[-1] != goto_page:
            driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
            continue
        else:
            page_is_ok = True
            
        #하나의 랭킹 웹페이지에서 무비링크 따오기        
        movie_link_list = driver.find_elements_by_css_selector('#old_content > table > tbody > tr > td.title > div > a')   
             
        for movie_link in movie_link_list:#하나의 영화 웹페이지 들어가서 그 영화에 대해서 크롤링하기
            #영화 웹페이지 새탭에 띄우고 탭 바꾸기
            movie_link.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[1])
            
            #goto
            if movie_is_ok == False and driver.current_url.split('code=')[-1] != goto_movie_id:
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue
            else:
                movie_is_ok = True
            
            #crawling......
            # crawling_one_movie(url_to_id(driver.current_url), driver)
            
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