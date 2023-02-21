
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QTreeWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import QSettings, pyqtSignal, QDir
import maincontrol


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os.path
import sys
import filecontrol as fc
import mod_data

#made by squeezylt


#usage in qt embedded widget data
DATA_ROLE = QtCore.Qt.UserRole + 1
EXTRA_DATA_ROLE = QtCore.Qt.UserRole + 2 #reserved, unused?


class MainWindow(QMainWindow):

    mod_path_set = pyqtSignal(str)   
    settings_updated = pyqtSignal()
    mod_updated = pyqtSignal()
    cat_updated = pyqtSignal(str)
    
    #should change to not use hardcoded ini file. use system abstracted format
    settings = QSettings("mod.ini", QSettings.IniFormat)
    mc = maincontrol.MainControl()
    mod_path = ""

    def __init__(self, parent=None):

        super(MainWindow, self).__init__(parent)
        uic.loadUi('main.ui',self)
        
        #callbacks
        self.mod_path_set.connect(self.changeModPath) 
        self.settings_updated.connect(self.saveSettings)
        self.mod_updated.connect(self.updateModTreeWidget)
        self.active_list.model().rowsInserted.connect(self.handleActiveListSizeChanged)
        self.active_list.model().rowsRemoved.connect(self.handleActiveListSizeChanged)
        self.add_selected_button.clicked.connect(self.handleAddSelected)
        self.plus_button.clicked.connect(self.handlePlusButton)
        self.minus_button.clicked.connect(self.handleMinusButton)
        self.clear_button.clicked.connect(self.handleClearButton)
        self.remove_selected_button.clicked.connect(self.handleRemoveSelected)
        self.mod_rename_button.clicked.connect(self.handleModRenameApply)

        #custom tree setup
        self.xtree = XTreeWidget(QTreeWidget)
        self.mainlayout.addWidget(self.xtree)
        self.xtree.itemChecked.connect(self.handleModToggled)
        self.xtree.itemClicked.connect(self.handleModSelected)
        self.xtree.setHeaderLabel("Mods")
        
        
        #widget things
        self.mod_rename_button.setEnabled(False)
        self.category_name_button.setEnabled(False)

        #settings
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
        #i want to rewrite this entire function but my brain hurts
        self.xtree.clear()
        mod_list = self.mc.getModDataStructure()
        
        if (not mod_list):
            print("mod list empty")
            return
        
        #all unsorted items can use this
        top_item = TreeWidgetItem()
        top_item.setFlags(top_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
        top_item.setText(0,"Unsorted")
    
        for item in mod_list.items():
            
            #bottom level item
            tree_item = TreeWidgetItem()
            tree_item.setFlags(tree_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
            mod_name = item.name()
            #print('in main loop, mod name is ' + mod_name)
            tree_item.setData(0,DATA_ROLE,item.id())

            if not item.enabled():
                tree_item.setCheckState(0,QtCore.Qt.Unchecked)
            else:
                tree_item.setCheckState(0,QtCore.Qt.Checked)
            
            tree_item.setText(0,mod_name)
            categories = item.getCategories()
            cat_top_item = None

            if len(categories) == 0:
                top_item.addChild(tree_item)
            
            
            else:
                first_cat = categories[0]
                #see if the top level item already exists in the tree
                find_top_cat = self.xtree.findItems(first_cat,QtCore.Qt.MatchFlag.MatchExactly,0)
                if len(find_top_cat) == 0:
                    cat_top_item = TreeWidgetItem()
                    cat_top_item.setFlags(cat_top_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
                    cat_top_item.setText(0,first_cat)
                    parent_item = cat_top_item
                else:
                    cat_top_item = find_top_cat[0]
                    parent_item = cat_top_item
            
            for cct in categories[1:]:

                child_item = None
                for i in range(parent_item.childCount()):
                    if parent_item.child(i).text(0) == cct:
                        child_item = parent_item.child(i)
               
                if not child_item:
                    
                    child_item = TreeWidgetItem()
                    child_item.setFlags(cat_top_item.flags() | QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsSelectable)
                    child_item.setText(0,cct)
                    parent_item.addChild(child_item)
                parent_item = child_item
            #getting sloppy but oh well, slap the actual mod on it now
            if len(categories) != 0:
                parent_item.addChild(tree_item)
                
            self.xtree.addTopLevelItem(top_item)
            if len(categories) != 0:
                self.xtree.addTopLevelItem(cat_top_item)


            
    def handleModToggled(self, item, column):
        print("Mod Toggled")
        selected = bool(item.checkState(column))
        id = item.data(column, DATA_ROLE)
        success = self.mc.toggleMod(id, selected)
        if (not success):
            print("error toggling mod")

        
    def handleModSelected(self, item, column):
        #path
        id = item.data(column, DATA_ROLE)
        self.mc.setSelectedMod(id)
        
    #toolside stuff
    
    #behavior when we add a mod to the working list
    def handleAddSelected(self):
        
        active_mod = self.mc.getSelectedMod()
        if not active_mod:
            return
        if not str(active_mod.modpath):
            return
        
        item = QListWidgetItem(active_mod.name())
        item.setData(DATA_ROLE, active_mod.id())
        
        #add only if the list doesnt have this mod name already
        for i in range (self.active_list.count()):
            if self.active_list.item(i).data(DATA_ROLE) == active_mod.id():
                return 
        
        self.active_list.addItem(item)
        
    def handleClearButton(self):
        self.active_list.clear()
        
    def handleRemoveSelected(self):
        current = self.active_list.currentItem()
        row = self.active_list.row(current)
        if current:   
            self.active_list.takeItem(row)
            
    def handleModRenameApply(self):
        #str. name not path
        new_mod_name = self.rename_edit.text()
        print("New mod name is " + new_mod_name)
        if (not new_mod_name):
            print("mod name null, returing")
            return
        #get top, this only works with 1 mod at a time anyway
        if (self.active_list.count() != 1):
            print("active list not size 1. returning")
            return
        mod_selected = self.active_list.item(0)
        mod_id = mod_selected.data(DATA_ROLE)
        
        self.mc.renameMod(mod_id, new_mod_name)
        
        #trigger tree redraw
        self.mod_updated.emit()
        
    def handlePlusButton(self):
        if (self.active_list.count() != 1):
            print("active list not size 1. returning")
            return
    
    def handleMinusButton(self):
        if (self.active_list.count() != 1):
            print("active list not size 1. returning")
            return
        
    def handleActiveListSizeChanged(self):
        active_list_size = self.active_list.count()
        if active_list_size != 1:
            self.mod_rename_button.setEnabled(False)
            self.category_name_button.setEnabled(False)
            self.sort_mod_label.setText("")
        else:
            self.mod_rename_button.setEnabled(True)
            self.category_name_button.setEnabled(True)
            current_item_id = self.active_list.item(0).data(DATA_ROLE)
            self.sort_mod_label.setText(self.mc.getModName(current_item_id))
        
                
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
