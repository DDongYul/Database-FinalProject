import sys
import searcher
import database as db
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
import urllib.request
from PyQt5 import QtCore,QtWidgets

form_class = uic.loadUiType("mainActivity.ui")[0]
class WindowClass(QMainWindow,form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.searchButton.clicked.connect(self.groupboxRadFunction)
        self.sortNameButton.clicked.connect(self.sortNameButtonClick)
        self.sortYearButton.clicked.connect(self.sortYearButtonClick)
        self.sortRateButton.clicked.connect(self.sortRateButtonClick)

    def screenChangeToMovieInfo(self,id):
        self.window_movieinfo = WindowClassMovieInfo(id)
        self.window_movieinfo.exec_()

    def screenChangeToActorInfo(self, id):
        self.window_actorinfo = WindowClassActorInfo(id)
        self.window_actorinfo.exec_()

    def screenChangeToDirectorInfo(self, id):
        self.window_directorinfo = WindowClassDirectorInfo(id)
        self.window_directorinfo.exec_()

    #검색버튼 눌렀을 시 실행할 함수
    def searchButtonClick(self):
        print("search button clicked")

    #정렬 버튼 클릭시 실행할 함수
    def sortNameButtonClick(self):
        print("sortName button clicked")
    def sortYearButtonClick(self):
        print("sortYear button clicked")
    def sortRateButtonClick(self):
        print("sortName button clicked")

    # 레디오버튼 상태에 따라 검색함수 바뀌게
    def groupboxRadFunction(self) :
        if self.radioButtonTitle.isChecked() :
            self.listWidget.clear()
            searchdata = searcher.search(1, self.lineEdit.text())
            for i in range(0,searchdata.__len__()):
                data = db.print_Movie(searchdata[i])
                self.listWidget.addItem(data[0]['title'])
            self.listWidget.itemClicked.connect(lambda: self.screenChangeToMovieInfo(db.getidWithTitle(self.listWidget.currentItem().text())))

        elif self.radioButtonActor.isChecked() :
            self.listWidget2.clear()
            searchdata = searcher.search(2, self.lineEdit.text())
            print(searchdata)
            for i in range(0,searchdata.__len__()):
                data = db.getAllActDataWithId(searchdata[i])
                self.listWidget2.addItem(data[0]['act_name'])
            self.listWidget2.itemClicked.connect(lambda: self.screenChangeToActorInfo(db.getActIdWithActName(self.listWidget2.currentItem().text())[0]['act_id']))

        elif self.radioButtonDirector.isChecked() :
            self.listWidget3.clear()
            searchdata = searcher.search(3, self.lineEdit.text())
            print(searchdata)
            for i in range(0, searchdata.__len__()):
                data = db.getAllDirDataWithId(searchdata[i])
                self.listWidget3.addItem(data[0]['dir_name'])
            self.listWidget3.itemClicked.connect(
                lambda: self.screenChangeToDirectorInfo(db.getDirectorIdWithDirectorName(self.listWidget3.currentItem().text())))
        #
        # elif self.radioButtonGenre.isChecked() :
        #     searcher.search(4, self.lineEdit.text())
        # elif self.radioButtonYear.isChecked():
        #     searcher.search(5, self.lineEdit.text())
        # elif self.radioButtonCountry.isChecked():
        #     searcher.search(6, self.lineEdit.text())

#영화 상세정보 화면
form_class_movieInfo = uic.loadUiType("movie_info.ui")[0]
class WindowClassMovieInfo(QDialog,QWidget , form_class_movieInfo):
    def __init__(self,id):      #id는 movie_id
        super().__init__()
        self.setupUi(self)
        self.show()
        data = db.getAllDataWithId(id)              #[{'act_id': 1937}, {'act_id': 2028}....] 헝식
        print(data)
########################배우 데이터 처리#############################################################
        actor_id_list = db.getACtorIdWithId(id)     #[{'act_id': 1937}, {'act_id': 2028}] 형식
        actor_list = []
        for i in range(0,actor_id_list.__len__()):
            actor_list.append(db.getActorNameWithActId(actor_id_list[i]['act_id']))     #[[{'act_name': '임창정'}], [{'act_name': '하지원'}]형식
        actor_list2 = []
        for i in range(0,actor_list.__len__()):
            actor_list2.append(actor_list[i][0]['act_name'])        #['임창정', '하지원', '주현'] 형식
        for i in range(0,actor_list2.__len__()):
            self.listWidget_actor.addItem(actor_list2[i])
        def screenChangeToActorInfo(id):
            window_actorinfo = WindowClassActorInfo(id)
            window_actorinfo.exec_()
        self.listWidget_actor.itemClicked.connect(lambda: screenChangeToActorInfo(db.getActIdWithActName(self.listWidget_actor.currentItem().text())[0]['act_id']))
########################배우 데이터 처리#############################################################
########################감독 데이터 처리#############################################################
        director_id = db.getDirectorIdWithId(id)
        if(db.getDirectorNameWithDirId(director_id['dir_id'])!=None):
            director_name = db.getDirectorNameWithDirId(director_id['dir_id'])
            self.listWidget_director.addItem(director_name['dir_name'])
            def screenChangeToDirectorInfo(id):
                window_directorinfo = WindowClassDirectorInfo(id)
                window_directorinfo.exec_()
            self.listWidget_director.itemClicked.connect(lambda:screenChangeToDirectorInfo(db.getDirIdwithDirName(self.listWidget_director.currentItem().text())[0]['dir_id']))
        else:
            director_name = ""
########################감독 데이터 처리#############################################################
        nation = db.getNationWithId(id)[0]['nation']
        self.textEdit_country.setText(nation)

        genre = ""
        genre_list = db.getGenreWithId(id)
        print(genre_list)
        for i in range(0,genre_list.__len__()-1):
            genre+=genre_list[i]['genre']
            genre+= ","
        genre += genre_list[genre_list.__len__()-1]['genre']
        self.textEdit_genre.setText(genre)

        qPixmapvar = QPixmap()
        url_list = db.getImgUrlWithId(id)
        url = url_list[0]['photo_link']
        urlOpen = urllib.request.urlopen(url).read()
        qPixmapvar.loadFromData(urlOpen)
        self.label_img.setPixmap(qPixmapvar)
        def screenChangeToImageInfo(id):
            window_imageinfo = WindowClassImageInfo(id)
            window_imageinfo.exec_()
        self.pushButton_image.clicked.connect(lambda: screenChangeToImageInfo(id))

        self.textEdit_title.setText(data[0]['title'])
        self.textEdit_audienceRate.setText(str(data[0]['netizen_score']))
        self.textEdit_journalRate.setText(str(data[0]['journal_score']))
        self.textEdit_playTime.setText("상영시간: " + str(data[0]['playtime'])+"분")
        self.textEdit_openingDate.setText("개봉: " + str(data[0]['open_date']))
        self.textEdit_rate.setText(str(data[0]['movie_rate']))
        self.textEdit_story.setText(data[0]['story'])
        self.textEdit_exp_score.setText(str(data[0]['exp_score']))
        self.textEdit_non_exp_score.setText(str(data[0]['non_exp_score']))

        def actor_click(event):
            self.window_actorinfo = WindowClassActorInfo()
            self.window_actorinfo.exec_()

    def screenChangeToActor(self):
        self.window_actroinfo = WindowClassActorInfo()
        self.window_actroinfo.exec_()


form_class_actorInfo = uic.loadUiType("actor_info.ui")[0]
class WindowClassActorInfo(QDialog,QWidget ,form_class_actorInfo):
    def __init__(self,id):
        super().__init__()
        self.setupUi(self)
        self.show()

        act_data = db.getAllActDataWithId(id)
        print(act_data)
        self.textEdit_act_name.setText(act_data[0]['act_name'])
        if (act_data[0]['act_birth'] != None):
            self.textEdit_act_birth.setText(act_data[0]['act_birth'])
        else:
            self.textEdit_act_birth.setText("출생 정보 없음")

        if (act_data[0]['act_awards'] != None):
            self.textEdit_act_awards.setText(act_data[0]['act_awards'])
        else:
            self.textEdit_act_awards.setText("수상내역 정보 없음")

        if (act_data[0]['act_profile'] != None):
            self.textEdit_act_profile.setText(act_data[0]['act_profile'])
        else:
            self.textEdit_act_profile.setText("프로필 정보 없음")

        act_movieid_list = db.getMovieListWithActId(id)
        print(act_movieid_list)

        def screenChangeToMovieInfo(id):
            window_movieinfo = WindowClassMovieInfo(id)
            window_movieinfo.exec_()

        for i in range(0,act_movieid_list.__len__()):
            movie = db.getTitleWithId(act_movieid_list[i]['movie_id'])
            print(movie)
            movie = movie[0]['title']
            self.listWidget_movieList.addItem(movie)
        self.listWidget_movieList.itemClicked.connect(
            lambda: screenChangeToMovieInfo(db.getidWithTitle(self.listWidget_movieList.currentItem().text())))



form_class_directorInfo = uic.loadUiType("director_info.ui")[0]
class WindowClassDirectorInfo(QDialog,QWidget ,form_class_directorInfo):
    def __init__(self,id):
        super().__init__()
        self.setupUi(self)
        self.show()

        dir_data = db.getAllDirDataWithId(id)
        print(dir_data)
        self.textEdit_dir_name.setText(dir_data[0]['dir_name'])
        if(dir_data[0]['dir_birth']!=None):
            self.textEdit_dir_birth.setText(dir_data[0]['dir_birth'])
        else:
            self.textEdit_dir_birth.setText("출생 정보 없음")

        if (dir_data[0]['dir_awards'] != None):
            self.textEdit_dir_awards.setText(dir_data[0]['dir_awards'])
        else:
            self.textEdit_dir_awards.setText("수상내역 정보 없음")

        if (dir_data[0]['dir_profile'] != None):
            self.textEdit_dir_profile.setText(dir_data[0]['dir_profile'])
        else:
            self.textEdit_dir_profile.setText("프로필 정보 없음")

        dir_movieid_list = db.getMovieListWithDirId(id)
        print(dir_movieid_list)

        def screenChangeToMovieInfo(id):
            window_movieinfo = WindowClassMovieInfo(id)
            window_movieinfo.exec_()

        for i in range(0, dir_movieid_list.__len__()):
            movie = db.getTitleWithId(dir_movieid_list[i]['movie_id'])
            print(movie)
            movie = movie[0]['title']
            self.listWidget_movieList.addItem(movie)
        self.listWidget_movieList.itemClicked.connect(
            lambda: screenChangeToMovieInfo(db.getidWithTitle(self.listWidget_movieList.currentItem().text())))

form_class_imageInfo = uic.loadUiType("image_info.ui")[0]
class WindowClassImageInfo(QDialog,QWidget ,form_class_imageInfo):
    def __init__(self,id):
        super().__init__()
        self.setupUi(self)
        self.show()

        qPixmapvar = QPixmap()
        url_list = db.getImgUrlWithId(id)
        url = url_list[1]['photo_link']
        urlOpen = urllib.request.urlopen(url).read()
        qPixmapvar.loadFromData(urlOpen)
        self.label_img_1.setPixmap(qPixmapvar)

        url_list = db.getImgUrlWithId(id)
        url = url_list[2]['photo_link']
        urlOpen = urllib.request.urlopen(url).read()
        qPixmapvar.loadFromData(urlOpen)
        self.label_img_2.setPixmap(qPixmapvar)

        url_list = db.getImgUrlWithId(id)
        url = url_list[3]['photo_link']
        urlOpen = urllib.request.urlopen(url).read()
        qPixmapvar.loadFromData(urlOpen)
        self.label_img_3.setPixmap(qPixmapvar)

        url_list = db.getImgUrlWithId(id)
        url = url_list[4]['photo_link']
        urlOpen = urllib.request.urlopen(url).read()
        qPixmapvar.loadFromData(urlOpen)
        self.label_img_4.setPixmap(qPixmapvar)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()
