import sys
import platform
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PySide2.QtWidgets import *

# GUI FILE
from ui_test import Ui_MainWindow

# IMPORT FUNCTIONS
# from ui_functions import *

class MainWindow(QMainWindow):
        def __init__(self):
                QMainWindow.__init__(self)
                self.ui = Ui_MainWindow()
                self.ui.setupUi(self)
                self.menuStates = ["Closed", "menuComponents", "menuColors"]
                self.currentState = self.menuStates[0]
                

                # self.ui.btn_toggle.clicked.connect(lambda: uiFunctions.toggleMenu(self, 200, True))
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

                self.show()

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

                #print("End:", button, "|", self.currentState)
                #print("-------------------------")

                #currentPage = self.ui.stacked_tools.currentWidget().accessibleName()
                #print(button, "|", currentPage)
                '''
                if(button == "btn_add" and currentPage == "page_colors"):
                enable = True
                elif(button == "btn_colors" and currentPage == "page_components"):
                enable = True
                '''


                if enable:
                        width = self.ui.frame_tools.width()
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
                        self.animation = QPropertyAnimation(self.ui.frame_tools, b"minimumWidth")
                        self.animation.setDuration(150)
                        self.animation.setStartValue(width)
                        self.animation.setEndValue(widthExtended)
                        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
                        self.animation.start()
                        # print(self.ui.stacked_tools.currentWidget().accessibleName())
            

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = MainWindow()
        sys.exit(app.exec_())