from notifier import Notifier

from PyQt5.QtWidgets import QApplication, QMainWindow
import interface
import camera

if __name__ == "__main__":
    import sys
    notifier = Notifier()

    qApp = QApplication(sys.argv)
    MainWindow = QMainWindow()

    ui = interface.UI_MainWindow(notifier)
    ui.setupUi(MainWindow)

    MainWindow.show()

    camera.main(ui, notifier)
    sys.exit(qApp.exec_())
