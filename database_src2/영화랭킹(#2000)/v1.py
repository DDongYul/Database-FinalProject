from sqlite3 import Cursor
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip
import time
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException

#너는내운명
goto_page = '9'
goto_movie_id = '39654'
page_is_ok = False
movie_is_ok = False

one_movie_inform_tuple_buf = ()
one_movie_nation_tuples_buf = []
one_movie_genre_tuples_buf = []
one_movie_photo_tuples_buf = []
one_movie_netizen_review_tuples_buf = []
one_movie_journal_review_tuples_buf = []
one_movie_dir_tuples_buf = []
one_movie_movie_dir_tuples_buf = []
one_movie_act_tuples_buf = []
one_movie_movie_act_tuples_buf = []

    
def url_to_id(cur_url : str):
    return cur_url.split('code=')[-1]

def check_exists_by_css_select(driver : webdriver.Chrome, css_path : str):
    try:
        driver.find_element_by_css_selector(css_path)
    except NoSuchElementException:
        return False
    return True

def dealing_exception(id : str, where : str, err_msg : str, conn : pymysql.Connection, cur : Cursor):
    global one_movie_inform_tuple_buf
    global one_movie_nation_tuples_buf
    global one_movie_genre_tuples_buf
    global one_movie_photo_tuples_buf
    global one_movie_netizen_review_tuples_buf
    global one_movie_journal_review_tuples_buf
    global one_movie_dir_tuples_buf
    global one_movie_movie_dir_tuples_buf
    global one_movie_act_tuples_buf
    global one_movie_movie_act_tuples_buf
        
    cur.execute('insert into exception_table(movie_id, _where, err_msg) values (%s, %s, %s)', (id, where, err_msg))
    conn.commit()
    
    one_movie_inform_tuple_buf = ()
    one_movie_nation_tuples_buf = []
    one_movie_genre_tuples_buf = []
    one_movie_photo_tuples_buf = []
    one_movie_netizen_review_tuples_buf = []
    one_movie_journal_review_tuples_buf = []
    one_movie_dir_tuples_buf = []
    one_movie_movie_dir_tuples_buf = []
    one_movie_act_tuples_buf = []
    one_movie_movie_act_tuples_buf = []

def sql_insert_query(movie_id : str, conn : pymysql.Connection, cur : Cursor):
    global one_movie_inform_tuple_buf
    global one_movie_nation_tuples_buf
    global one_movie_genre_tuples_buf
    global one_movie_photo_tuples_buf
    global one_movie_netizen_review_tuples_buf
    global one_movie_journal_review_tuples_buf
    global one_movie_dir_tuples_buf
    global one_movie_movie_dir_tuples_buf
    global one_movie_act_tuples_buf
    global one_movie_movie_act_tuples_buf
    
    #movie insert
    try:
        movie_insert_sql = """insert into movie(movie_id, title, playtime, open_date, movie_rate, story, exp_score, non_exp_score, netizen_score, netizen_count, journal_score, journal_count)
                            values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        cur.execute(movie_insert_sql, one_movie_inform_tuple_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie', str(e), conn, cur)
        return
    
    #movie_nation insert
    try:
        cur.executemany('insert into movie_nation(movie_id, nation) values(%s, %s);', one_movie_nation_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_nation', str(e), conn, cur)
        return
    
    #movie_genre insert
    try:
        cur.executemany('insert into movie_genre(movie_id, genre) values (%s, %s);', one_movie_genre_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_genre', str(e), conn, cur)
        return
    
    #movie_photo
    try:
        cur.executemany('insert into movie_photo(movie_id, photo_link) values (%s, %s);', one_movie_photo_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_photo', str(e), conn, cur)
        return
    
    #movie_netizen_review
    try:
        cur.executemany('insert into movie_netizen_review(movie_id, user_name, score, review, good, bad) values (%s, %s, %s, %s, %s, %s);', one_movie_netizen_review_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_netizen_review', str(e), conn, cur)
        return
    
    #movie_journal_review
    try:
        cur.executemany('insert into movie_journal_review(movie_id, journal_name, score, title, review) values (%s, %s, %s, %s, %s);', one_movie_journal_review_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_journal_review', str(e), conn, cur)
        return        
    
    #actor_insert
    try:
        cur.executemany('insert into actor(act_id, act_name, act_birth, act_awards, act_profile) values(%s, %s, %s, %s, %s);', one_movie_act_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert actor', str(e), conn, cur)
        return
    
    #movie_act insert
    try:
        cur.executemany('insert into movie_act(movie_id, act_id, casting, is_main) values(%s, %s, %s, %s);', one_movie_movie_act_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_act', str(e), conn, cur)
        return
    
    #director insert    
    try:
        cur.executemany('insert into director(dir_id, dir_name, dir_birth, dir_awards, dir_profile) values(%s, %s, %s, %s, %s);', one_movie_dir_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert director', str(e), conn, cur)
        return
    
    #movie_director insert
    try:
        cur.executemany('insert into movie_dir(movie_id, dir_id) values(%s, %s);', one_movie_movie_dir_tuples_buf)
        conn.commit()
    except Exception as e:
        dealing_exception(movie_id, 'insert movie_dir', str(e), conn, cur)
        return
    
    one_movie_inform_tuple_buf = ()
    one_movie_nation_tuples_buf = []
    one_movie_genre_tuples_buf = []
    one_movie_photo_tuples_buf = []
    one_movie_netizen_review_tuples_buf = []
    one_movie_journal_review_tuples_buf = []
    one_movie_dir_tuples_buf = []
    one_movie_movie_dir_tuples_buf = []
    one_movie_act_tuples_buf = []
    one_movie_movie_act_tuples_buf = []


def crawling_one_movie(movie_id : str, driver : webdriver.Chrome,  conn : pymysql.Connection, cur : Cursor):
    
    global one_movie_inform_tuple_buf
    global one_movie_nation_tuples_buf
    global one_movie_genre_tuples_buf
    global one_movie_photo_tuples_buf
    global one_movie_netizen_review_tuples_buf
    global one_movie_journal_review_tuples_buf
    global one_movie_dir_tuples_buf
    global one_movie_movie_dir_tuples_buf
    global one_movie_act_tuples_buf
    global one_movie_movie_act_tuples_buf
    
    main_html = driver.page_source
    main_soup = BeautifulSoup(main_html,'html.parser')
    
    #영화 기본정보 크롤링   
    #id
    one_movie_inform_list = []
    one_movie_inform_list.append(movie_id)
    #size1
    try:     
        #title
        title = main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > h3 > a:nth-child(1)').text
        if(len(title) > 40):
            title = title[:40]
        one_movie_inform_list.append(title)
        #size2
    except Exception as e:
        dealing_exception(movie_id, 'crawling_title', str(e), conn, cur)
        return 1
    
    try:    
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
                        one_movie_nation_tuples_buf.append((movie_id, nation_atag.text))
                elif infospec_dd_summary_span.select_one('a').attrs['href'].find('genre') != -1:#movie_genre
                    genre_atag_list = infospec_dd_summary_span.select('a')
                    for genre_atag in genre_atag_list:
                        one_movie_genre_tuples_buf.append((movie_id,genre_atag.text))
            one_movie_inform_list.extend(infospec_dd_summary_span_inform_list)
        else:
            one_movie_inform_list.extend([None, None])
        #size4
    except Exception as e:
        dealing_exception(movie_id, 'crawling summary', str(e), conn, cur)
        return 1
    
    #infospec_dd_list에서 감독에 대한 정보 제거
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step2') is not None:
        infospec_dd_list.pop(0)
        
    #infospec_dd_list에서 출연진에 대한 정보 제거
    if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step3') is not None:
        infospec_dd_list.pop(0)
    
    try:        
        #movierate
        if main_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info > dl > dt.step4') is not None:
            infospec_dd_rate = infospec_dd_list.pop(0)
            movierate = infospec_dd_rate.select_one('p > a').text
            one_movie_inform_list.append(movierate)
        else:
            one_movie_inform_list.append(None)
        #size5
    except Exception as e:
        dealing_exception(movie_id, 'crawling rate', str(e), conn, cur)
        return 1
    
    try:
        if check_exists_by_css_select(driver, '#content > div.article > div.section_group.section_group_frst > div > div > div.story_area > p'):
            story = driver.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst > div > div > div.story_area > p').text
            one_movie_inform_list.append(story)
        else:
            one_movie_inform_list.append(None)
    except Exception as e:
        dealing_exception(movie_id, 'crawling story', str(e), conn, cur)
        return 1
    #size6
    
    try:    
        #exp, non_exp_score 항상 존재한다.
        exp_box = main_soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score > div.exp_area > div')
        exp_score = exp_box.select_one('div.exp_info > span#interest_cnt_basic > em').next_sibling.replace(',','')
        non_exp_score = exp_box.select_one('div.exp_info > span#not_interest_cnt_basic > em').next_sibling.replace(',','')
        one_movie_inform_list.extend([exp_score, non_exp_score])
        #size8
    except Exception as e:
        dealing_exception(movie_id, 'crawling expect', str(e), conn, cur)
        return 1
    
    try:    
        #netizen, journal score count
        score_area = main_soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score > div.score_area')
        score_count_list = [None, None, None, None]
        if score_area is not None:
            #netizen score,count
            netizen_count = score_area.select_one('div.netizen_score > div.sc_view > span.user_count > em').text.replace(',','')
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
        #size12
    except Exception as e:
        dealing_exception(movie_id, 'crawling score count', str(e), conn, cur)
        return 1
    one_movie_inform_tuple_buf = tuple(one_movie_inform_list)
    #영화 기본정보 크롤링
    
    #탭 메뉴들에 대하여 크롤링
    tab_menu_li_a_tag_list = driver.find_elements_by_css_selector('#movieEndTabMenu > li > a')
    for tab_menu_li_a_tag in tab_menu_li_a_tag_list:
        if tab_menu_li_a_tag.get_attribute('title') == '배우/제작진':#배우, 감독에 대해 크롤링 하고 buffer들에 저장
            tab_menu_li_a_tag.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[2])
            #펼쳐보기
            if check_exists_by_css_select(driver, '#actorMore'):
                driver.find_element_by_css_selector('#actorMore').click()   
                          
            dir_actor_list_html =  driver.page_source
            dir_actor_list_soup = BeautifulSoup(dir_actor_list_html, 'html.parser')
            
            div_obj_section_list = dir_actor_list_soup.select('#content > div.article > div.section_group.section_group_frst > div')
            for div_obj_section in div_obj_section_list:
                if div_obj_section.select_one('div > div.title_area > h4 > strong').text == '배우':                   
                    actor_link_list = driver.find_elements_by_css_selector('#content > div.article > div.section_group.section_group_frst > div.obj_section.noline > div > div.lst_people_area.height100 > ul > li > div > a')
                    for actor_link in actor_link_list:
                        actor_id = url_to_id(actor_link.get_attribute('href'))
                        cur.execute('select * from actor where act_id = %s', (actor_id))
                        if not cur.fetchone():#해당하는 배우에 대해 record가 없는 경우, 그 배우에 대해 record를 만들어야 한다.                        
                            actor_link.send_keys(Keys.CONTROL + '\n')
                            driver.switch_to.window(driver.window_handles[3])
                            #하나의 배우에 대한 웹페이지로 들어옴
                            one_actor_inform_list = []
                            one_actor_inform_list.append(actor_id)
                            #size1
                            
                            one_actor_html = driver.page_source
                            one_actor_soup = BeautifulSoup(one_actor_html, 'html.parser')
                            try:
                                #이름 무조건 존재한다.
                                act_name = one_actor_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
                                if len(act_name) > 30:
                                    act_name = act_name[:30]
                                one_actor_inform_list.append(act_name)
                                #size2
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one actor name', str(e), conn, cur)
                                return 3
                            
                            try:    
                                act_info_spec_dd_list = one_actor_soup.select('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd')
                                #출생
                                if one_actor_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5') is not None:
                                    birth = act_info_spec_dd_list.pop(0).text.replace('\n','').replace('\t','')
                                    one_actor_inform_list.append(birth)
                                else:
                                    one_actor_inform_list.append(None)
                                #size3
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one actor birth', str(e), conn, cur)
                                return 3
                                
                            if one_actor_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step7') is not None:
                                act_info_spec_dd_list.pop(0)

                            try:    
                                #수상경력
                                if one_actor_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step8') is not None:
                                    awards = act_info_spec_dd_list.pop(0).text.replace('\t','').replace('\n','')
                                    one_actor_inform_list.append(awards)
                                else:
                                    one_actor_inform_list.append(None)
                                #size4
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one actor awards', str(e), conn, cur)
                                return 3
                                
                            try:    
                                #프로필
                                if check_exists_by_css_select(driver, '#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx'):
                                    profile = driver.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx').text
                                    one_actor_inform_list.append(profile)
                                else:
                                    one_actor_inform_list.append(None)
                                #size5
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one actor profile', str(e), conn, cur)
                                return 3
                            one_movie_act_tuples_buf.append(tuple(one_actor_inform_list))
                                                                                                                                                                                                                            
                            driver.close()
                            driver.switch_to.window(driver.window_handles[2])
                            #하나의 배우에 대한 크롤링 완료
                    
                    #중복제거
                    one_movie_act_tuples_buf = list(dict.fromkeys(one_movie_act_tuples_buf)) 
                    #배우/제작진 웹페이지로 돌아옴
                    
                    #movie_act_table에 대한 buf채워넣기
                    try:
                        act_litag_list = div_obj_section.select('div > div.lst_people_area > ul > li')
                        for act_litag in act_litag_list:
                                                       
                            if act_litag.select_one('div > a') is None: #배우에 대한 페이지가 따로 없을 수도 있음 즉 배우이름이 링크로 되어 있지 않은 경우 그냥 제외
                                continue
                            
                            #id
                            tmp_act_id = url_to_id(act_litag.select_one('div > a').attrs['href'])
                            #주연 여부
                            is_Main = ''
                            if act_litag.select_one('div > div > p.in_prt > em') is not None:
                                is_Main_str = act_litag.select_one('div > div > p.in_prt > em').text
                                if is_Main_str == '주연':
                                    is_Main = '1'
                                else:
                                    is_Main = '0'
                            else :#impossible
                                is_Main = None
                            #역할
                            casting = ''
                            if act_litag.select_one('div > div > p.pe_cmt > span') is not None:
                                casting = act_litag.select_one('div > div > p.pe_cmt > span').text
                            else:
                                casting = None
                            one_movie_movie_act_tuples_buf.append((movie_id, tmp_act_id, casting, is_Main))
                    except Exception as e:
                        dealing_exception(movie_id, 'crawling movie act table', str(e), conn, cur)
                        return 2                                                    
                    
                elif div_obj_section.select_one('div > div.title_area > h4 > strong').text == '감독':#감독 section
                    dir_link_list = driver.find_elements_by_css_selector('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.director > div.dir_obj > div > a')
                    for dir_link in dir_link_list:
                        dir_id = url_to_id(dir_link.get_attribute('href'))
                        cur.execute('select * from director where dir_id = %s', (dir_id))
                        if not cur.fetchone():#감독에 대한 record가 없어서 감독에 대한 record만듬
                            dir_link.send_keys(Keys.CONTROL + '\n')
                            driver.switch_to.window(driver.window_handles[3])
                            one_dir_inform_list = []
                            
                            #id
                            one_dir_inform_list.append(dir_id)
                            #size1
                            
                            one_dir_html = driver.page_source
                            one_dir_soup = BeautifulSoup(one_dir_html, 'html.parser')
                            try:
                                #이름
                                dir_name = one_dir_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > h3 > a').text
                                if len(dir_name) > 30:
                                    dir_name = dir_name[:30]
                                one_dir_inform_list.append(dir_name)
                                #size2
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one dir name', str(e), conn, cur)
                                return 3
                            
                            try:    
                                dir_info_spec_dd_list = one_dir_soup.select('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd')
                                
                                #출생                          
                                if one_dir_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step5') is not None:
                                    birth = dir_info_spec_dd_list.pop(0).text.replace('\t','').replace('\n','')
                                    one_dir_inform_list.append(birth)
                                else:
                                    one_dir_inform_list.append(None)
                                #size3
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one dir birth', str(e), conn, cur)
                                return 3
                                
                            #필모그래프 dd tag 빼내기                 
                            if one_dir_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step7') is not None:
                                dir_info_spec_dd_list.pop(0)
                            
                            try:        
                                #수상경력                            
                                if one_dir_soup.select_one('#content > div.article > div.mv_info_area > div.mv_info.character > dl > dt.step8') is not None:
                                    awards = dir_info_spec_dd_list.pop(0).text.replace('\n','').replace('\t','')
                                    one_dir_inform_list.append(awards)
                                else:
                                    one_dir_inform_list.append(None)                            
                                #size4
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one dir awards', str(e), conn, cur)
                                return 3
                            
                            try:    
                                #프로필
                                if check_exists_by_css_select(driver, '#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx'):
                                    profile = driver.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx').text
                                    one_dir_inform_list.append(profile)
                                else:
                                    one_dir_inform_list.append(None)                            
                                #size5
                            except Exception as e:
                                dealing_exception(movie_id, 'crawling one dir profile', str(e), conn, cur)
                                return 3
                            
                            #버퍼에 넣기
                            one_movie_dir_tuples_buf.append(tuple(one_dir_inform_list))

                            driver.close()
                            driver.switch_to.window(driver.window_handles[2])

                    #배우 / 제작진 웹페이지로 돌아옴
                    
                    #movie_dir_buf채워넣기
                    try:
                        dir_obj_list = div_obj_section.select('div > div.dir_obj')
                        for dir_obj in dir_obj_list:
                            tmp_dir_id = url_to_id(dir_obj.select_one('div > a').attrs['href'])
                            one_movie_movie_dir_tuples_buf.append((movie_id, tmp_dir_id))
                    except Exception as e:
                        dealing_exception(movie_id, 'crawling movie dir', str(e), conn, cur)
                        return 2          
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
        elif tab_menu_li_a_tag.get_attribute('title') == '포토':
            tab_menu_li_a_tag.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[2])
            
            #포토탭 들어와서 포토 따오기
            driver.find_element_by_css_selector('#photo_area > div > div.title_area > div > div.btn_view_mode > a.cick_off').click()
            try:
                while True:
                    imgsrc_tag_list = driver.find_elements_by_css_selector('#gallery_group > li > a > img')
                    for imgsrc_tag in imgsrc_tag_list:
                        one_movie_photo_tuples_buf.append((movie_id, imgsrc_tag.get_attribute('src')))
                                            
                    if check_exists_by_css_select(driver, 'a.pg_next > em'):
                        driver.find_element_by_css_selector('a.pg_next > em').click()
                    else:
                        break    
            except Exception as e:
                dealing_exception(movie_id, 'crawling photo', str(e), conn, cur)
                return 2
            #포토탭 들어와서 포토 따오기            
            
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
        elif tab_menu_li_a_tag.get_attribute('title') == '평점':
            tab_menu_li_a_tag.send_keys(Keys.CONTROL + '\n')
            driver.switch_to.window(driver.window_handles[2])
            
            #평점 탭에 들어옴
            
            #네티즌
            link_to_ntz_review = driver.find_element_by_css_selector('#pointAfterListIframe').get_attribute('src')
            exec_txt = 'window.open("' + link_to_ntz_review + '")'
            driver.execute_script(exec_txt)
            driver.switch_to.window(driver.window_handles[3])
            #네티즌 리뷰 탭에 들어옴
            ntz_review_html = driver.page_source
            ntz_review_soup = BeautifulSoup(ntz_review_html,'html.parser')
            try:
                ntz_litag_list = ntz_review_soup.select('body > div > div > div.score_result > ul > li')
                for ntz_litag in ntz_litag_list:
                    ntz_score = ntz_litag.select_one('div.star_score > em').text
                    ntz_name = ntz_litag.select_one('div.score_reple > dl > dt > em > a').text.replace('\n','').replace('\\','')
                    ntz_review_text = ntz_litag.select('div.score_reple > p > span')[-1].text.replace('\t','').replace('\n','')
                    good_count = ntz_litag.select_one('div.btn_area > a._sympathyButton > strong').text
                    bad_count = ntz_litag.select_one('div.btn_area > a._notSympathyButton > strong').text
                    one_movie_netizen_review_tuples_buf.append((movie_id, ntz_name, ntz_score, ntz_review_text, good_count, bad_count))
            except Exception as e:
                dealing_exception(movie_id, 'netizen review crawling', str(e), conn, cur)
                return 3            
            driver.close()
            driver.switch_to.window(driver.window_handles[2])            
            #네티즌....
            
            #평점 탭에 돌아옴
            #평론가
            all_review_html = driver.page_source
            all_review_soup = BeautifulSoup(all_review_html,'html.parser')
            div_score_special = all_review_soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score_special')
            if div_score_special is not None:#평론가 평점 존재
                try:
                    reporter = div_score_special.select_one('div.reporter')
                    if reporter is not None:
                        rep_li_tag_list = reporter.select('ul > li')
                        for rep_li_tag in rep_li_tag_list:
                            rep_name = rep_li_tag.select_one('div.reporter_line > dl > dt > a').text
                            rep_title = rep_li_tag.select_one('div.reporter_line > dl > dd').text
                            rep_score = rep_li_tag.select_one('div.re_score_grp > div > div > em').text
                            rep_review_txt = rep_li_tag.select_one('p.tx_report').text
                            one_movie_journal_review_tuples_buf.append((movie_id, rep_name, rep_score, rep_title, rep_review_txt))
                    score140 = div_score_special.select_one('div.score140')
                    if score140 is not None:
                        sc_li_tag_list = score140.select('div > ul > li')
                        for sc_li_tag in sc_li_tag_list:
                            sc_score = sc_li_tag.select_one('div.star_score > em').text
                            sc_review_txt = sc_li_tag.select_one('div.score_reple > p').text
                            sc_name = sc_li_tag.select_one('div.score_reple > dl > dd').text.replace('\n','').replace('\t','').lstrip('| ')
                            one_movie_journal_review_tuples_buf.append((movie_id, sc_name, sc_score, None, sc_review_txt))
                except:
                    dealing_exception(movie_id, 'crawling journal review', str(e), conn, cur)
            #평론가.....
            
            driver.close()
            driver.switch_to.window(driver.window_handles[1])
    
    return 0    
            
    
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
            res = crawling_one_movie(url_to_id(driver.current_url), driver, conn, cur)
            if(res == 0):
                sql_insert_query(url_to_id(driver.current_url), conn, cur)        
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            else:
                for window in reversed(driver.window_handles):
                    driver.switch_to.window(window)
                    if window == driver.window_handles[0]:
                        break
                    driver.close()
        
        #다음 페이지가 있으면 넘어가기
        if check_exists_by_css_select(driver, '#old_content > div.pagenavigation > table > tbody > tr > td.next > a'):
            driver.find_element_by_css_selector('#old_content > div.pagenavigation > table > tbody > tr > td.next > a').click()
        else:
            break
    
    
        
    driver.quit()
    close_db(conn,cur)


if __name__ == '__main__':
    main()