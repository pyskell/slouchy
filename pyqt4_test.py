# -*- coding: utf-8 -*-

import sys
import time

from PyQt4 import QtGui, QtCore
# from PyQt4.QtCore import QString

from main import main as main_slouching

class MyApp(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
   
    self.setGeometry(300, 300, 280, 600)
    self.setWindowTitle('threads')
   
    # self.layout = QtGui.QVBoxLayout(self)
   
    # self.testButton = QtGui.QPushButton("test")
    # self.connect(self.testButton, QtCore.SIGNAL("released()"), self.test)
    # self.listwidget = QtGui.QListWidget(self)
   
    # self.layout.addWidget(self.testButton)
    # self.layout.addWidget(self.listwidget)

    self.show()
    self.tray = QtGui.QSystemTrayIcon()
    # print("Supports messages:", self.tray.supportsMessages())
    self.tray.setIcon(QtGui.QIcon('favicon_32.bmp'))
    self.tray.show()

  def alert(self):
    # Alerting by receiving a signal
    self.workThread = SlouchingThread()
    self.connect(self.workThread, QtCore.SIGNAL("alert(QString)"), 
                 self.tray.showMessage)
    self.workThread.start()

class SlouchingThread(QtCore.QThread):
  def __init__(self):
    QtCore.QThread.__init__(self)

  # Called run but start() should run this...
  def run(self):
    while True:
      print("In the loop")
      slouching = main_slouching()

      if slouching:
        self.emit(QtCore.SIGNAL('alert(QString)'), "You're slouching", "Stop slouching!")
        # tray.showMessage("You're slouching", "Quit it!")
      
      time.sleep(10)

app = QtGui.QApplication(sys.argv)

test = MyApp()
test.show()
app.exec_()

# check_slouching = SlouchingThread()
# check_slouching.start()


# w = QtGui.QWidget()
# # w.resize(250, 150)
# # w.move(300, 300)
# # w.setWindowTitle('Simple')
# w.show()


# tray = QtGui.QSystemTrayIcon()
# print("Supports messages:", tray.supportsMessages())
# tray.setIcon(QtGui.QIcon('favicon_32.bmp'))
# tray.show()
# tray.showMessage("You're slouching", "Quit it!")
# check_slouching()

# sys.exit(app.exec_())



# if __name__ == '__main__':
#     main()