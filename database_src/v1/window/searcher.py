from PyQt5 import QtCore
import database as db

#검색결과를 만족하는 movie_id 리스트를 반환 (data = 텍스트입력된거)
def search(menu, data):
    search_data = []
    if menu == 1:
        title_list = db.get_allMovie()
        for i in range(0,title_list.__len__()):
            title = title_list[i][1]   #데이터베이스에서 title 가져와서
            movie_id = title_list[i][0]
            # index = title.find(data)
            reg = QtCore.QRegExp(data)
            index = reg.indexIn(title)
            if(index != -1):
                search_data.append(movie_id)
    if menu == 2:
        actor_list = db.get_allActor()
        for i in range(0,actor_list.__len__()):
            actor = actor_list[i][1]   #데이터베이스에서 title 가져와서
            actor_id = actor_list[i][0]
            reg = QtCore.QRegExp(data)
            index = reg.indexIn(actor)
            if(index != -1):
                search_data.append(actor_id)
    if menu == 3:
        director = "temp"
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(director)
        if (index != -1):
            search_data.append(movie_id)
    if menu == 4:
        genre = "temp"
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(genre)
        if (index != -1):
            search_data.append(movie_id)
    if menu == 5:
        year = "temp"
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(year)
        if (index != -1):
            search_data.append(movie_id)
    if menu == 6:
        country = "temp"
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(country)
        if (index != -1):
            search_data.append(movie_id)
    return search_data
