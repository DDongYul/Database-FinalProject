import pymysql

def open_db():
    conn = pymysql.connect(host='localhost', user='js_movie', password='jgtmapm3876', db='movie')
    cur = conn.cursor(pymysql.cursors.DictCursor)
    return conn, cur

def close_db(conn, cur):
    cur.close()
    conn.close()
    

if __name__ == '__main__':
    try:
        none = None
        str = none.text
    except Exception as e:
        conn, cur = open_db()
        str = str(e)
        tuple = (1, str)
        cur.execute('insert into exception_table values(%s, %s)', tuple)
        conn.commit()
        close_db(conn, cur)