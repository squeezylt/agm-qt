from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow ,QLabel, QGridLayout, QPushButton
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QImage
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
import PyQt5.QtCore as QtCore

import sys

class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        uic.loadUi('mainwindow.ui',self)
        print("initialized ui")
        self.show()
        
        self.btn_Toggle.clicked.connect(lambda: self.toggleMenu(250, True))
        
        #self.label_3.setWidth(0)

        ## PAGES
        ########################################################################

        # PAGE 1
        #self.ui.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ui.page_1))
        #self.home_button.setStyleSheet('text-align: left;')
        '''
        pb = QPushButton()
        name = "SP_MessageBoxCritical"
        #icon = self.style().standardIcon(getattr(QStyle, name))
        icon = QIcon('resources/home_icon.png')
        # icon = self.style().standardIcon(QtWidgets.QStyle.SP_MessageBoxCritical)
        pb.setIcon(icon)

        pb.setStyleSheet('text-align: left;')
        pb.setLayout(QGridLayout())
        
        label = QLabel('')
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        label.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, 1)
        pb_layout = pb.layout()
        pb_layout.addWidget(label)

        self.gridLayout_4.addWidget(pb)
        '''
        

        pb = MyButton('test')
        
        path = "resources/home_icon.png"
        pixmap = QPixmap(path).scaled(40, 40, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        
        if not pixmap:
            print ('failed pixmap')
        print(pixmap.height())
        #pixmap.show()
     
        pb.setPixmap(pixmap)
        
        self.gridLayout_4.addWidget(pb)


        
    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            # SET MAX WIDTH
            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(MyButton, self).__init__(*args, **kwargs)

    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def sizeHint(self):
        parent_size = QPushButton.sizeHint(self)
        return QtCore.QSize(parent_size.width() + self.pixmap.width(), max(parent_size.height(), self.pixmap.height()))

    def paintEvent(self, event):
        QPushButton.paintEvent(self, event)

        pos_x = 5  # hardcoded horizontal margin
        pos_y = (self.height() - self.pixmap.height()) / 2

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)
        painter.drawPixmap(int(pos_x), int(pos_y), self.pixmap)