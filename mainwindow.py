from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow ,QLabel, QGridLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QPixmap, QImage
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QRect
import PyQt5.QtCore as QtCore

import sys

class MainWindow(QMainWindow):
    
    #upper menu icons
    top_icons = []
    #lower menu icons
    bottom_icons = []
    
    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        uic.loadUi('mainwindow.ui',self)
        print("initialized ui")
        
        self.setupMenuBar()
        self.top_icons[0].clicked.connect(lambda: self.toggleMenu(250, True))
        self.show()
        #self.label_3.setWidth(0)

        ## PAGES
        ########################################################################

        # PAGE 1
        #self.ui.btn_page_1.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.ui.page_1))
        #self.home_button.setStyleSheet('text-align: left;')
       
        
        
        
    def setupMenuBar(self):
        self.top_icons.append(self.addTopMenuIcon("", "resources/menu_icon.png", "\n	color: rgb(255, 255, 255);\n	background-color: rgb(35, 35, 35);\n	border: 0px solid;\n}\nQPushButton:hover {\n	background-color: rgb(85, 170, 255);\n"))
        #self.top_icons[0].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.top_menu_grid.addWidget(self.top_icons[0])
        self.top_menu_grid.addWidget(self.top_icons[0])
        
        vspace = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.top_menu_grid.addItem(vspace)
        self.top_icons.append(self.addTopMenuIcon("Home", "resources/home_icon.png", "\n	color: rgb(255, 255, 255);\n	background-color: rgb(35, 35, 35);\n	border: 0px solid;\n}\nQPushButton:hover {\n	background-color: rgb(85, 170, 255);\n"))
    
        for icon in self.top_icons[1:]:
            icon.hideText()
            self.top_menu_grid.addWidget(icon)
            
        self.bottom_icons.append(self.addTopMenuIcon("Settings", "resources/settings_icon.png", "\n	color: rgb(255, 255, 255);\n	background-color: rgb(35, 35, 35);\n	border: 0px solid;\n}\nQPushButton:hover {\n	background-color: rgb(85, 170, 255);\n"))
        
        for icon in self.bottom_icons:
            icon.hideText()
            self.lower_menu_grid.addWidget(icon)
        
    def addTopMenuIcon(self,name,icon_path, style_sheet = ""):
        pb = MyButton(name)
        pixmap = QPixmap(icon_path).scaled(40, 33, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        pb.setPixmap(pixmap)
        if style_sheet:
            pb.setStyleSheet(style_sheet)
        
        return pb
        


        
    def toggleMenu(self, maxWidth, enable):
        if enable:
            
            # GET WIDTH
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 50

            # SET MAX WIDTH
            if width == standard:
                widthExtended = maxExtend
            else:
                widthExtended = standard
                for icon in self.top_icons:
                    icon.hideText()
                for icon in self.bottom_icons:
                    icon.hideText()

            # ANIMATION
            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()
            if widthExtended != standard:
      
                #for icon in self.top_icons:
                for i in range(len(self.top_icons)):
                    self.animation.finished.connect(lambda: self.top_icons[i].showText())
                    #self.top_icons[i].showText()
                for icon in self.bottom_icons:
                    self.animation.finished.connect(lambda: icon.showText())
                    
                    
        else:
            print("Disabling")
            
            
            

class MyButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super(MyButton, self).__init__(*args, **kwargs)
        self.original_text = self.text()

    def setPixmap(self, pixmap):
        self.pixmap = pixmap

    def hideText(self):

        self.setText("")
    def showText(self):
        print('in show text, original is ' + str(self.original_text))
        self.setText(self.original_text)
    
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