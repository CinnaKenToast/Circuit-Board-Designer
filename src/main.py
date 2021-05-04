import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets, QtSvg
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI FILE
from ui_main import Ui_MainWindow
from twoPin import Ui_Form

import classes

# IMPORT FUNCTIONS
# from ui_functions import *

eventList = []

def addToEvent(item):
    if len(eventList) == 2:
        eventList[0] = eventList[1]
        eventList[1] = item
    else:
        eventList.append(item)
    #print(eventList)

class Widget(QtWidgets.QWidget):
    def __init__(self, compType, name, scene, boundingBox, id, parent = None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_name.setText(name)
        self.ui.btn_pin0.clicked.connect(lambda: self.printLeftButtonPos())
        self.ui.btn_pin1.clicked.connect(lambda: self.printRightButtonPos())
        self.boundingBox = boundingBox
        self.scene = scene
        self.id = id

        if compType == "Resistor":
            self.setImage("Resistor")
        elif compType == "Capacitor":
            self.setImage("Capacitor")
        elif compType == "Diode":
            self.setImage("Diode")
        elif compType == "Led":
            self.setImage("Led")
        elif compType == "Inductor":
            self.setImage("Inductor")
        elif compType == "Switch":
            self.setImage("Switch")
        elif compType == "VoltageSource":
            self.setImage("Voltage Source")
            
    
    def printLeftButtonPos(self):
        #self.boundingBox.setSelected(True)
        #print(self.boundingBox.pos())
        pin0x = self.boundingBox.pos().x() + 12
        pin0y = self.boundingBox.pos().y() + 30 + 60/2
        addToEvent((self.boundingBox, QPoint(pin0x, pin0y), [self.id, 0]))

    def printRightButtonPos(self):
        #self.boundingBox.setSelected(True)
        #print(self.boundingBox.pos())
        pin1x = self.boundingBox.pos().x() + 170 - 12
        pin1y = self.boundingBox.pos().y() + 30 + 60/2
        addToEvent((self.boundingBox, QPoint(pin1x, pin1y), [self.id, 1]))
    
    def setImage(self, compType):
        svgRenderer = None
        image = QtGui.QImage(170, 60, QtGui.QImage.Format_ARGB32)
        image.fill(0x00000000)
        svgRenderer = QtSvg.QSvgRenderer("comp_img/"+compType+".svg")
        svgRenderer.render(QtGui.QPainter(image))
        pixmap = QtGui.QPixmap.fromImage(image)
        self.ui.lable_image.setPixmap(pixmap)

class Component(QtWidgets.QGraphicsRectItem):
    def __init__(self, scene, pen, compType, name, id):
        super().__init__()
        self.scene = scene
        self.name = name
        self.compType = compType
        self.id = id
        self.boundingBox = self.scene.addRect(0,0, 170, 95, pen)
        self.widget = Widget(compType, self.name, self.scene, self.boundingBox, self.id)
        self.sceneWidget = self.scene.addWidget(self.widget)
        self.boundingBox.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.boundingBox.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.sceneWidget.setParentItem(self.boundingBox)   
        self.schematicArgs = {}
        self.pin0Connection = None
        self.pin1Connection = None

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
        
        return super(Component, self).itemChange(change, value)

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
        self.ids = 2
        self.penColor = QtGui.QPen(QtCore.Qt.black)
        self.penColor.setWidth(3)

        self.components = []
        self.schematic = classes.Schematic()
        self.connections = []

# ------------------ Test Components ------------------
        self.component1 = Component(self.scene, self.penColor, "Resistor", "r1", 0)
        self.component1.boundingBox.moveBy(1000, 1000)
        self.component1.schematicArgs = {"id": 0, "label": self.component1.name, "component_type": "Resistor"} 
        self.schematic.add_component(self.component1.schematicArgs)
        self.schematic.set_component_schematic_pos(0, [self.component1.boundingBox.pos().x(), self.component1.boundingBox.pos().y()])
        self.components.append(self.component1)

        self.component2 = Component(self.scene, self.penColor, "Diode", "d1", 1)
        self.component2.boundingBox.moveBy(1500, 1000)
        self.component2.schematicArgs = {"id": 1, "label": self.component2.name, "component_type": "Diode"} 
        self.schematic.add_component(self.component2.schematicArgs)
        self.schematic.set_component_schematic_pos(1, [self.component2.boundingBox.pos().x(), self.component2.boundingBox.pos().y()])
        self.components.append(self.component2)
# -----------------------------------------------------

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
                "brown" : QtGui.QColor(119, 90, 49)
        }

        # Connect buttons to functions
        self.ui.btn_resistor.clicked.connect(lambda: self.addComponent("Resistor", "r1"))
        self.ui.btn_capacitor.clicked.connect(lambda: self.addComponent("Capacitor", "c1"))
        self.ui.btn_diode.clicked.connect(lambda: self.addComponent("Diode", "d1"))
        self.ui.btn_led.clicked.connect(lambda: self.addComponent("Led", "l1"))
        self.ui.btn_inductor.clicked.connect(lambda: self.addComponent("Inductor", "i1"))
        self.ui.btn_switch.clicked.connect(lambda: self.addComponent("Switch", "s1"))
        self.ui.btn_voltage.clicked.connect(lambda: self.addComponent("VoltageSource", "v1"))

        self.ui.btn_delete.clicked.connect(lambda: self.deleteComponent())

        self.ui.btn_wire.clicked.connect(lambda:self.addConnection())

        self.ui.btn_toggle.clicked.connect(lambda: self.toggleMenu(200, True))
        self.ui.btn_design.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_design))
        self.ui.btn_convert.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_convert))
        self.ui.btn_file.clicked.connect(lambda: self.ui.stacked_workspaces.setCurrentWidget(self.ui.page_file))

        self.ui.btn_wire.clicked.connect(lambda: self.toggleTools(50, "btn_wire"))
        self.ui.btn_snip.clicked.connect(lambda: self.toggleTools(50, "btn_snip"))
        self.ui.btn_delete.clicked.connect(lambda: self.toggleTools(50, "btn_delete"))
        self.ui.btn_label.clicked.connect(lambda: self.toggleTools(50, "btn_clicked"))
        self.ui.btn_comment.clicked.connect(lambda: self.toggleTools(50, "btn_comment"))

        self.ui.btn_add.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_components))
        self.ui.btn_color.clicked.connect(lambda: self.ui.stacked_tools.setCurrentWidget(self.ui.page_colors))

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

        self.ui.btn_label.clicked.connect(lambda: self.changeLabel())
        self.ui.btn_comment.clicked.connect(lambda: self.printSchematic())
        self.ui.btn_snip.clicked.connect(lambda: self.removeConnection())

        self.scene.changed.connect(lambda: self.updatePositions())

        self.show()


