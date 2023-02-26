# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_mainrvpJdh.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PyQt5.QtWidgets import *

from PyQt5 import uic

import sys

class Ui_MainWindow(QMainWindow):
    
    def __init__(self, parent=None):

        super(Ui_MainWindow, self).__init__(parent)
        uic.loadUi('ui_main.ui',self)
        print("initialized ui")
        self.show()

def main():

    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.setWindowTitle("AGM Manager Beta")
    app.exec_()

if __name__ == "__main__":
    main()