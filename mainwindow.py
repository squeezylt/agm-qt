
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTreeWidgetItem, QTreeWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import QSettings, pyqtSignal, QDir
import maincontrol


from PyQt5 import QtCore, QtGui, QtWidgets, uic
import os.path
import sys
import filecontrol as fc
import mod_data
from PyQt5.QtCore import QUuid

#made by squeezylt


#usage in qt embedded widget data
USER_ROLE = QtCore.Qt.UserRole
DATA_ROLE = QtCore.Qt.UserRole + 1
EXTRA_DATA_ROLE = QtCore.Qt.UserRole + 2 #reserved, unused?


class MainWindow(QMainWindow):

    mod_path_set = pyqtSignal(str)   
    settings_updated = pyqtSignal()
    mod_updated = pyqtSignal()
    
    refresh_mod_tree = pyqtSignal()
    
    refresh_active_tool_list = pyqtSignal()
    
    refresh_sorting_mod = pyqtSignal()
    
    #single mod has been renamed
    mod_renamed = pyqtSignal(QUuid)
    
    mod_cat_updated = pyqtSignal(QUuid)
    
    
    
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
        self.category_name_button.clicked.connect(self.handleCategoryNameButton)
        self.remove_selected_button.clicked.connect(self.handleRemoveSelected)
        self.mod_rename_button.clicked.connect(self.handleModRenameApply)
        self.category_combo.currentIndexChanged.connect(self.handleCategoryIndexChanged)

        #custom tree setup
        self.xtree = XTreeWidget(QTreeWidget)
        self.mainlayout.addWidget(self.xtree)
        self.xtree.itemChecked.connect(self.handleModToggled)
        self.xtree.itemClicked.connect(self.handleModSelected)
        self.xtree.setHeaderLabel("Mods")
        
        
        #widget things
        self.mod_rename_button.setEnabled(False)
        self.category_name_button.setEnabled(False)
        
        #not yet enabled lol
        self.minus_button.setEnabled(False)

        #settings
        self.loadSettings()
        
        self.actionLoad_Mod_Dir.triggered.connect(self.loadModDir)
        
        #refresh of things when actions are called
        #self.actionRefresh_Mod_List.triggered.connect(self.handleRefreshModTree)
        #self.refresh_mod_tree.connect(self.handleRefreshModTree)
        #self.refresh_active_tool_list.connect(self.handleRefreshActiveToolList)
        #self.refresh_sorting_mod.connect(self.handleRefreshSortingMod)
        self.mod_renamed.connect(self.handleModRenamed)
        self.mod_cat_updated.connect(self.handleModCatUpdated)
        
        
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
        #this is cursed. -squeezy
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
        #self.mod_updated.emit()
        self.mod_renamed.emit(mod_id)
        
    def handlePlusButton(self):
        if (self.active_list.count() != 1):
            print("active list not size 1. returning")
            return
        self.category_combo.addItem("Category Level" + str(self.category_combo.count()),self.category_combo.count())
        
    
    def handleMinusButton(self):
        if (self.active_list.count() != 1):
            print("active list not size 1. returning")
            return
        
    def handleCategoryNameButton(self):
        #handle apply button
        category_text = self.category_edit.text()
        level = self.category_combo.itemData(self.category_combo.currentIndex(),USER_ROLE)
        
        if not category_text:
            print('category text empty')
            return
        
        mod_id = self.active_list.item(0).data(DATA_ROLE)
        if not mod_id:
            print("Error:couldnt find mod for category naming")
            return
        
        self.mc.writeModCategory(mod_id,level,category_text)
        self.actionRefresh_Mod_List.triggered.emit()
        #self.refresh.emit()
        
    def handleCategoryIndexChanged(self,index):
        if self.active_list.count() <= 0:
            return
        if self.category_combo.count() <= 0:
            return
        print("combo count is " + str(self.category_combo.count()) )
        
        if self.active_list.count() == 1:
            mod_id = self.active_list.item(0).data(DATA_ROLE)
            level = self.category_combo.itemData(index,USER_ROLE)
            if level is None:
                return
            category = self.mc.getCategory(mod_id, level)
            if not category:
                print("no category, returning")
                return
            self.category_edit.setText(category)
        else:
            self.category_edit.setText("")
        
        
    def handleActiveListSizeChanged(self):
        active_list_size = self.active_list.count()
        if active_list_size != 1:
            self.mod_rename_button.setEnabled(False)
            self.category_name_button.setEnabled(False)
            self.sort_mod_label.setText("")
            self.rename_edit.clear()
            self.category_combo.clear()
        else:
            self.mod_rename_button.setEnabled(True)
            self.category_name_button.setEnabled(True)
            current_item_id = self.active_list.item(0).data(DATA_ROLE)
            self.sort_mod_label.setText(self.mc.getModName(current_item_id))
            self.rename_edit.clear()
            self.category_combo.clear()
            
            #get existing categories if they exist
            mod_id = self.active_list.item(0).data(DATA_ROLE)
            categories = self.mc.getCategories(mod_id)
            
            for i in range(len(categories)):
                self.category_combo.addItem("Category Level" + str(i),i)
                
            
    '''        
    def handleRefresh(self):
        self.active_list.clear()
        self.mod_path_set.emit(self.mod_path)
        self.category_combo.clear()
        self.category_edit.setText("")
        self.sort_mod_label.setText("")
    '''
    # slots
    def handleModRenamed(self,id):
        name = self.mc.getModName(id)
        if not name:
            return
        
        if self.active_list.count() == 1:
            #have a mod in list
            self.sort_mod_label.setText(name)
            
            active_id = self.active_list.item(0).data(DATA_ROLE)
            if active_id == id:
                self.active_list.item(0).setText(name)
            self.setTreeModItemName(id)
                
    
    #this isnt most efficient or correct. but working        
    def setTreeModItemName(self,id):
        cat_item = None
        item = None
        name = self.mc.getModName(id)
        cat_item = self.getTreeItemById(id)
        print("cat_item is " + str(cat_item))
        if not cat_item:
            print("Cat item not mod in set mod tree name")
            return
        print("Setting text to " + name)
        cat_item.setText(0,name)
        
    


    def getTreeItemById(self,id,cat_item=None):
        cat_item = None
        for i in range(self.xtree.topLevelItemCount()):
            item = self.xtree.topLevelItem(i)
            cat_item = self.getRecursiveTreeItemById(item, id)
            #print("cat_item is " + str(cat_item))
            if cat_item:
                print("GOT OUR ITEM")
                
                return cat_item
        return cat_item
        
    def getRecursiveTreeItemById(self, item, id):
        if item.data(0, DATA_ROLE) == id:
            print("Found the correct return item")
            return item

        for i in range(item.childCount()):
            child = item.child(i)
            result = self.getRecursiveTreeItemById(child, id)
            if result is not None:
                # If we found the item in a child, return it
                return result
        # If we didn't find the item in this item or any of its children, return None
        return None
        
    
    def handleModCatUpdated(self,id):
        pass
                
        
    
        
                
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
    window.setWindowTitle("AGM Manager Beta")
    app.exec_()

if __name__ == "__main__":
    main()
