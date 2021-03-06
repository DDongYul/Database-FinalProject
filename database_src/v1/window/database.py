import pymysql


def open_db():
    conn = pymysql.connect(host='localhost', user='root',
                           password='rltkd3306!', db='naver_movie', unix_socket='/tmp/mysql.sock')

    cur = conn.cursor(pymysql.cursors.DictCursor)

    return conn, cur


def close_db(conn, cur):
    cur.close()
    conn.close()

def get_allMovie():
    conn1, cur1 = open_db()
    sql = """
        select movie_id,title
        from movie;
        """
    cur1.execute(sql)
    movie_title_list = []
    r = cur1.fetchone()
    while r:
        movie_title_list.append([r['movie_id'],r['title']])
        r=cur1.fetchone()
    return movie_title_list

def get_allActor():
    conn1, cur1 = open_db()
    sql = """
            select act_id,act_name
            from actor;
            """
    cur1.execute(sql)
    actor_list = []
    r = cur1.fetchone()
    while r:
        actor_list.append([r['act_id'], r['act_name']])
        r = cur1.fetchone()
    return actor_list

def get_allDirector():
    conn1, cur1 = open_db()
    sql = """
            select dir_id,dir_name
            from director;
            """
    cur1.execute(sql)
    director_list = []
    r = cur1.fetchone()
    while r:
        director_list.append([r['dir_id'], r['dir_name']])
        r = cur1.fetchone()
    return director_list

def getidWithTitle(title):      #영화 제목으로 id 받아옴
    conn1, cur1 = open_db()
    sql = """
    select movie_id
    from movie
    where title = "{0}";
    """.format(title)
    cur1.execute(sql)
    r = cur1.fetchone()
    if(r!=None):
        id = r['movie_id']
    else:
        id=0
    return id

def getAllDataWithId(id):       #해당 영화에 나오는 데이터를 movie 테이블에서 전부 가쟈옴
    conn1, cur1 = open_db()
    sql = """
        select *
        from movie
        where movie_id = '{0}';
        """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getACtorIdWithId(id):       #해당 영화에 나오는 배우들의 act_id를 전부 가져옴
    conn1, cur1 = open_db()
    sql = """
            select act_id
            from movie_actor
            where movie_id = '{0}';
            """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getActorNameWithActId(id):  #act_id에 해당하는 배우의 이름 조회
    conn1, cur1 = open_db()
    sql = """
                select act_name
                from actor
                where act_id = '{0}';
                """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getActIdWithActName(name):
    conn1, cur1 = open_db()
    sql = """
                    select act_id
                    from actor
                    where act_name = '{0}';
                    """.format(name)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getAllActDataWithId(id):
    conn1, cur1 = open_db()
    sql = """
           select *
          from actor
          where act_id = '{0}';
        """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getMovieListWithActId(id):  #배우 출연작
    conn1, cur1 = open_db()
    sql = """
            select movie_id
            from movie_actor
            where act_id = '{0}';
        """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getMovieListWithDirId(id):  #출연작
    conn1, cur1 = open_db()
    sql = """
            select movie_id
            from movie_director
            where dir_id = '{0}';
        """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getTitleWithId(id):
    conn1, cur1 = open_db()
    sql = """
                select title
                from movie
                where movie_id = '{0}';
            """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getDirectorIdWithId(id):    #해당 영화에 출연하는 감독의 dir_id를 가져옴
    conn1, cur1 = open_db()
    sql = """
                    select dir_id
                    from movie_director
                    where movie_id = '{0}';
                    """.format(id)
    cur1.execute(sql)
    r = cur1.fetchone()
    return r

def getDirectorNameWithDirId(id):
    conn1, cur1 = open_db()
    sql = """
                    select dir_name
                    from director
                    where dir_id = '{0}';
                    """.format(id)
    cur1.execute(sql)
    r = cur1.fetchone()
    return r

def getDirIdwithDirName(name):
    conn1, cur1 = open_db()
    sql = """
                select dir_id
                from director
                where dir_name = '{0}';
                """.format(name)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getDirectorIdWithDirectorName(name):
    conn1, cur1 = open_db()
    sql = """
                    select dir_id
                    from director
                    where dir_name = '{0}';
                    """.format(name)
    cur1.execute(sql)
    r = cur1.fetchall()
    id = r[0]['dir_id']
    return id

def getAllDirDataWithId(id):
    conn1, cur1 = open_db()
    sql = """
            select *
            from director
            where dir_id = '{0}';
                """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getNationWithId(id):
    conn1, cur1 = open_db()
    sql = """
            select nation
            from movie_nation
            where movie_id = '{0}';
        """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getGenreWithId(id):
    conn1, cur1 = open_db()
    sql = """
           select genre
           from movie_genre
           where movie_id = '{0}';
       """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

def getImgUrlWithId(id):
    conn1, cur1 = open_db()
    sql = """
           select photo_link
           from movie_photo
           where movie_id = '{0}';
       """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

#검색결과 반환
def print_Search_Movie(id):
    conn1, cur1 = open_db()
    sql = """
            select *
            from movie
            where movie_id = {0};
            """.format(id)
    cur1.execute(sql)
    r = cur1.fetchall()
    return r

    close_db(conn1, cur1)
# def get_actor():
#     conn1, cur1 = open_db()
#     sql = """
#     select *
#     from movie
#     where movie_id = '174830';
#     """
#     cur1.execute(sql)
#     r= cur1.fetchone()
#
#     close_db(conn1,cur1)
#     print(r)


