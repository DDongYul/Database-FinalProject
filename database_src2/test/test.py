from multiprocessing.connection import Connection
from sqlite3 import Cursor
from this import d
from time import time
import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

def check_exists_by_css_select(driver : webdriver.Chrome, css_path : str):
    try:
        driver.find_element_by_css_selector(css_path)
    except NoSuchElementException:
        return False
    return True

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn : pymysql.Connection, cur : Cursor):
    cur.close()
    conn.close()
    
def conn_cur_test(conn : pymysql.Connection, cur : Cursor):
    sql = """insert into test_ex_many values(%s)"""
    cur.executemany(sql, ['1','2','3'])
    conn.commit()
    
    cur.executemany(sql, [])
    conn.commit
    
def list_zero_test():
    
    conn, cur = open_db()
    conn_cur_test(conn, cur)    
    close_db(conn, cur)
    
def fetch_test(id):
    sql = "select * from test_ex_many where id = %s"
    conn, cur = open_db()
    cur.execute(sql, (id))
    if cur.fetchone():
        print('yes')
    else:
        print('no')
    
    close_db(conn, cur)

def crawling_exp_test():
    url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=192608'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    exp_box = soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div.score > div.exp_area > div')
    exp_score = exp_box.select_one('div.exp_info > span#interest_cnt_basic > em').next_sibling.replace(',','')
    non_exp_score = exp_box.select_one('div.exp_info > span#not_interest_cnt_basic > em').next_sibling.replace(',','')
    print(non_exp_score)
    
def driver_attr_test():
    url = 'https://movie.naver.com/movie/bi/mi/basic.naver?code=192608'
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get(url)
    
    tab_menu_li_a_tag_list = driver.find_elements_by_css_selector('#movieEndTabMenu > li > a')
    for tab_menu_li_a_tag in tab_menu_li_a_tag_list:
        print(tab_menu_li_a_tag.get_attribute('title'))
        tab_menu_li_a_tag.send_keys(Keys.CONTROL + '\n')
        driver.switch_to.window(driver.window_handles[1])
        time.sleep(0.5)
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
def photo_link_test():
    url = 'https://movie.naver.com/movie/bi/mi/photoView.naver?code=192608'
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get(url)
    
    while True:
        print(driver.find_element_by_css_selector('#photo_area > div > div.img_src._img_area > div > div > div > img').get_attribute('src'))
        if check_exists_by_css_select(driver, '#photo_area > div > div.img_src._img_area > div > div > a.pic_next._photo_next._NoOutline.none'):        
            break
        else:
           driver.find_element_by_css_selector('#photo_area > div > div.img_src._img_area > div > div > a.pic_next._photo_next._NoOutline').click()
           continue   

def profile_test():
    url = 'https://movie.naver.com/movie/bi/pi/basic.naver?code=102768'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get(url)
    # pf = soup.select_one('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx')
    driver.find_element_by_css_selector('#content > div.article > div.mv_info_area > div.mv_info.character > div.next_movie > a').send_keys(Keys.CONTROL + '\n')
    driver.switch_to.window(driver.window_handles[1])
    pf = driver.find_element_by_css_selector('#content > div.article > div.section_group.section_group_frst > div.obj_section > div > div.pf_intro > div.con_tx').text
    print(pf)
    print(len(pf))
    driver.quit()
    
def two_class_test():
    url = 'https://movie.naver.com/movie/bi/mi/detail.naver?code=192608'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    div_obj_section_list = soup.select('#content > div.article > div.section_group.section_group_frst > div')
    print(div_obj_section_list[0].text)
    
def None_test():
    casting = ''
    casting = None
    if casting is None:
        print('yes')
    
def Tab_test():
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get('https://naver.com')
    driver.execute_script('window.open("https://google.com")')
    driver.execute_script('window.open("https://google.com")')
    driver.execute_script('window.open("https://google.com")')
    for window in reversed(driver.window_handles):
        driver.switch_to.window(window)
        if window == driver.window_handles[0]:
            break
        driver.close()       
    a = driver.find_element_by_css_selector('#account > a')   
    a.send_keys(Keys.CONTROL + '\n')
    time.sleep(3)

def click_test():
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get('https://movie.naver.com/movie/bi/mi/point.naver?code=67786')
    driver.find_element_by_css_selector('label#actualYnLable').click()
    time.sleep(3)
    
def review_test():
    url = 'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code=217366&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    # li_list = soup.select('div.input_netizen > div.score_result > ul > li')
    li_list = soup.select('body > div > div > div.score_result > ul > li')
    # li_list = soup.select('body > div.basic > div.container > div#content > div.article > div.section_group.section_group_first > div.obj_section.noline > div.ifr_module2 > iframe.ifr > html > body')
    for li in li_list:
        lst = li.select('div.score_reple > p > span')
        x = lst[-1]
        txt = x.text.replace('\t','').replace('\n','')
        print(len(txt))
        print(txt)
        
def review_test2():
    driver = webdriver.Chrome(executable_path='C:/Users/junsub/study/2022_1/database_final_project/database_src2/chromedriver.exe')
    driver.get('https://movie.naver.com/movie/bi/mi/point.naver?code=192608')
    link = driver.find_element_by_css_selector('#pointAfterListIframe').get_attribute('src')
    print(link)
    exceution = 'window.open("' + link + '")'
    driver.execute_script(exceution)
    time.sleep(3)
    
if __name__ == '__main__':
    #  fetch_test('1')
    #  list_zero_test()
    #  fetch_test('2')
    #  list_zero_test()
    # fetch_test('5')
    # list_zero_test()
    # crawling_exp_test()
    # driver_attr_test()
    # photo_link_test()
    # profile_test()
    # two_class_test()
    # None_test()
    # Tab_test()
    # click_test()
    # review_test2()
    # review_test()
    Tab_test()