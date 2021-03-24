from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import argparse

class ScalingWidget (QWidget):
    ''' Displays a pixmap optimally in the center of the widget, in such way
        the pixmap is shown in the middle
    '''
    white   = QColor(255,255,255)
    black   = QColor(  0,  0,  0)
    arcrect = QRect(-10, -10, 20, 20)

    def __init__(self):
        super(ScalingWidget, self).__init__()
        self.pixmap = QPixmap(400, 400)
        painter = QPainter(self.pixmap)
        painter.fillRect(self.pixmap.rect(), self.white)
        self.point1 = QPoint(20, 20)
        self.point2 = QPoint(380, 380)
        painter.setPen(self.black)
        painter.drawRect(QRect(self.point1, self.point2))
        painter.end()
        self.matrix = None

    def sizeHint(self):
        return QSize(500,400)

    ##
    # Applies the default transformations
    #
    def _default_img_transform(self, painter):
        #size of widget
        winheight   = float(self.height())
        winwidth    = float(self.width())
        #size of pixmap
        scrwidth    = float(self.pixmap.width())
        scrheight   = float(self.pixmap.height())
        assert(painter.transform().isIdentity())

        if scrheight <= 0 or scrwidth <= 0:
            raise RuntimeError(repr(self) + "Unable to determine Screensize")

        widthr  = winwidth / scrwidth
        heightr = winheight / scrheight

        if widthr > heightr:
            translate = (winwidth - heightr * scrwidth) /2
            painter.translate(translate, 0)
            painter.scale(heightr, heightr)
        else:
            translate = (winheight - widthr * scrheight) / 2
            painter.translate(0, translate)
            painter.scale(widthr, widthr)

        # now store the matrix used to map the mouse coordinates back to the 
        # coordinates of the pixmap
        self.matrix = painter.transform()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setClipRegion(e.region())

        # fill the background of the entire widget.
        painter.fillRect(self.rect(), QColor(0,0,0))

        # transform to place the image nicely in the center of the widget.
        self._default_img_transform(painter)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap, self.pixmap.rect())
        pen = QPen(QColor(255,0,0))

        # Just draw on the points used to make the black rectangle of the pix map
        # drawing is not affected, be remapping those coordinates with the "same"
        # matrix is.
        pen.setWidth(4)
        painter.setPen(pen)
        painter.save()
        painter.translate(self.point1)
        painter.drawPoint(0,0)
        painter.restore()
        painter.save()
        painter.translate(self.point2)
        painter.drawPoint(0,0)
        painter.restore()

        painter.end()

    def mouseReleaseEvent(self, event):
        x, y = float(event.x()), float(event.y())
        inverted, invsucces = self.matrix.inverted()
        assert(invsucces)
        xmapped, ymapped = inverted.map(x,y)
        print (x, y)
        print (xmapped, ymapped)
        self.setWindowTitle("mouse x,y = {}, {}, mapped x, y = {},{} "
                                .format(x, y, xmapped, ymapped)
                            )


def start_bug():
    ''' Displays the mouse press mapping bug.
        This is a bit contrived, but in the real world
        a widget is embedded in deeper in a gui
        than a single widget, besides the problem
        grows with the depth of embedding.
    '''
    app = QApplication(sys.argv)
    win     = QWidget()
    layout  = QVBoxLayout()
    win.setLayout(layout)
    widget = None
    for i in range(0, args.increase_bug):
        if i < args.increase_bug-1:
            widget = QWidget()
            layout.addWidget(widget)
            layout= QVBoxLayout()
            widget.setLayout(layout)
        else:
            layout.addWidget(ScalingWidget())
    win.show()
    sys.exit(app.exec_())

def start_no_bug():
    ''' Does not show the mapping bug, the mouse event.x() and .y() map nicely back to
        the coordinate system of the pixmap
    '''
    app = QApplication(sys.argv)
    win = ScalingWidget()
    win.show()
    sys.exit(app.exec_())

# parsing arguments
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('-b', '--display-bug', action='store_true',
                    help="Toggle this option to get the bugged version"
                    )
parser.add_argument('-n', '--increase-bug', type=int, default=1,
                    help="Increase the bug by n times."
                    )

if __name__ == "__main__":
    args = parser.parse_args()
    if args.display_bug:
        start_bug()
    else:
        start_no_bug()