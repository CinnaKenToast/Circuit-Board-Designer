import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI FILE
from ui_main import Ui_MainWindow
from twoPin import Ui_Form

# IMPORT FUNCTIONS
# from ui_functions import *

eventList = []

def addToEvent(item):
    if len(eventList) == 2:
        eventList[0] = eventList[1]
        eventList[1] = item
    else:
        eventList.append(item)
    print(eventList)

class Widget(QtWidgets.QWidget):
    def __init__(self, name, scene, boundingBox, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_name.setText(name)
        self.ui.btn_pin0.clicked.connect(lambda: self.printLeftButtonPos())
        self.ui.btn_pin1.clicked.connect(lambda: self.printRightButtonPos())
        self.boundingBox = boundingBox
        self.scene = scene
    
    def printLeftButtonPos(self):
        #self.boundingBox.setSelected(True)
        print(self.boundingBox.pos())
        pin0x = self.boundingBox.pos().x()
        pin0y = self.boundingBox.pos().y() + 20 + 75/2
        addToEvent((self.boundingBox, QPoint(pin0x, pin0y)))

    def printRightButtonPos(self):
        #self.boundingBox.setSelected(True)
        print(self.boundingBox.pos())
        pin1x = self.boundingBox.pos().x() + 150
        pin1y = self.boundingBox.pos().y() + 20 + 75/2
        addToEvent((self.boundingBox, QPoint(pin1x, pin1y)))

class component(QtWidgets.QGraphicsRectItem):
    def __init__(self, scene, pen, name):
        super().__init__()
        self.scene = scene
        self.boundingBox = self.scene.addRect(0,0, 150, 95, pen)
        self.widget = self.scene.addWidget(Widget(name, scene, self.boundingBox))
        self.boundingBox.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.boundingBox.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.widget.setParentItem(self.boundingBox)   
        self.line = None
        self.isPoint = None
        #print(self.boundingBox.parent())
        print(self)

    def mousePressEvent(self, event):
        print("Hello")
        self.boundingBox.setSelected(False)

    def addLine(self, line, ispoint):
        self.line = line
        self.isPoint = ispoint
    
    def itemChange(self, change, value):
        print("HELLO")
        if change == self.ItemPositionChange and self.scene():
            newPos = value
            self.moveLineToCenter(newPos)
        
        return super(component, self).itemChange(change, value)

    def moveLineToCenter(self, newPos):
        xOffset = self.rect().x() + self.rect().width()/2
        yOffset = self.rect().y() + self.rect().height()/2

        newCenterPos = QtCore.QPointF(newPos.x()+xOffset, newPos.y()+yOffset)

        p1 = newCenterPos if self.isPoint else self.line.line().p1()
        p2 = self.line.line().p2() if self.isPoint else newCenterPos

        self.line.setLine(QtCore.QLineF(p1, p2))


class MainWindow(QMainWindow):
    def __init__(self):
        # Window set up
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menuStates = ["Closed", "menuComponents", "menuColors"]
        self.currentState = self.menuStates[0]
        self.scene = QtWidgets.QGraphicsScene()
        self.ui.window_canvas.setScene(self.scene)
        self.ui.window_canvas.setMouseTracking(True)
        self.zoom = 100
        self.scene.setSceneRect(0.0, 0.0, 3000.0, 2000.0)
        self.ui.window_canvas.move(1500.0, 1000.0)
        self.ui.window_canvas.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.ui.window_canvas.centerOn(1500.0, 1000.0)
        redBrush = QtGui.QBrush(QtCore.Qt.red)
        blackPen = QtGui.QPen(QtCore.Qt.black)
        blackPen.setWidth(5)

        self.penColor = QtGui.QPen(QtCore.Qt.black)
        self.penColor.setWidth(3)

        self.component1 = component(self.scene, self.penColor, "resistor")
        self.component1.boundingBox.moveBy(1000, 1000)

        self.penColors = {
                "black" : QtCore.Qt.black,
                "red" : QtCore.Qt.red,
                "orange" : QtGui.QColor(255, 166, 0), 
                "yellow" : QtCore.Qt.yellow,
                "green" : QtCore.Qt.green,
                "blue" : QtCore.Qt.blue,
                "purple" : QtGui.QColor(221, 101, 247), 
                "pink" : QtGui.QColor(255, 186, 244), 
                "cyan" : QtCore.Qt.cyan,
                "brown" : QtGui.QColor(122, 112, 97)
        }

        ellipse = self.scene.addEllipse(1000,1000,50,50,self.penColors["brown"],redBrush)
        ellipse.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)

        # Connect buttons to functions
        self.ui.btn_toggle.clicked.connect(lambda: self.toggleMenu(200, True))
        self.ui.btn_design.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_design))
        self.ui.btn_convert.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_convert))
        self.ui.btn_file.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_file))

        '''
        self.ui.btn_wire.clicked.connect(lambda: uiFunctions.toggleTools(self, 50, True, "btn_wire"))
        self.ui.btn_snip.clicked.connect(lambda: uiFunctions.toggleTools(self, 50, True, "btn_snip"))
        self.ui.btn_delete.clicked.connect(lambda: uiFunctions.toggleTools(self, 50, True, "btn_delete"))
        self.ui.btn_label.clicked.connect(lambda: uiFunctions.toggleTools(self, 50, True, "btn_clicked"))
        self.ui.btn_comment.clicked.connect(lambda: uiFunctions.toggleTools(self, 50, True, "btn_comment"))
        '''
        self.ui.btn_wire.clicked.connect(lambda: self.toggleTools(50, "btn_wire"))
        self.ui.btn_snip.clicked.connect(lambda: self.toggleTools(50, "btn_snip"))
        self.ui.btn_delete.clicked.connect(lambda: self.toggleTools(50, "btn_delete"))
        self.ui.btn_label.clicked.connect(lambda: self.toggleTools(50, "btn_clicked"))
        self.ui.btn_comment.clicked.connect(lambda: self.toggleTools(50, "btn_comment"))

        self.ui.btn_add.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_components))
        self.ui.btn_color.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_colors))
        
        '''
        tooslOpened = self.ui.btn_add.clicked.connect(lambda: uiFunctions.toggleTools(self, 100, True, "page_components"))
        toolsOpened = self.ui.btn_color.clicked.connect(lambda: uiFunctions.toggleTools(self, 100, True, "page_colors"))
        
        self.ui.btn_add.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_components))
        self.ui.btn_color.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_colors))
        '''

        self.ui.btn_add.clicked.connect(lambda: self.toggleTools(100, "btn_add"))
        self.ui.btn_color.clicked.connect(lambda: self.toggleTools(100, "btn_colors"))
        
        self.ui.btn_add.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_components))
        self.ui.btn_color.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_colors))

        self.ui.btn_zoom_in.clicked.connect(lambda: self.zoomIn())
        self.ui.btn_zoom_out.clicked.connect(lambda: self.zoomOut())
        self.ui.btn_zoom_home.clicked.connect(lambda: self.zoomHome())

        self.ui.btn_black.clicked.connect(lambda: self.changePenColor("black"))
        self.ui.btn_red.clicked.connect(lambda: self.changePenColor("red"))
        self.ui.btn_orange.clicked.connect(lambda: self.changePenColor("orange"))
        self.ui.btn_yellow.clicked.connect(lambda: self.changePenColor("yellow"))
        self.ui.btn_green.clicked.connect(lambda: self.changePenColor("green"))
        self.ui.btn_blue.clicked.connect(lambda: self.changePenColor("blue"))
        self.ui.btn_purple.clicked.connect(lambda: self.changePenColor("purple"))
        self.ui.btn_pink.clicked.connect(lambda: self.changePenColor("pink"))
        self.ui.btn_cyan.clicked.connect(lambda: self.changePenColor("cyan"))
        self.ui.btn_brown.clicked.connect(lambda: self.changePenColor("brown"))

        self.show()


