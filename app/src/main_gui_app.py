import wx
from core.frontends.gui import *


def main_app_gui():
    app = wx.App()
    frame = MainWindow()
    app.MainLoop()


if __name__ == '__main__':
    main_app_gui()
