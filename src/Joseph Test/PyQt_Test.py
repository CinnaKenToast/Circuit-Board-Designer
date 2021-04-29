# pyuic5 –x "filename".ui –o "filename".py   <----- Command to convert .ui file from QtDesigner to .py
# C:\Users\Spear\OneDrive\Desktop\CSCI Capstone\Practice\lib\python3.6 <---- Joseph's python folder location



import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
class window(QWidget): # Class approach to the solution
   def __init__(self, parent = None):
      super(window, self).__init__(parent)
      self.resize(400,100) # Changes size of window
      self.setWindowTitle("PyQt5") # Window Title
      self.label = QLabel(self) 
      self.label.setText("Hello World")
      font = QFont()
      font.setFamily("Arial")
      font.setPointSize(16)
      self.label.setFont(font)
      self.label.move(50,20)
def main():
   app = QApplication(sys.argv)
   ex = window()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()