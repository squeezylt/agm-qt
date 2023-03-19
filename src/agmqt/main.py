
from PyQt5.QtWidgets import QApplication
from view import mainwindow

import sys

def main():

    app = QApplication(sys.argv)
    window = mainwindow.MainWindow()
    window.setWindowTitle("AGM Manager Beta")
    app.exec_()

if __name__ == "__main__":
    main()