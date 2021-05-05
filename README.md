# Circuit-Board-Designer

The Circuit Board Designer has been developed to be an easy-to-use tool to develop circuit diagrams efficiently and for those who may be lacking experience. The Circuit Board Designer offers a lot of features, but the most important is it’s simple and easy to understand graphical user interface (GUI) which allows the user to generate their own basic circuit within minutes. The Circuit Board Designer also provides functionality to convert the circuit diagram to a physical component layout that fits optimally on a printable circuit board (PCB). This function allows the user to be able to quickly develop their optimal layout for a compact circuit. This program also has the ability to give the user an image of their optimal PCB layout.

This GitHub repository is organized as follows:

## Documents

This directory includes all of the documents throughout the CSCI 4805 Course. This includes word documents and powerpoints which (some of which are saved as .pdf files) from various milestones of this project.

## examples

This directory is solely used to give the user examples on how to use different parts of the backend program. It is also used for testing purposes by the developers. 

## src

This is the source directory of the entire project.

<ins>color_img</ins>
: Contains all of the different .png files for the color-related buttons on the GUI.

<ins>comp_img</ins>
: Contains all of the different .svg files for the components on the workspace of the GUI.

<ins>img</ins>
: Contains all of the different .png files for the other buttons not included in the color_img folder.

The classes.py file contains all of the class data related to the monte carlo and A* methods for the PCB Optimization

The main.py file contains all of the class data related to the GUI, file management, and the driver function of the program.

# Required Libraries and Installation (Windows Only)
* Install the latest version of Python3 and make sure to include python3 to your PATH
* Install Git and make sure to include git to your PATH
* In cmd run **pip3 install PyQt5**
* In cmd run **pip3 install PySide2**
* In cmd run **pip3 install numpy**
* In cmd run **pip3 install Pillow**
* In cmd run **git clone https://github.com/CinnaKenToast/Circuit-Board-Designer.git**

# Run the Program
Navigate to the src folder in cmd and the run **python3 main.py** in cmd.

# Important Program Controls
![Select](/readmeImg/select.png)

In order to select a component, click on the label of said component. 


## Licenses
The base of the repo contains **license.txt** that contains all required licenses information and credit for any icons used in the program. 
