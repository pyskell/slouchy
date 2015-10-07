# import daemon
import threading
import time
import wx
import wx.lib.agw.toasterbox as TB

from wxAnyThread import anythread

from main import main

# from wx import TaskBarIcon

class ToasterFrame(wx.Frame):
  def __init__(self, parent):

    wx.Frame.__init__(self, parent, -1)

    self.toaster = TB.ToasterBox(self, tbstyle=TB.TB_SIMPLE)

    self.toaster.SetPopupPauseTime(5000)
    self.toaster.SetPopupPositionByInt(3)
    self.toaster.SetPopupSize((100, 100))
    self.toaster.SetPopupBackgroundColour(wx.Colour(0,0,0))
    self.toaster.SetPopupTextColour(wx.Colour(255,255,255))
    self.toaster.SetPopupText("You're slouching.")

  @anythread
  def show_popup(self):
    wx.CallLater(1000, self.Show(False)) # Hides the main app window?
    wx.CallLater(1000, self.toaster.Play)
    # wx.CallLater(2000, toaster.CleanList)

def start_thread(func, *args):
    thread = threading.Thread(target=func, args=args)
    thread.setDaemon(True)
    thread.start()

def check_slouching():
  while True:
    slouching = main()

    if slouching:
      alert = ToasterFrame(None)
      alert.show_popup()
      # wx.CallLater(1000, alert.toaster.Play)
      # wx.CallLater(1000, alert.Destroy)
      # wx.CallLater(2000, alert.Destroy)
    
    time.sleep(60)

app = wx.App(0)
icon = wx.TaskBarIcon()
icon.SetIcon(wx.Icon('favicon_32.bmp', type=wx.BITMAP_TYPE_ANY))

# app.SetTopWindow(alert)

start_thread(check_slouching)

app.MainLoop()

# alert.show_popup()
