import time
import wx
import wx.lib.agw.toasterbox as TB

from wxAnyThread import anythread

from main import main


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
    wx.CallAfter(self.Show, False) # Hides the main app window?
    wx.CallAfter(self.toaster.Play)

def check_slouching(alert):
  while True:
    slouching = main()

    if slouching:
      alert.show_popup()
    
    time.sleep(10)

app = wx.App(0)
icon = wx.TaskBarIcon()
icon.SetIcon(wx.Icon('favicon_32.bmp', type=wx.BITMAP_TYPE_ANY))

alert = ToasterFrame(None)
alert.Show(False)
app.SetTopWindow(alert)

wx.CallAfter(check_slouching, alert)

app.MainLoop()

