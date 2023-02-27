
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow

import sys

def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("AGM Manager Beta")
    app.exec_()

if __name__ == "__main__":
    main()