#------------------- BUTTON FUNCTIONS -------------------
    # Update the positions of the components
    def updatePositions(self):
        for component in self.components:
            compId = component.id
            self.schematic.set_component_schematic_pos(compId, [component.boundingBox.pos().x(), component.boundingBox.pos().y()])

    # Print all components in schematic
    def printSchematic(self):
        for component in self.schematic.components.values():
            print(component.to_string())
        print(self.connections)

    # Add component to the scene
    def addComponent(self, component, name):
        name, ok = QtWidgets.QInputDialog.getText(self, 'Component Name', 'Enter component name:')
        if ok:
            newComponent = Component(self.scene, self.penColor, component, name, self.ids)
            newComponent.boundingBox.moveBy(1500,1000)
            newComponent.schematicArgs = {"id": self.ids, "label": newComponent.name, "component_type": component} 
            newComponent.id = self.ids
            self.schematic.add_component(newComponent.schematicArgs)
            self.schematic.set_component_schematic_pos(self.ids, [newComponent.boundingBox.pos().x(), newComponent.boundingBox.pos().y()])
            #print(self.component1.boundingBox.pos().x(), self.component1.boundingBox.pos().y())
            self.components.append(newComponent)
            self.ids += 1

        for component in self.schematic.components.values():
            print(component.to_string())

    # Deleted selected component from scene
    def deleteComponent(self):
        for component in self.components:
            if component.boundingBox.pos() == self.scene.selectedItems()[0].pos():
                compId = component.id     
                self.scene.removeItem(self.scene.selectedItems()[0])
                comp = component
                self.components.remove(comp)
                self.schematic.remove_component(compId)
                del comp

    # Adds connection between two components
    def addConnection(self):
        if len(eventList) < 2:
            print("Not enough events")
        elif eventList[0][0] == eventList[1][0]:
            print("Can't connect the pins of same component")
        else:
            line = self.scene.addLine(QtCore.QLineF(eventList[0][1], eventList[1][1]), self.penColor)
            pinId0 = str(eventList[0][2][0]) + "_" + str(eventList[0][2][1]) 
            pinId1 = str(eventList[1][2][0]) + "_" + str(eventList[1][2][1]) 
            self.connections.append(line)
            self.schematic.add_connection(pinId0, pinId1)
            for component in self.components:
                if component.id == eventList[0][2][0]: # Check if component is first event 
                    if eventList[0][2][1] == 0: # which pin was pressed
                        component.pin0Connection = line
                    else:
                        component.pin1Connection = line
                elif component.id == eventList[1][2][0]: # Check if component is second event
                    if eventList[1][2][1] == 0: # Which pin was pressed
                        component.pin0Connection = line
                    else:
                        component.pin1Connection = line
            print(self.connections)
    
    # Delete the connection between two components
    def removeConnection(self):
        if len(eventList) < 2:
            print("Not enough events")
        elif eventList[0][0] == eventList[1][0]:
            print("There can't be a connection between pins of the same component.")
        else:
            pinId0 = str(eventList[0][2][0]) + "_" + str(eventList[0][2][1]) 
            pinId1 = str(eventList[1][2][0]) + "_" + str(eventList[1][2][1]) 
            self.schematic.remove_connection(pinId0, pinId1)
            component1 = None
            component2 = None
            for component in self.components:
                if component.boundingBox == eventList[0][0]:
                    component1 = component
                    print("component1", component1)
                if component.boundingBox == eventList[1][0]:
                    component2 = component
                    print("component2", component2)
            if not(component1.pin0Connection == None):
                self.scene.removeItem(component1.pin0Connection)
                self.connections.remove(component1.pin0Connection)
                component1.pin0Connection = None
            else:
                self.scene.removeItem(component1.pin1Connection)
                self.connections.remove(component1.pin1Connection)             
                component1.pin1Connection = None
            if not(component2.pin0Connection == None):
                component2.pin0Connection = None
            else:
                component2.pin1Connection = None
            
    # Change the label on a component
    def changeLabel(self):
        if len(self.scene.selectedItems()) == 0:
            print("Nothing selected")
        else:
            name, ok = QtWidgets.QInputDialog.getText(self, 'Component Name', 'Enter component name:')
            for component in self.components:
                if component.boundingBox.pos() == self.scene.selectedItems()[0].pos() and ok:
                    component.widget.ui.label_name.setText(name)
                    compId = component.id
                    self.schematic.edit_label(compId, name)

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

    # Changes color of the wire pen
    def changePenColor(self, color):
        self.penColor.setColor(color)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("color_img/"+color+"Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ui.btn_color.setIcon(icon)
        print(color)
        self.toggleTools(50, "btn_pick_color")

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
        buttons = ["btn_wire", "btn_snip", "btn_delete", "btn_clicked", "btn_comment", "btn_pick_color"]
        
        # print("Start:", button, "|", self.currentState)

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
            self.ui.frame_top_extra_tools.setMaximumSize(QtCore.QSize(50, 350))

        elif button == "btn_colors" and self.currentState == "Closed":
            enable = True
            self.currentState = self.menuStates[2]
            self.ui.frame_top_extra_tools.setMaximumSize(QtCore.QSize(50, 500))
        
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
            # print(self.ui.frame_tools.width())
            # print(self.ui.stacked_tools.currentWidget().accessibleName())


if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())