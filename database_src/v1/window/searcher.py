from PyQt5 import QtCore

#검색결과를 만족하는 movie_id 리스트를 반환 (data = 텍스트입력된거)
def search(menu, data):
    search_data = []
    if menu == 1:
        title = "temp"   #데이터베이스에서 title 가져와서
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(title)
        if(index != -1):
            search_data.append(movie_id)
    if menu == 2:
        actor = "temp"
        movie_id = "0"
        reg = QtCore.QRegExp(data)
        index = reg.indexIn(actor)
        if (index != -1):
            search_data.append(movie_id)
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
    print(menu , data)
    return search_data
