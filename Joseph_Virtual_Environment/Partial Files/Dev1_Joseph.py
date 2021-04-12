from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import argparse


class Window (QWidget):
      white   = QColor(255,255,255)
      black   = QColor(  0,  0,  0)
      arcrect = QRect(-10, -10, 20, 20)

      def __init__(self):
            super(Window, self).__init__()
            self.pixmap = QPixmap(400, 400)
            painter = QPainter(self.pixmap)
            painter.fillRect(self.pixmap.rect(), self.white)
            self.point1 = QPoint(20, 20)
            self.point2 = QPoint(380, 380)
            painter.setPen(self.black)
            painter.drawRect(QRect(self.point1, self.point2))
            painter.end()
            self.matrix = None      

class DragButton(QtWidgets.QPushButton):

      def mousePressEvent(self, event):
            self.__mousePressPos = None
            self.__mouseMovePos = None
            self.matrix = None
            if event.button() == QtCore.Qt.LeftButton:
                  self.__mousePressPos = event.globalPos()
                  self.__mouseMovePos = event.globalPos()

            super(DragButton, self).mousePressEvent(event)

      def mouseMoveEvent(self,event):
            if event.buttons() == QtCore.Qt.LeftButton:
                  currPos = self.mapToGlobal(self.pos())
                  globalPos = event.globalPos()
                  diff = globalPos - self.__mouseMovePos
                  newPos = self.mapFromGlobal(currPos + diff)
                  self.move(newPos)

                  self.__mouseMovePos = globalPos

            super(DragButton, self).mouseMoveEvent(event)

      def mouseReleaseEvent(self, event):
            if self.__mousePressPos is not None:
                  moved = event.globalPos() - self.__mousePressPos
                  if moved.manhattanLength() > 3:
                        event.ignore()
                        return
            print(event.x(), event.y()) 

            super(DragButton, self).mouseReleaseEvent(event)
            
class Ui_drag_drop(object):
      def andgdrag(self):
            print("AND press")  

      def setupUi(self,drag_drop):
      # Setup ---------------------
            drag_drop.setObjectName("drag_drop")
            drag_drop.resize(579, 445)
            print("Hello from setupUi")
            self.canvas_layout = QtWidgets
            self.centralwidget = QtWidgets.QWidget(drag_drop)
            self.centralwidget.setObjectName("centralwidget")

      # Button 1
            self.nand = DragButton(self.centralwidget)
            self.nand.setGeometry(QtCore.QRect(40, 50, 91, 50))
            self.nand.setText("")
            icon1 = QtGui.QIcon()
            icon1.addPixmap(QtGui.QPixmap(".\images\Diode.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.nand.setIcon(icon1)
            self.nand.setIconSize(QtCore.QSize(100, 90))
            self.nand.setObjectName("nand")

      # Menu ----------------------------
            drag_drop.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(drag_drop)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 579, 21))
      # Canvas -------------------
            self.canvas = QtWidgets.QLabel(self.centralwidget)
            self.canvas.lower()
            self.canvas.setGeometry(QtCore.QRect(140, 10, 821, 651))
            self.canvas.setMouseTracking(True)
            self.canvas.setAutoFillBackground(False)
            self.canvas.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(255, 255, 255);\n"
                                    "border-color: rgb(0, 0, 0);")
            self.canvas.setText("")
            self.canvas.setObjectName("canvas")

      def retranslateUi(self, drag_drop):
            _translate = QtCore.QCoreApplication.translate
            drag_drop.setWindowTitle(_translate("drag_drop", "MainWindow"))
            self.menuHelp.setTitle(_translate("drag_drop", "More"))
            self.actionHelp.setText(_translate("drag_drop", "Help"))

if __name__ == "__main__":
      app = QtWidgets.QApplication(sys.argv)
      thing = Window()
      drag_drop = QtWidgets.QMainWindow()
      ui = Ui_drag_drop()
      ui.setupUi(drag_drop)
      drag_drop.show()
      print("End of program")
      sys.exit(app.exec_())