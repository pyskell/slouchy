# -*- coding: utf-8 -*-
import sys
import time

from PyQt4 import QtGui, QtCore
# from PyQt4.QtCore import QString

from main import main as maybe_slouching

class TrayIcon(QtGui.QSystemTrayIcon):
  def __init__(self, icon, parent=None):
    QtGui.QSystemTrayIcon.__init__(self, icon, parent)

  def alert(self):
    # Alerting by receiving a signal
    self.workThread = SlouchingThread()
    self.connect(self.workThread, QtCore.SIGNAL("slouching_alert(QString, QString)"), 
                 self.showMessage)
    self.workThread.start()

class MyWidget(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
   
    self.setGeometry(300, 300, 280, 600)
    self.setWindowTitle('threads')
    # self.show()

class SlouchingThread(QtCore.QThread):
  def __init__(self):
    QtCore.QThread.__init__(self)

  # Called run but start() should run this...
  def run(self):
    while True:
      # print("In the slouching loop")
      slouching = maybe_slouching()

      if slouching.success:
        self.emit(QtCore.SIGNAL('slouching_alert(QString, QString)'), 
                  "You're slouching", "Stop slouching!")
      else:
        self.emit(QtCore.SIGNAL('slouching_alert(QString, QString)'), 
                  "Error encountered", str(slouching.result))
      
      time.sleep(10)

app = QtGui.QApplication(sys.argv)

w = MyWidget()
tray = TrayIcon(QtGui.QIcon('favicon_32.bmp'), w)

tray.show()
tray.alert()
sys.exit(app.exec_())