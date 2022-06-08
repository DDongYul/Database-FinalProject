import sys
import searcher
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

    def screenChangeToMovieInfo(self):
        self.window_movieinfo = WindowClassMovieInfo()
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
            searcher.search(1, self.lineEdit.text())
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
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        def actor_click(event):
            self.window_actorinfo = WindowClassActorInfo()
            self.window_actorinfo.exec_()

        # def makeButton():
        #

        # self.textEdit_actor.setText("이동열,이준섭")
        # actor_list = self.textEdit_actor.toPlainText().split(",")
        # for i in range(0,actor_list.__len__()):
        #     # app = QtWidgets.QApplication(sys.argv)
        #     button = QtWidgets.QPushButton()
        #     button.setGeometry(QtCore.QRect(100+i*50,220 , 150+i*50,250))
        #     # self.button.setGeomerty(QtCore.QRect(100+i*50,220 , 150+i*50,250))
        #     # button.setText = actor_list[i]
        #     # self.button.clicked.connet(self.actor_click)
        #     button.show()
        self.textEdit_actor.mousePressEvent = actor_click
        # self.textEdit_director.show()
        # sys.exit(app.exec_())

    def screenChangeToActor(self):
        self.window_actroinfo = WindowClassActorInfo()
        self.window_actroinfo.exec_()


form_class_actorInfo = uic.loadUiType("actor_info.ui")[0]
class WindowClassActorInfo(QDialog,QWidget ,form_class_actorInfo):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()