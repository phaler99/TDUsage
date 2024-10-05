from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QSystemTrayIcon, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent

class color:
    background = "#E1F7F5"
    accent = "#9AC8CD"
    primary = "#0E46A3"
    secondary = "#1E0342"

class App(QMainWindow):
    #core of app
    def __init__(self):
        super().__init__()
        self.MainWindow()

    def MainWindow(self):
        #window settings
        self.setWindowTitle("Tusage")
        self.setWindowIcon(QIcon('icon.png'))
        self.setMinimumSize(500, 350)
        self.setStyleSheet(f"background-color: {color.background};")

        #app in tray
        self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), self)
        self.tray_icon.activated.connect(self.on_tray_icon_clicked)
        self.tray_icon.setToolTip('Tusage')

        #context menu of app in tray
        self.tray_menu = QMenu(self)
        quit_action = QAction('Quit', self)
        quit_action.triggered.connect(self.on_quit_action)
        self.tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(self.tray_menu)

    #when minimized
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.window_state = self.saveState()
                self.hide()
                self.tray_icon.show()
        super().changeEvent(event)

    def on_tray_icon_clicked(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isHidden():
                self.showNormal()
                self.restoreState(self.window_state)
                self.activateWindow()

    def closeEvent(self, event):
        QApplication.quit()
    def on_quit_action(self):
        QApplication.quit()

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec_())