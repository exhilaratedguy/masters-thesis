import sys

from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtGui import QPalette, QPixmap
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout, QPushButton, QStyle, \
    QVBoxLayout, QLabel, QSlider, QApplication

from downloader import Downloader
import CONSTANTS


def hhmmss(ms):
    s = (ms / 1000) % 60
    m = (ms / (1000 * 60)) % 60
    h = (ms / (1000 * 60 * 60)) % 24
    return ("%d:%02d:%02d" % (h, m, s)) if h else ("%d:%02d" % (m, s))

class VideoPlayer(QWidget):
    def __init__(self, aQuery, aNotifier):
        super().__init__()

        self.notifier = aNotifier
        self.notifier.subscribe('videoplayer_close', self.close)
        self.notifier.subscribe('videoplayer_volume_up', self.volume_increase_5)
        self.notifier.subscribe('videoplayer_volume_down', self.volume_decrease_5)
        self.notifier.subscribe('videoplayer_play_or_pause', self.play_or_pause)

        self.setWindowTitle("Webflux Media Player")
        self.setGeometry(320, 180, CONSTANTS.VIDEO_WIDTH, CONSTANTS.VIDEO_HEIGHT - CONSTANTS.HEIGHT_OFFSET)
        self.setContentsMargins(0,0,0,0)

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.downloader = Downloader(aQuery)

        self.setup_ui()
        self.show()
        #self.showMaximized()

        self.notifier.notify('set_videoplayer_window', self)


    def setup_ui(self):
        prefix = "videoplayer_"

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.setObjectName(prefix + "mediaPlayer")

        videoWidget = QVideoWidget()
        videoWidget.setObjectName(prefix + "videoWidget")

        self.downloader.download()
        filename = self.downloader.getFile()
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

        # Play button
        self.playBtn = QPushButton(self)
        self.playBtn.setObjectName(prefix + "playBtn")
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.playVideo)

        # Pause button
        self.pauseBtn = QPushButton(self)
        self.pauseBtn.setObjectName(prefix + "pauseBtn")
        self.pauseBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.pauseBtn.clicked.connect(self.pauseVideo)

        # Stop button
        self.stopBtn = QPushButton(self)
        self.stopBtn.setObjectName(prefix + "stopBtn")
        self.stopBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stopBtn.clicked.connect(self.stopVideo)

        # Video position slider
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setObjectName(prefix + "slider")
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position_slider)

        # Current time label
        self.labelTime = QLabel(self)
        self.labelTime.setObjectName(prefix + "labelTime")
        self.labelTime.setText("0:00")
        self.labelTime.setStyleSheet("color: rgb(255, 255, 255)")
        self.labelTime.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Duration time label
        self.labelDuration = QLabel(self)
        self.labelDuration.setObjectName(prefix + "labelDuration")
        self.labelDuration.setText("0:00")
        self.labelDuration.setStyleSheet("color: rgb(255, 255, 255)")
        self.labelDuration.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Volume icon
        self.volumeBtn = QPushButton(self)
        self.volumeBtn.setObjectName(prefix + "volumeBtn")
        self.volumeBtn.setStyleSheet("background-color: rgba(255, 255, 255, 0)")
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.clicked.connect(self.muteVideo)


        # Volume slider
        self.volumeSlider = QSlider(Qt.Horizontal, self)
        self.volumeSlider.setObjectName(prefix + "volumeSlider")
        self.volumeSlider.setRange(0, 100)
        self.volumeSlider.setFixedWidth(100)
        self.volumeSlider.setValue(50)
        self.mediaPlayer.setVolume(50)
        self.volumeSlider.sliderMoved.connect(self.set_volume_slider)


        # Label for error msg
        self.labelError = QLabel()
        self.labelError.setObjectName(prefix + "labelError")
        self.labelError.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.labelError.setStyleSheet("color: rgb(255, 255, 255)")

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)

        #hbox.addWidget(openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.pauseBtn)
        hbox.addWidget(self.stopBtn)
        hbox.addWidget(self.labelTime)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.labelDuration)
        hbox.addWidget(self.volumeBtn)
        hbox.addWidget(self.volumeSlider)

        #Adding widgets to the Vertical Box Layout
        vbox = QVBoxLayout()
        vbox.addWidget(videoWidget)
        vbox.addLayout(hbox)
        vbox.addWidget(self.labelError)

        self.setLayout(vbox)

        self.mediaPlayer.setVideoOutput(videoWidget)

        # Start the video
        self.mediaPlayer.play()

        # media player signals
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.volumeChanged.connect(self.volume_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

        # Create icon overlays
        self.labelPlay = self.buildLabel(CONSTANTS.ICONS.Play)
        self.labelPause = self.buildLabel(CONSTANTS.ICONS.Pause)
        self.labelVolumeUp = self.buildLabel(CONSTANTS.ICONS.VolumeUp)
        self.labelVolumeDown = self.buildLabel(CONSTANTS.ICONS.VolumeDown)


    #region --- FUNCTIONS FOR INTERFACE BUTTONS ---
    def playVideo(self):
        self.mediaPlayer.play()
        self.showAndHideOverlay(self.labelPlay)

    def pauseVideo(self):
        self.mediaPlayer.pause()
        self.showAndHideOverlay(self.labelPause)

    def stopVideo(self):
        self.mediaPlayer.stop()

    def muteVideo(self):
        self.mediaPlayer.setMuted(True)
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        self.volumeBtn.clicked.connect(self.unmuteVideo)

    def unmuteVideo(self):
        self.mediaPlayer.setMuted(False)
        self.volumeBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaVolume))
        self.volumeBtn.clicked.connect(self.muteVideo)

    def position_changed(self, position):
        self.slider.setValue(position)
        self.labelTime.setText(hhmmss(position))

    def volume_changed(self, volume):
        self.volumeSlider.setValue(volume)
        if self.mediaPlayer.volume() == 0:
            self.muteVideo()
        else:
            self.unmuteVideo()

    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        self.labelDuration.setText(hhmmss(duration))

    def set_position_slider(self, position):
        self.mediaPlayer.setPosition(position)

    def set_volume_slider(self, volume):
        self.mediaPlayer.setVolume(volume)

    def handle_error(self):
        self.playBtn.setEnabled(False)
        self.labelError.setText("Error: " + self.mediaPlayer.errorString())
    #endregion

    #region --- FUNCTIONS FOR NOTIFIER EVENTS ---
    def volume_increase_5(self):
        vol = self.mediaPlayer.volume()
        vol += 10
        if vol > 100: vol = 100
        self.set_volume_slider(vol)
        self.showAndHideOverlay(self.labelVolumeUp)

    def volume_decrease_5(self):
        vol = self.mediaPlayer.volume()
        vol -= 10
        if vol < 0: vol = 0
        self.set_volume_slider(vol)
        self.showAndHideOverlay(self.labelVolumeDown)

    def play_or_pause(self):
        if self.mediaPlayer.state() == self.mediaPlayer.PlayingState:
            self.pauseVideo()
        else:
            self.playVideo()
    #endregion

    def getWidgetAtCursor(self):
        from PyQt5 import QtCore, QtGui
        try:
            pos = QtGui.QCursor.pos()
            window_pos = self.pos()
            """print("\tpos\nx: " + str(pos.x()) + "\ty: " + str(pos.y()))
            print("\twindow\nx: " + str(window_pos.x()) + "\ty: " + str(window_pos.y()))"""

            # For some reason mainwindow.childAt() is checking as if mainwindow starts on (0, 0)
            # edit: the above is true on runtime, if in debug mode then it will return
            #       a relative cursor position instead :)
            real_pos = QtCore.QPoint(pos.x() - window_pos.x(), pos.y() - window_pos.y())

            widget_at = self.childAt(real_pos)

            return widget_at.objectName()
        except Exception as error:
            print(error)

    def showAndHideOverlay(self, label: QLabel):
        label.show()
        QTimer.singleShot(700, lambda: label.hide())

    def buildLabel(self, icon):
        """
        Builds the label for the overlay with the icon of the action triggered.
        :param icon: int -> 1- play; 2- pause; 3- vol_up; 4- vol_down
        :return: label: QLabel
        """
        if icon is CONSTANTS.ICONS.Play:
            pixmap = QPixmap("./icons/overlays/play.png")
        elif icon is CONSTANTS.ICONS.Pause:
            pixmap = QPixmap("./icons/overlays/pause.png")
        elif icon is CONSTANTS.ICONS.VolumeUp:
            pixmap = QPixmap("./icons/overlays/vol_up.png")
        elif icon is CONSTANTS.ICONS.VolumeDown:
            pixmap = QPixmap("./icons/overlays/vol_down.png")
        else:
            return None

        pix = pixmap.scaledToHeight(100)

        label = QLabel(self)

        label.setAutoFillBackground(False)
        label.setFixedSize(pix.width(), pix.height())
        label.setMask(pix.createMaskFromColor(Qt.transparent))
        label.setPixmap(pix)

        posX = CONSTANTS.VIDEO_WIDTH / 2 - label.width() / 2 + 10
        posY = CONSTANTS.VIDEO_HEIGHT / 2 - label.height() / 2 + 10 - CONSTANTS.HEIGHT_OFFSET
        label.move(posX, posY)
        label.hide()

        return label

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            if self.isMaximized():
                self.showNormal()
            else:
                self.showMaximized()

    def closeEvent(self, *args, **kwargs):
        super(VideoPlayer, self).closeEvent(*args, **kwargs)

        # Set an empty media content to the player to free the video file to be deleted by the system
        self.mediaPlayer.setMedia(QMediaContent())
        self.downloader.deleteFile()
        self.notifier.notify('set_videoplayer_window')


"""if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VideoPlayer("spirited away trailer")
    sys.exit(app.exec_())"""