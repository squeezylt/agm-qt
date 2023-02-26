from PyQt5.QtWidgets import QTreeWidgetItem, QTreeWidget, QWidget, QSizePolicy
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QSettings, pyqtSignal, QDir, QSize

#usage in qt embedded widget data
USER_ROLE = QtCore.Qt.UserRole
DATA_ROLE = QtCore.Qt.UserRole + 1
EXTRA_DATA_ROLE = QtCore.Qt.UserRole + 2 #reserved, unused?


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

    def __init__(self,parent=None):
        QTreeWidget.__init__(self)   
        
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
    
class ModTreeView(QWidget):
    
    def __init__(self, parent=None):
        super(ModTreeView, self).__init__(parent)
        self.xtree = XTreeWidget(QTreeWidget)
        self.xtree.setParent(self)
        
        #self.xtree.itemChecked.connect(self.handleModToggled)
        #self.xtree.itemClicked.connect(self.handleModSelected)
        self.xtree.setHeaderLabel("Mods")
        #self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #self.xtree.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.show()
        
    def sizeHint(self):
        return self.xtree.sizeHint()
        #return QSize(15,15)
    def minimumSizeHint(self):
        return self.xtree.minimumSizeHint()
    #def sizePolicy(self) -> 'QSizePolicy':
    #    return self.xtree.sizePolicy()

        
    def updateModTreeWidget(self, mod_list):
        #i want to rewrite this entire function but my brain hurts
        #this is cursed. -squeezy
        
        #mod_list = self.mc.getModDataStructure()
        print('updating mod tree')
        
        if (not mod_list):
            print("mod list empty")
            return
        self.xtree.clear()
        
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
                #print("first cat is " + first_cat)
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
        