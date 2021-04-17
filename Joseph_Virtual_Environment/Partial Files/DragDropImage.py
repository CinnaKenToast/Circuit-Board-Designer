from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

class DragButton(QtWidgets.QPushButton):

    def mousePressEvent(self, event):
        self.__mousePressPos = None
        self.__mouseMovePos = None
        if event.button() == QtCore.Qt.LeftButton:
            self.__mousePressPos = event.globalPos()
            self.__mouseMovePos = event.globalPos()

        super(DragButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            # adjust offset from clicked point to origin of widget
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

        super(DragButton, self).mouseReleaseEvent(event)

class Ui_drag_drop(object):

    def andgdrag(self):
        print("AND press")

    def setupUi(self, drag_drop):
        drag_drop.setObjectName("drag_drop")
        drag_drop.resize(579, 445)
        self.canvas_layout = QtWidgets
        self.centralwidget = QtWidgets.QWidget(drag_drop)
        self.centralwidget.setObjectName("centralwidget")

        drag_drop.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(drag_drop)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 579, 21))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        drag_drop.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(drag_drop)
        self.statusbar.setObjectName("statusbar")
        drag_drop.setStatusBar(self.statusbar)
        self.actionHelp = QtWidgets.QAction(drag_drop)
        self.actionHelp.setObjectName("actionHelp")
        self.menuHelp.addAction(self.actionHelp)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(drag_drop)
        QtCore.QMetaObject.connectSlotsByName(drag_drop)

        # andg
        self.andg = DragButton(self.centralwidget)
        self.andg.setGeometry(QtCore.QRect(10, 0, 91, 50))
        self.andg.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("and.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.andg.setIcon(icon)
        self.andg.setIconSize(QtCore.QSize(100, 50))
        self.andg.setObjectName("andg")
        #
        self.andg.clicked.connect(self.andgdrag)

        ##nand

        self.nand = DragButton(self.centralwidget)
        self.nand.setGeometry(QtCore.QRect(40, 50, 91, 50))
        self.nand.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("nand.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nand.setIcon(icon1)
        self.nand.setIconSize(QtCore.QSize(100, 50))
        self.nand.setObjectName("nand")

        # notg
        self.notg = DragButton(self.centralwidget)
        self.notg.setGeometry(QtCore.QRect(10, 110, 91, 50))
        self.notg.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("not.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.notg.setIcon(icon2)
        self.notg.setIconSize(QtCore.QSize(100, 50))
        self.notg.setObjectName("notg")

        # org
        self.org = DragButton(self.centralwidget)
        self.org.setGeometry(QtCore.QRect(40, 170, 91, 50))
        self.org.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("or.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.org.setIcon(icon3)
        self.org.setIconSize(QtCore.QSize(100, 90))
        self.org.setObjectName("org")

        # nor
        self.nor = DragButton(self.centralwidget)
        self.nor.setGeometry(QtCore.QRect(10, 230, 91, 50))
        self.nor.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("nor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.nor.setIcon(icon4)
        self.nor.setIconSize(QtCore.QSize(120, 60))
        self.nor.setObjectName("nor")

        # exor
        self.exor = DragButton(self.centralwidget)
        self.exor.setGeometry(QtCore.QRect(40, 290, 91, 50))
        self.exor.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("exor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exor.setIcon(icon5)
        self.exor.setIconSize(QtCore.QSize(110, 60))
        self.exor.setObjectName("exor")

        # exnor
        self.exnor = DragButton(self.centralwidget)
        self.exnor.setGeometry(QtCore.QRect(10, 350, 91, 50))
        self.exnor.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("exnor.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exnor.setIcon(icon6)
        self.exnor.setIconSize(QtCore.QSize(110, 60))
        self.exnor.setObjectName("exnor")

        # canvas
        self.canvas = QtWidgets.QLabel(self.centralwidget)
        self.canvas.lower()
        self.canvas.setGeometry(QtCore.QRect(140, 10, 421, 351))
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
    import sys

    app = QtWidgets.QApplication(sys.argv)
    drag_drop = QtWidgets.QMainWindow()
    ui = Ui_drag_drop()
    ui.setupUi(drag_drop)
    drag_drop.show()
    sys.exit(app.exec_())