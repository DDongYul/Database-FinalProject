import pymysql
from bs4 import BeautifulSoup
from urllib.request import urlopen

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='naver_movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
def list_zero_test():
    sql = """insert into test_ex_many values(%s)"""
    conn, cur = open_db()
    
    cur.executemany(sql, ['1','2','3'])
    conn.commit()
    
    cur.executemany(sql, [])
    conn.commit
    
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
    
if __name__ == '__main__':
    # fetch_test('1')
    # list_zero_test()
    # fetch_test('2')
    # list_zero_test()
    # fetch_test('5')
    # list_zero_test()
    crawling_exp_test()