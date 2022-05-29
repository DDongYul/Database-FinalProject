import pymysql


def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur
    
def close_db(conn, cur):
    cur.close()
    conn.close()
    
def main():
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie_year.naver'

if __name__ == '__main__':
    main()