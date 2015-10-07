# import daemon
import threading
import time
import wx
import wx.lib.agw.toasterbox as TB

from main import main

# from wx import TaskBarIcon

class ToasterFrame(wx.Frame):
  def __init__(self, parent):

    wx.Frame.__init__(self, parent, -1)

    toaster = TB.ToasterBox(self, tbstyle=TB.TB_SIMPLE)

    toaster.SetPopupPauseTime(5000)
    toaster.SetPopupPositionByInt(3)
    toaster.SetPopupSize((100, 100))
    toaster.SetPopupText("You're slouching.")

    wx.CallLater(1000, toaster.Play)

def start_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()

def check_slouching():

  while True:
    slouching = main()

    if slouching:
      alert = ToasterFrame(None)
      app.SetTopWindow(alert)
      wx.CallLater(100, alert.Show(False)) # Hides the main app window?
      # wx.CallLater(1000, alert.Destroy)
      # wx.CallLater(2000, alert.Destroy)
    
    time.sleep(10)

app = wx.App(0)
icon = wx.TaskBarIcon()
icon.SetIcon(wx.Icon('favicon_32.bmp', type=wx.BITMAP_TYPE_ANY))

start_thread(check_slouching)

app.MainLoop()

# alert.show_popup()
