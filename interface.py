from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
from videoplayer import VideoPlayer
import CONSTANTS
import os
import time


def hhmmss(time_in_seconds):
    s = time_in_seconds % 60
    m = (time_in_seconds / 60) % 60
    h = (time_in_seconds / (60 * 60)) % 24
    return ("%d:%02d:%02d" % (h, m, s)) if h is 0 else ("%d:%02d" % (m, s))


class UI_MainWindow(object):
    """THUMBNAIL_WIDTH = 200
    THUMBNAIL_SPACING = 10"""
    # Dictionary to store variable variables for UI widgets
    sections_dic = {}

    def __init__(self, aNotifier):
        # Count the number of categories (folders in ../icons)
        folders = self.readDirectory("icons")
        self.number_of_categories = len(folders)-2
        self.notifier = aNotifier
        self.notifier.subscribe('scroll_section', self.clickButtonScroll)
        self.notifier.subscribe('scroll_vertically', self.scrollVertically)

    def setupUi(self, aMainWindow):
        self.mainWindow = aMainWindow
        self.mainWindow.setObjectName("Webflux")
        self.mainWindow.setWindowTitle("Webflux")
        self.mainWindow.setFixedSize(1280, 720)
        self.mainWindow.setStyleSheet("background-color: rgb(110,110,110)")
        self.centralWidget = QtWidgets.QWidget(self.mainWindow)
        self.centralWidget.setObjectName("centralwidget")

        self.main_scroll_area = QtWidgets.QScrollArea(self.centralWidget)
        self.main_scroll_area.setGeometry(QtCore.QRect(10, 60, 1260, 640))
        self.main_scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.main_scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.main_scroll_area.setObjectName("main_scroll_area")
        self.main_scroll_areaContents = QtWidgets.QWidget()
        self.main_scroll_areaContents.setGeometry(QtCore.QRect(0, 0, 1260, self.number_of_categories * 320))
        self.main_scroll_areaContents.setObjectName("main_scroll_areaContents")
        #self.main_scroll_areaContents.setStyleSheet("background-color: rgba(90, 50, 50, 100)")
        self.vBox = QtWidgets.QVBoxLayout(self.main_scroll_areaContents)
        self.vBox.setContentsMargins(0, 0, 0, 0)
        self.vBox.setAlignment(QtCore.Qt.AlignTop)
        self.vBox.setObjectName("vbox")

        """self.createMovieSection("action_movies")
        self.createMovieSection("horror_movies")
        self.createMovieSection("animation_movies")
        self.createMovieSection("fantasy_movies")
        self.createMovieSection("romance_movies")"""
        self.createAllMovieSections()

        self.main_scroll_area.setWidget(self.main_scroll_areaContents)
        self.mainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(self.mainWindow)
        QtCore.QMetaObject.connectSlotsByName(self.mainWindow)

        self.timeStart = time.time()


    def count_time(self):
        print("\tTIME TOOK: ", hhmmss(time.time()-self.timeStart))


    def createAllMovieSections(self):
        # Returns list with folders names (action_movies, horror_movies, etc)
        folders = self.readDirectory("icons")

        for i in range(len(folders)):
            if folders[i] == "temp" or folders[i] == "overlays":
                continue
            self.createMovieSection(folders[i])


    def createMovieSection(self, aFolderName):
        # Create prefix to add to created variables objectName's
        # e.g. if aSectionName is "Action Movies" then prefix is "section_actionmovies_"
        prefix = "section_" + aFolderName + "_"

        split = aFolderName.split('_')
        section_name_formatted = ""
        for i in range(len(split)):
            section_name_formatted += split[i]
            section_name_formatted += " "
        section_name_formatted = section_name_formatted.strip()

        # Label "MOVIE GENRE" (aSectionName) for this section
        label = QtWidgets.QLabel(self.main_scroll_areaContents)
        #label = QtWidgets.QPushButton(self.main_scroll_areaContents)
        label.setGeometry(QtCore.QRect(10, 10, 160, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)

        # the next 3
        label.setLineWidth(2)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setFrameShape(QtWidgets.QFrame.Box)

        label.setText(" " + section_name_formatted.upper() + " ")
        label.setObjectName(prefix + "label")
        label.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        #label.clicked.connect(partial(self.count_time))

        self.sections_dic[label.objectName()] = label
        self.vBox.addWidget(label)

        # Movie scroll section
        amount = 20
        amWidth = amount * (CONSTANTS.THUMBNAIL_WIDTH + CONSTANTS.THUMBNAIL_SPACING)
        scroll_area = QtWidgets.QScrollArea(self.main_scroll_areaContents)
        scroll_area.setGeometry(QtCore.QRect(10, 60, 1240, 280))
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll_area.setObjectName(prefix + "scroll_area")
        # scroll_area.setStyleSheet("background-color: rgba(60, 150, 60, 100)")
        scroll_area.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        scroll_area_contents = QtWidgets.QWidget()
        scroll_area_contents.setGeometry(QtCore.QRect(0, 0, amWidth, 280))
        scroll_area_contents.setObjectName(prefix + "scroll_area_contents")
        hBox = QtWidgets.QHBoxLayout(scroll_area_contents)
        hBox.setContentsMargins(0, 0, 0, 0)
        hBox.setObjectName(prefix + "hBox")
        self.sections_dic[scroll_area.objectName()] = scroll_area
        self.sections_dic[scroll_area_contents.objectName()] = scroll_area_contents
        self.sections_dic[hBox.objectName()] = hBox

        # Each movie 200x280
        self.createMoviesThumbnails(amount, CONSTANTS.THUMBNAIL_WIDTH, scroll_area_contents, hBox, prefix, aFolderName)

        # Scroll right button for this section
        btn_right = QtWidgets.QPushButton(scroll_area)
        btn_right.setGeometry(1230, 0, 30, 282)
        btn_right.setObjectName(prefix + "btn_scroll_right")
        btn_right.setText(">>>")
        btn_right.setFont(font)
        btn_right.setStyleSheet("background-color: rgba(255, 255, 255, 130)")
        btn_right.clicked.connect(partial(self.scrollMovies, scroll_area, btn_right, amWidth))
        self.sections_dic[btn_right.objectName()] = btn_right

        # Scroll left button for this section
        btn_left = QtWidgets.QPushButton(scroll_area)
        btn_left.setGeometry(0, 0, 30, 282)
        btn_left.setObjectName(prefix + "btn_scroll_left")
        btn_left.setText("<<<")
        btn_left.setFont(font)
        btn_left.setStyleSheet("background-color: rgba(255, 255, 255, 130)")
        btn_left.clicked.connect(partial(self.scrollMovies, scroll_area, btn_left))
        btn_left.setVisible(False)
        self.sections_dic[btn_left.objectName()] = btn_left

        scroll_area.setWidget(scroll_area_contents)
        self.vBox.addWidget(scroll_area)


    def readDirectory(self, aPath):
        """
        Read files/folders in folder and return list with files/folders names
        :param aPath: folder path relative to env
        :return: list with filenames and extensions
        """
        return os.listdir(aPath)


    def createMoviesThumbnails(self, aRange, aWidth, aParent, aHBox, aPrefix, aFolderName):
        # Folder path for section aSectionName
        path = "icons/" + aFolderName

        # Get the movies in aGenre folder
        thumbnails = self.readDirectory(path)

        for i in range(aRange):
            btn = QtWidgets.QPushButton(aParent)
            name = aPrefix + "btn_" + thumbnails[i]
            btn.setText("")
            btn.setObjectName(name)
            btn.setFixedSize(aWidth, 280)
            btn.setStyleSheet("border-image: url(" + path + "/" + thumbnails[i] + ");"
                              "background-color: rgba(0, 0, 0, 0)")
            aHBox.addWidget(btn)
            btn.clicked.connect(partial(self.clickMovie, btn.objectName()))
            self.sections_dic[btn.objectName()] = btn


    def clickMovie(self, aButtonName):
        print(aButtonName.upper() + " PRESSED")
        name = aButtonName.split("_btn_")[1].split('.')[0].replace('_', ' ')
        try:
            self.player = VideoPlayer(name + " trailer", self.notifier)
        except Exception as e:
            print(e)


    def scrollMovies(self, aScrollArea, aBtn, aWidth):
        btnName = aBtn.objectName()
        print(btnName)
        if "right" in btnName:
            # Scroll movie list to the right for the length of the QScrollArea widget
            aScrollArea.horizontalScrollBar().setValue(aScrollArea.horizontalScrollBar().value() + 1240)

            if aScrollArea.horizontalScrollBar().value() + 1240+20 >= aWidth:
                aBtn.setVisible(False)

            otherBtnName = btnName.replace("right", "left")
            otherBtn = aScrollArea.findChild(QtWidgets.QPushButton, otherBtnName)
            otherBtn.setVisible(True)
        elif "left" in btnName:
            # Scroll movie list to the left for the length of the QScrollArea widget
            aScrollArea.horizontalScrollBar().setValue(aScrollArea.horizontalScrollBar().value() - 1250)

            if aScrollArea.horizontalScrollBar().value() is 0:
                aBtn.setVisible(False)

            otherBtnName = btnName.replace("left", "right")
            otherBtn = aScrollArea.findChild(QtWidgets.QPushButton, otherBtnName)
            otherBtn.setVisible(True)


    def scrollVertically(self, down=True):
        """
        Scrolls the main window up and down.
        :param down: bool - scroll downwards
        """
        if down:
            self.main_scroll_area.verticalScrollBar().setValue(self.main_scroll_area.verticalScrollBar().value() + 640)
        else:
            self.main_scroll_area.verticalScrollBar().setValue(self.main_scroll_area.verticalScrollBar().value() - 640)


    def getWidgetAtCursor(self):
        try:
            pos = QtGui.QCursor.pos()
            window_pos = self.mainWindow.pos()
            """print("\tpos\nx: " + str(pos.x()) + "\ty: " + str(pos.y()))
            print("\twindow\nx: " + str(window_pos.x()) + "\ty: " + str(window_pos.y()))"""

            # For some reason mainwindow.childAt() is checking as if mainwindow starts on (0, 0)
            # edit: the above is true on runtime, if in debug mode then it will return
            #       a relative cursor position instead :)
            real_pos = QtCore.QPoint(pos.x()-window_pos.x(), pos.y()-window_pos.y())

            widget_at = self.mainWindow.childAt(real_pos)

            return widget_at.objectName()
        except Exception as error:
            print(error)


    def clickButtonScroll(self, aBtnName, aForward=True):
        aux = aBtnName.split('_')
        prefix = aux[0] + "_" + aux[1] + "_"
        if aForward:
            self.sections_dic[prefix + "btn_scroll_right"].click()
        else:
            self.sections_dic[prefix + "btn_scroll_left"].click()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


"""if __name__ == "__main__":
    import sys
    qApp = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UI_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(qApp.exec_())"""
