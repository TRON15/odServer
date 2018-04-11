import sys
from ask_for_frame import *
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QPoint, QRect, QSize, Qt
from PyQt4.QtGui import QRubberBand
import time
from PIL import Image, ImageDraw
# function to process frame
def updateframe(path):
    im = Image.open(path)
    draw = ImageDraw.Draw(im)
    if (redLTx.text() and redLTy.text() and redRBx.text() and redRBy.text()):
        draw.rectangle( [(float(redLTx.text()), float(redLTy.text())), (float(redRBx.text()), float(redRBy.text()))], fill = None, outline = (255, 000, 000))
    if (blackLTx.text() and blackLTy.text() and blackRBx.text() and blackRBy.text()):
        draw.rectangle([(float(blackLTx.text()), float(blackLTy.text())), (float(blackRBx.text()), float(blackRBy.text()))], fill = None, outline = (255, 255, 000))
    del draw
    im.save('/tmp/tmp_frame.png', 'PNG')
    return '/tmp/tmp_frame.png'

# frame class to display frame
class frame(QtGui.QLabel):

    def __init__(self, parent = None):
    
        QtGui.QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
    
    def mousePressEvent(self, event):
    
        if event.button() == Qt.LeftButton:
            global LTx, LTy
            [LTx, LTy] = [event.pos().x(), event.pos().y()]
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()
    
    def mouseMoveEvent(self, event):
    
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
    
        if event.button() == Qt.LeftButton:
            global RBx, RBy
            [RBx, RBy] =  [event.pos().x(), event.pos().y()]
            self.rubberBand.hide()

