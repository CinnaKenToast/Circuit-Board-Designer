import pyqtgraph as pg
app = pg.QtGui.QApplication([])

l = pg.QtGui.QListWidget()
l.addItem('Drag me')
l.setDragDropMode(l.DragOnly)
l.show()

win = pg.GraphicsWindow()
win.show()

def dragEnterEvent(ev):
    ev.accept()

win.dragEnterEvent = dragEnterEvent

plot = pg.PlotItem()
plot.setAcceptDrops(True)
win.addItem(plot)

def dropEvent(event):
    print ("Got drop!")

plot.dropEvent = dropEvent