from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QHBoxLayout, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import sys

class Window(QWidget):
      def __init__(self):
            super().__init__()

            self.myListWidget1 = QListWidget()
            self.myListWidget2 = QListWidget()

            self.iconSize = QSize(150, 150)

            #self.myListWidget1.setViewMode(QListWidget.IconMode)
            self.myListWidget1.setIconSize(self.iconSize)
            self.myListWidget2.setViewMode(QListWidget.IconMode)
            
            self.myListWidget1.setAcceptDrops(True)
            self.myListWidget1.setDragEnabled(True)
            
            self.myListWidget2.setAcceptDrops(True)
            self.myListWidget2.setDragEnabled(True)

            self.setGeometry(300, 350, 500, 300)
            
            self.hboxlayout = QHBoxLayout()
            self.hboxlayout.addWidget(self.myListWidget1)
            self.hboxlayout.addWidget(self.myListWidget2)

            l1 = QListWidgetItem(QIcon("../src/images/Led.svg"), "LED")
            l2 = QListWidgetItem(QIcon("kitty.png"), "MEOW")

            self.myListWidget1.insertItem(1, l1)
            self.myListWidget1.insertItem(2, l2)

            QListWidgetItem(QIcon("pythonlogo.png"), "PYTON", self.myListWidget2)

            self.setWindowTitle("DRAG DROP")
            self.setLayout(self.hboxlayout)

            self.show()



app = QApplication(sys.argv)
window=Window()
sys.exit(app.exec_())