#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys
import signal
import time

from PyQt4 import QtGui, QtCore

# Local imports
import config
from main import take_picture, determine_posture

# This fixes an UnboundLocalError / referenced before assignment error...
# Directly importing slouching_results doesn't work?
from main import slouching_results as slouching_results_what

# Qt4 threading advice from here: https://joplaete.wordpress.com/2010/07/21/threading-with-pyqt4/

check_frequency = config.poll_rate

# Set initial values to slouchy.ini
def setup():
  maybe_image           = take_picture(config.video_device)
  maybe_current_posture = determine_posture(maybe_image)

  if maybe_current_posture.success:
    distance_reference = str(maybe_current_posture.result.get('distance'))
    config.config_file['MAIN']['distance_reference'] = distance_reference
    print("Reference value detected as:", maybe_current_posture.result)

  else:
    print("Error:", maybe_current_posture.result)
    return maybe_current_posture

  config.config_file.write()


class TrayIcon(QtGui.QSystemTrayIcon):
  def __init__(self, icon, parent=None):
    QtGui.QSystemTrayIcon.__init__(self, icon, parent)
    self.workThread = SlouchingThread()

    menu        = QtGui.QMenu(parent)
    setupAction = menu.addAction("Setup")
    exitAction  = menu.addAction("Quit")
    self.setContextMenu(menu)

    self.connect(exitAction, QtCore.SIGNAL('triggered()'), sys.exit)
    self.connect(setupAction, QtCore.SIGNAL('triggered()'), setup)

  def __del__(self):
    QtGui.QSystemTrayIcon.__del__(self)
    self.workThread.terminate()

  def alert(self):
    # Alerting by receiving a signal
    self.connect(self.workThread, QtCore.SIGNAL("slouching_alert(QString, QString)"),
                 self.showMessage)
    self.workThread.start()

class WrapperWidget(QtGui.QWidget):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)

    self.setGeometry(100, 100, 100, 100)
    self.setWindowTitle('threads')
    # self.show()

class SlouchingThread(QtCore.QThread):
  def __init__(self):
    QtCore.QThread.__init__(self)
    self.run_loop = True

  # Helps ensure that the thread quits before it's destroyed.
  def __del__(self):
    self.wait()

  # I can't get the timing right but I think having this
  # will help kill our while loop in run()
  # This hopefully avoids a race condition where the camera is stuck active
  # if we quit while it's taking a picture.
  # I could be entirely wrong though...
  def terminate(self):
    self.run_loop = False

  # Called run but start() actually runs this
  def run(self):
    while self.run_loop:

      # TODO: Possibly collect a certain number of readings and then only bother people if all or most of the readings indicate slouching. Best 2 out of 3?
      maybe_slouching = slouching_results_what()

      if maybe_slouching.success:
        slouching_results  = maybe_slouching.result
        slouching_messages = str('')

        body_slouching = slouching_results.get('body_slouching')
        head_tilting   = slouching_results.get('head_tilting')

        if body_slouching:
          slouching_messages = slouching_messages + "Your body is slouched!"

        if head_tilting:
          if len(slouching_messages) > 0:
            slouching_messages = slouching_messages + '\n'

          slouching_messages = slouching_messages + "Your head is tilted!"

        if body_slouching or head_tilting:
          self.emit(QtCore.SIGNAL('slouching_alert(QString, QString)'),
                  "Your posture is off!", str(slouching_messages))

      else:
        self.emit(QtCore.SIGNAL('slouching_alert(QString, QString)'),
                  "Error encountered", str(maybe_slouching.result))

      time.sleep(float(check_frequency))

app = QtGui.QApplication(sys.argv)
signal.signal(signal.SIGINT, signal.SIG_DFL) #Force PYQT to handle SIGINT (CTRL+C)

w = WrapperWidget()
tray = TrayIcon(QtGui.QIcon('slouchy_icon.png'), w)

tray.show()
tray.alert()
sys.exit(app.exec_())