# main class to display the whole GUI
class Example(QtGui.QMainWindow):
    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
    
        # basic settings
        wid = QtGui.QWidget(self)
        self.setCentralWidget(wid) 
        self.statusBar()

        # buttons
        redButton = QtGui.QPushButton('&Red')
        clearRedButton = QtGui.QPushButton('Clear red') 
        blackButton = QtGui.QPushButton('&Black')
        clearBlackButton = QtGui.QPushButton('Clear black')
        saveButton = QtGui.QPushButton('&Save')
        quitButton = QtGui.QPushButton('&Quit')
        refreshButton = QtGui.QPushButton('Refresh(F5)')

        # display pos info
        global redLTx, redLTy, redRBx, redRBy, blackLTx, blackLTy, blackRBx, blackRBy
        redText = QtGui.QLabel('Red Block:')
        blackText = QtGui.QLabel('Black Block:')
        redLTx = QtGui.QLineEdit()
        redLTy = QtGui.QLineEdit()
        redRBx = QtGui.QLineEdit()
        redRBy = QtGui.QLineEdit()
        blackLTx = QtGui.QLineEdit()
        blackLTy = QtGui.QLineEdit()
        blackRBx = QtGui.QLineEdit()
        blackRBy = QtGui.QLineEdit()

        # QlineEdit connect to the display of the frame
        redLTx.returnPressed.connect(self.change_by_hand)
        redLTy.returnPressed.connect(self.change_by_hand)
        redRBx.returnPressed.connect(self.change_by_hand)
        redRBy.returnPressed.connect(self.change_by_hand)
        blackLTx.returnPressed.connect(self.change_by_hand)
        blackLTy.returnPressed.connect(self.change_by_hand)
        blackRBx.returnPressed.connect(self.change_by_hand)
        blackRBy.returnPressed.connect(self.change_by_hand)

        # botton connect to their functions
        redButton.clicked.connect(self.chooseRed)
        blackButton.clicked.connect(self.chooseBlack)
        clearRedButton.clicked.connect(self.clearRed)
        clearBlackButton.clicked.connect(self.clearBlack)
        saveButton.clicked.connect(self.save)
        quitButton.clicked.connect(self.close)
        refreshButton.clicked.connect(self.refresh)

        # set the shortcut of the buttons
        redButton.setShortcut('Ctrl+R')
        blackButton.setShortcut('Ctrl+B')
        saveButton.setShortcut('Ctrl+S')
        quitButton.setShortcut('Ctrl+Q')
        refreshButton.setShortcut('F5')

        # load the welcome GUI
        global pixmap
        pixmap = QtGui.QPixmap('welcome.png')
        im = Image.open('welcome.png')
        im.save('/tmp/processing_copy.png', 'PNG')

        # settings of the frame class
        global lbl
        lbl = frame(self)
        lbl.setPixmap(pixmap)
        lbl.rubberband = QtGui.QRubberBand(QtGui.QRubberBand.Rectangle, lbl)
        lbl.setMouseTracking(True)
        
        # settings of the grid layout
        grid = QtGui.QGridLayout()
        grid.setSpacing(10)        
        spaceNum = 2
        grid.addWidget(lbl, 1, 0, 8+2*spaceNum, 1)
        grid.addWidget(refreshButton, 9+2*spaceNum, 0)
        grid.addWidget(redText, 1, 2)
        grid.addWidget(redLTx, 2, 2)
        grid.addWidget(QtGui.QLabel(','), 2, 3)
        grid.addWidget(redLTy, 2, 4)
        grid.addWidget(redRBx, 3, 2)
        grid.addWidget(QtGui.QLabel(','), 3, 3)
        grid.addWidget(redRBy, 3, 4)
        # boring settings ,jump it
        for i in range(0, spaceNum):
            grid.addWidget(QtGui.QLabel(' '), 4+i, 2)
        grid.addWidget(blackText, 4+spaceNum, 2)
        grid.addWidget(blackLTx, 5+spaceNum, 2)
        grid.addWidget(QtGui.QLabel(','), 5+spaceNum, 3)
        grid.addWidget(blackLTy, 5+spaceNum, 4)
        grid.addWidget(blackRBx, 6+spaceNum, 2)
        grid.addWidget(QtGui.QLabel(','), 6+spaceNum, 3)
        grid.addWidget(blackRBy, 6+spaceNum, 4)
        # boring settings ,jump it
        for i in range(0, spaceNum):
            grid.addWidget(QtGui.QLabel(' '), spaceNum+7+i, 2)
        grid.addWidget(redButton, 7+2*spaceNum, 2)
        grid.addWidget(blackButton,7+2*spaceNum, 4)
        grid.addWidget(clearRedButton,8+2*spaceNum, 2)
        grid.addWidget(clearBlackButton,8+2*spaceNum, 4)
        grid.addWidget(saveButton, 9+2*spaceNum, 2)
        grid.addWidget(quitButton, 9+2*spaceNum, 4)
        
        # show the grid layout
        wid.setLayout(grid)
        self.center()
        self.setWindowTitle('set_blocks')
        self.show()

    # refresh function after changes on the frame in processing
    def change_by_hand(self):
        # just reload the copy of the frame in processing according to the pos info now
        path = updateframe('/tmp/processing_copy.png')
        self.refresh(path)

    # function of buttons
    def chooseRed(self):
        global redLTx, redLTy, redRBx, redRBy
        redLTx. setText(str(LTx))
        redLTy. setText(str(LTy))
        redRBx. setText(str(RBx))
        redRBy. setText(str(RBy))
        self.change_by_hand()
        self.statusBar().showMessage(u'Red block info has been filled!')

    def chooseBlack(self):
        global blackLTx, blackLTy, blackRBx, blackRBy
        blackLTx. setText(str(LTx))
        blackLTy. setText(str(LTy))
        blackRBx. setText(str(RBx))
        blackRBy. setText(str(RBy))
        self.change_by_hand()
        self.statusBar().showMessage(u'black block info has been filled!')

    def clearRed(self):
        redLTx.clear()
        redLTy.clear()
        redRBx.clear()
        redRBy.clear()
        self.change_by_hand()
        self.statusBar().showMessage(u'Red block info has been cleared!')

    def clearBlack(self):
        blackLTx.clear()
        blackLTy.clear()
        blackRBx.clear()
        blackRBy.clear()
        self.change_by_hand()
        self.statusBar().showMessage(u'Black block info has been cleared!')

    def save(self):
        save_msg = 'Are sure to upload this:\nred: ({_redLTx}, {_redLTy}) ({_redRBx}, {_redRBy})\nblack: ({_blackLTx}, {_blackLTy}) ({_blackRBx}, {_blackRBy})'
        save_msg = save_msg.format(_redLTx = redLTx.text(), _redLTy = redLTy.text(), _redRBx = redRBx.text(), _redRBy = redRBy.text(), _blackLTx = blackLTx.text(), _blackLTy = blackLTy.text(), _blackRBx = blackRBx.text(), _blackRBy = blackRBy.text())
        reply = QtGui.QMessageBox.question(self, 'Message', save_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            redBlock = [[int(redLTx.text()), int(redLTy.text())], [int(redRBx.text()), int(redRBy.text())]]
            blackBlock = [[int(blackLTx.text()), int(blackLTy.text())], [int(blackRBx.text()), int(blackRBy.text())]]
            print('red', redBlock)
            upload_result = upload_block_info(redBlock, blackBlock)
            print(upload_result)
            print([[int(redLTx.text()), int(redLTy.text())], [int(redRBx.text()), int(redRBy.text())]])
            print([[int(blackLTx.text()), int(blackLTy.text())], [int(blackRBx.text()), int(blackRBy.text())]])
            self.statusBar().showMessage(u'All info has been saved!')
        else:
            pass

    def refresh(self, path=None):
        global lbl
        if (not path):
            self.clearBlack()
            self.clearRed()
            # refresh frame.png
            refresh_frame()
            # reload it
            lbl.setPixmap(QtGui.QPixmap('/tmp/frame.png'))
            im = Image.open('/tmp/frame.png')
            im.save('/tmp/processing_copy.png', 'PNG')
            self.statusBar().showMessage(u'This is a new frame!')
        else:
            lbl.setPixmap(QtGui.QPixmap(path))
        self.update()
        
    # set the GUI to display in the center of the screen
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    # override the close function
    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QtGui.QMessageBox.question(self, 'Message', quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            close_flag = close_cap()
            print(close_flag)  
            event.accept()
        else:
            event.ignore()
        

def main():
    # open cap
    open_flag =  open_cap()
    print(open_flag)
    # show the GUI
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    

