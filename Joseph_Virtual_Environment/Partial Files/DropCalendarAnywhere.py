# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import sys
  
# QCalendarWidget Class
class Calendar(QCalendarWidget):
  
    # constructor
    def __init__(self, parent = None):
        super(Calendar, self).__init__(parent)
  
    # overriding the mouse press event
    def mousePressEvent(self, QMouseEvent):
  
        # making flag true
        window.move_calendar = True
  
    # overriding the mouse release event
    def mouseReleaseEvent(self, event):
  
        # making flag false
        window.move_calendar = False
  
  
  
  
  
class Window(QMainWindow):
  
    def __init__(self):
        super().__init__()
  
        # setting title
        self.setWindowTitle("Python ")
  
        # setting geometry
        self.setGeometry(100, 100, 650, 400)
  
        # calling method
        self.UiComponents()
  
        # showing all the widgets
        self.show()
  
        # creating amove flag
        self.move_calendar = False
  
    # method for components
    def UiComponents(self):
  
        # creating a QCalendarWidget object
        # as Calendar class inherits QCalendarWidget
        self.calendar = Calendar(self)
  
        # enabling mouse tracking
        self.calendar.setMouseTracking(True)
        self.setMouseTracking(True)
  
        # setting geometry to the calender
        self.calendar.setGeometry(50, 10, 250, 250)
  
        # setting cursor
        self.calendar.setCursor(Qt.PointingHandCursor)
  
  
    # overriding the mouse move event
    def mouseMoveEvent(self, event):
  
        # getting x, y co-ordinates
        x = event.x()
        y = event.y()
  
        # checking the flag
        if self.move_calendar:
  
            # moving the calendar
            self.calendar.move(x, y)
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())