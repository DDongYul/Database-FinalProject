import sys
import searcher
import database as db
from PyQt5.QtWidgets import *
from PyQt5 import uic
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
        self.tempButton.clicked.connect(self.screenChangeToMovieInfo)

    def screenChangeToMovieInfo(self,id):
        self.window_movieinfo = WindowClassMovieInfo(id)
        self.window_movieinfo.exec_()

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
            searcher.search(2, self.lineEdit.text())
        elif self.radioButtonDirector.isChecked() :
            searcher.search(3, self.lineEdit.text())
        elif self.radioButtonGenre.isChecked() :
            searcher.search(4, self.lineEdit.text())
        elif self.radioButtonYear.isChecked():
            searcher.search(5, self.lineEdit.text())
        elif self.radioButtonCountry.isChecked():
            searcher.search(6, self.lineEdit.text())

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
########################배우 데이터 처리#############################################################

        director_id = db.getDirectorIdWithId(id)
        director_name = db.getDirectorNameWithDirId(director_id['dir_id'])
        self.listWidget_director.addItem(director_name['dir_name'])
        def screenChangeToDirectorInfo(id):
            window_directorinfo = WindowClassDirectorInfo(id)
            window_directorinfo.exec_()
        self.listWidget_director.itemClicked.connect(lambda:screenChangeToDirectorInfo(db.getDirIdwithDirName(self.listWidget_director.currentItem().text())['dir_id']))




        self.textEdit_title.setText(data[0]['title'])
        self.textEdit_audienceRate.setText(str(data[0]['netizen_score']))
        self.textEdit_journalRate.setText(str(data[0]['journal_score']))
        self.textEdit_playTime.setText("상영시간: " + str(data[0]['playtime'])+"분")
        self.textEdit_openingDate.setText("개봉: " + str(data[0]['open_date']))
        self.textEdit_rate.setText(str(data[0]['movie_rate']))

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
            self.textEdit_dir_birth.setText("출생: " + dir_data[0]['dir_birth'])
        else:
            self.textEdit_dir_birth.setText("출생 정보 없음")

        if (dir_data[0]['dir_awards'] != None):
            self.textEdit_dir_awards.setText("수상내역: " + dir_data[0]['dir_awards'])
        else:
            self.textEdit_dir_awards.setText("수상내역 정보 없음")

        if (dir_data[0]['dir_profile'] != None):
            self.textEdit_dir_profile.setText(dir_data[0]['dir_profile'])
        else:
            self.textEdit_dir_profile.setText("프로필 정보 없음")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()