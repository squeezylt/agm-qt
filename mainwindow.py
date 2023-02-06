
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QTreeWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import QSettings, pyqtSignal, QDir
import maincontrol


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os.path
import sys

#made by squeezyxl


class MainWindow(QMainWindow):

    mod_path_set = pyqtSignal(str)   
    settings_updated = pyqtSignal()
    mod_updated = pyqtSignal()
    settings = QSettings("mod.ini", QSettings.IniFormat)
    mc = maincontrol.MainControl()
    mod_path = ""

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        uic.loadUi('main.ui',self)
        
        self.mod_path_set.connect(self.changeModPath) 
        self.settings_updated.connect(self.saveSettings)
        self.add_selected_button.clicked.connect(self.handleAddSelected)
        self.clear_button.clicked.connect(self.handleClearButton)
        self.remove_selected_button.clicked.connect(self.handleRemoveSelected)

        self.xtree = XTreeWidget(QTreeWidget)
        self.mainlayout.addWidget(self.xtree)
        self.xtree.itemChecked.connect(self.handleModToggled)
        self.xtree.itemClicked.connect(self.handleModSelected)

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
        
    def handleModSelected(self, item, column):
        path = item.data(column, QtCore.Qt.UserRole + 1)
        name = item.text(column)
        print("selected" + name)
        self.mc.setSelectedMod(path,name)
        
    #toolside stuff
    
    #behavior when we add a mod to the working list
    def handleAddSelected(self):
        print(0)
        active_mod = self.mc.getSelectedMod()
        if not str(active_mod[0]):
            return
        print("Active mod is" + str(active_mod[1]))
        item = QListWidgetItem(active_mod[1])
        item.setData(QtCore.Qt.UserRole, active_mod[0])
        
        #add only if the list doesnt have this mod name already
        for i in range (self.active_list.count()):
            print("looping")
            if self.active_list.item(i).data(QtCore.Qt.UserRole) == active_mod[0]:
                return 
        
        self.active_list.addItem(item)
        
    def handleClearButton(self):
        self.active_list.clear()
        
    def handleRemoveSelected(self):
        current = self.active_list.currentItem()
        row = self.active_list.row(current)
        if current:   
            self.active_list.takeItem(row)
        
        
                
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