#------------------- BUTTON FUNCTIONS -------------------
        # Zooms in on the scene
    def zoomIn(self):
        self.zoom += 20
        if self.zoom >= 200:
                self.zoom = 200
        scaleFactorX = self.zoom/100/self.ui.window_canvas.transform().m11()
        scaleFactorY = self.zoom/100/self.ui.window_canvas.transform().m22()
        self.ui.window_canvas.scale(scaleFactorX, scaleFactorY)

    # Zooms out on the scene
    def zoomOut(self):
        self.zoom -= 20
        if self.zoom <= 20:
                self.zoom = 20
        scaleFactorX = self.zoom/100/self.ui.window_canvas.transform().m11()
        scaleFactorY = self.zoom/100/self.ui.window_canvas.transform().m22()
        self.ui.window_canvas.scale(scaleFactorX, scaleFactorY)
    
    # Sets zoom back to default
    def zoomHome(self):
        self.zoom = 100
        scaleFactorX = self.zoom/100/self.ui.window_canvas.transform().m11()
        scaleFactorY = self.zoom/100/self.ui.window_canvas.transform().m22()
        self.ui.window_canvas.scale(scaleFactorX, scaleFactorY)

    def changePenColor(self, color):
        self.penColor.setColor(color)
        print(color)

    # Toggles the left pull out menu for the different screens
    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.ui.frame_menu.width()
            # print(width)
            maxExtend = maxWidth
            standard = 0

            if width == 0:
                    widthExtended = maxExtend
            else:
                    widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.frame_menu, b"minimumWidth")
            self.animation.setDuration(200)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
    # Toggles the right pull out menu for the tools
    def toggleTools(self, maxWidth, button):
        enable = False
        buttons = ["btn_wire", "btn_snip", "btn_delete", "btn_clicked", "btn_comment"]
        
        print("Start:", button, "|", self.currentState)

        if button in buttons and self.currentState != "Closed":
            enable = True
            self.currentState = self.menuStates[0]

        elif button == "btn_add" and self.currentState == "menuComponents":
            enable = True
            self.currentState = self.menuStates[0]

        elif button == "btn_colors" and self.currentState == "menuColors":
            enable = True
            self.currentState = self.menuStates[0]

        elif button == "btn_add" and self.currentState == "Closed":
            enable = True
            self.currentState = self.menuStates[1]

        elif button == "btn_colors" and self.currentState == "Closed":
            enable = True
            self.currentState = self.menuStates[2]
        
        elif button == "btn_add" and self.currentState == "menuColors":
            enable = False
            self.currentState = self.menuStates[1]

        elif button == "btn_colors" and self.currentState == "menuComponents":
            enable = False
            self.currentState = self.menuStates[2]

        if enable:
            width = self.ui.frame_tools.width()
            height = self.ui.frame_tools.height()
            # print(width)
            maxExtend = maxWidth
            standard = 50

            if width == 50:
                widthExtended = maxExtend
                toolsOpened = True
                    
            else:
                widthExtended = standard
                toolsOpened = False
                    
            #print(toolsOpened)
            # print("width it should be", widthExtended)
            self.animation = QPropertyAnimation(self.ui.frame_tools, b"minimumSize")
            self.animation.setDuration(150)
            self.animation.setStartValue(QtCore.QSize(width, height))
            self.animation.setEndValue(QtCore.QSize(widthExtended, height))
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()
            print(self.ui.frame_tools.width())
            # print(self.ui.stacked_tools.currentWidget().accessibleName())


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())