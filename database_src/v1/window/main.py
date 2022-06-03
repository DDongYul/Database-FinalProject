import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic


form_class = uic.loadUiType("mainActivity.ui")[0]
class WindowClass(QMainWindow,form_class ):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


        self.searchButton.clicked.connect(self.groupboxRadFunction)
        self.sortNameButton.clicked.connect(self.sortNameButtonClick)
        self.sortYearButton.clicked.connect(self.sortYearButtonClick)
        self.sortRateButton.clicked.connect(self.sortRateButtonClick)
        self.tempButton.clicked.connect(self.screenChange)

    def screenChange(self):
        self.window_sub = WindowClassSub()
        self.window_sub.exec_()

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
            self.searchTitle(self.lineEdit.text())
        elif self.radioButtonActor.isChecked() :
            self.searchActor(self.lineEdit.text())
        elif self.radioButtonDirector.isChecked() :
            self.searchDirector(self.lineEdit.text())
        elif self.radioButtonGenre.isChecked() :
            self.searchGenre(self.lineEdit.text())
        elif self.radioButtonYear.isChecked():
            self.searchYear(self.lineEdit.text())
        elif self.radioButtonCountry.isChecked():
            self.searchCountry(self.lineEdit.text())

    # 검색 조건에 따른 검색 함수
    def searchTitle(self, string):
        print("입력한 제목 검색어 = {}".format(string))

    def searchActor(self, string):
        print("입력한 배우 검색어 = {}".format(string))

    def searchDirector(self, string):
        print("입력한 감독 검색어 = {}".format(string))

    def searchGenre(self, string):
        print("입력한 장르 검색어 = {}".format(string))

    def searchYear(self, string):
        print("입력한 년도 검색어 = {}".format(string))

    def searchCountry(self, string):
        print("입력한 국적 검색어 = {}".format(string))

###영화 상세정보 화면 (두번째 화면)
form_class_sub = uic.loadUiType("subActivity.ui")[0]
class WindowClassSub(QDialog,QWidget , form_class_sub):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = WindowClass()
    mainWindow.show()
    app.exec_()