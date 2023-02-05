
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QTreeWidget
from PyQt5.QtCore import QSettings, pyqtSignal, QDir
import maincontrol


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os.path
import sys

#made by squeezyxl


class MainWindow(QMainWindow):

    mod_path_set = pyqtSignal(str)   
    settings_updated = pyqtSignal()
    settings = QSettings("mod.ini", QSettings.IniFormat)
    mc = maincontrol.MainControl()
    mod_path = str

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        uic.loadUi('main.ui',self)
        
        self.mod_path_set.connect(self.changeModPath) 
        self.settings_updated.connect(self.saveSettings)

        self.xtree = XTreeWidget(QTreeWidget)
        self.mainlayout.addWidget(self.xtree)
        self.xtree.itemChecked.connect(self.handleModToggled)

        self.loadSettings()
        
        self.actionLoad_Mod_Dir.triggered.connect(self.loadModDir)
        self.show()

    def saveSettings(self):
        self.settings.beginGroup("Path")
        self.settings.setValue("mod_path",self.mod_path)
        self.settings.endGroup()
    
    def loadSettings(self):
                                                                                                                                                                          
        mod_path = self.settings.value('Path/mod_path', type=str)
        if mod_path:
            print('mod path set in load settings')
            self.mod_path_set.emit(mod_path)
        else: print("mod path is ...." + mod_path)

    def changeModPath(self,str):
        self.mod_path = str
        self.mc.setModDir(str)
        self.updateModTreeWidget()

        #on purpose, force settings saving on mod path update
        self.settings_updated.emit()
        
    def loadModDir(self):
        fname = QFileDialog.getExistingDirectory(
            self, 'Select Mod Directory')
        dir = QDir(fname)
        if dir.exists():
            self.mod_path_set.emit(fname)

    def updateModTreeWidget(self):
        mod_list = self.mc.getModDataStructure()
        #rowcount = self.mod_tree.topLevelItemCount()
        for item in mod_list:

            tree_item = TreeWidgetItem()
            tree_item.setFlags(tree_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
            mod_name = os.path.basename(item)
            #save absolute path in item itself because why not. won't clutter much
            tree_item.setData(0,QtCore.Qt.UserRole + 1,item)

            if mod_list[item] == False:
                tree_item.setCheckState(0,QtCore.Qt.Unchecked)
                item_stripped = mod_name.replace("DISABLED","")
                tree_item.setText(0,item_stripped)
            else:
                tree_item.setCheckState(0,QtCore.Qt.Checked)
                tree_item.setText(0,os.path.basename(mod_name))
            
            self.xtree.addTopLevelItem(tree_item)

            
    def handleModToggled(self, item, column):
        print("Mod Toggled")
        selected = bool(item.checkState(column))
        path = item.data(column, QtCore.Qt.UserRole + 1)
        print(str(selected) + " " + path)
        new_path = self.mc.toggleMod(path, selected)
        #manually set item data
        #should also probably make this role a const definition
        item.setData(0, QtCore.Qt.UserRole + 1, new_path)
        
                
class TreeWidgetItem(QTreeWidgetItem):

    def setData(self, column, role, value):
        state = self.checkState(column)
        QTreeWidgetItem.setData(self, column, role, value)
        if (role == QtCore.Qt.CheckStateRole and
            state != self.checkState(column)):
            treewidget = self.treeWidget()
            if treewidget is not None:
                treewidget.itemChecked.emit(self, column)
class XTreeWidget(QTreeWidget):
    #this was bullshit i had to do this
    itemChecked = pyqtSignal(object, int)

    def __init__(self,parent):
        QTreeWidget.__init__(self)               

        

def main():

    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("AGM Manager")
    app.exec_()

if __name__ == "__main__":
    main()
