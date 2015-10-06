import wx
import wx.lib.agw.toasterbox as TB

from wx import TaskBarIcon

class MyBox(TB.ToasterBox):
  pass

class ToasterFrame(wx.Frame):
  def __init__(self, parent):

    wx.Frame.__init__(self, parent, -1)
    toaster = TB.ToasterBox(self, tbstyle=TB.TB_SIMPLE)

    toaster.SetPopupPauseTime(5000)
    toaster.SetPopupPositionByInt(3)
    toaster.SetPopupSize((100, 100))
    toaster.SetPopupText("You're slouching.")

  # def show_popup():
    wx.CallLater(1000, toaster.Play)

app = wx.App(0)
icon = TaskBarIcon()
icon.SetIcon(wx.Icon('favicon_32.bmp', type=wx.BITMAP_TYPE_ANY))

alert = ToasterFrame(None)
app.SetTopWindow(alert)
alert.Show(False) # Hides the main app window?

app.MainLoop()