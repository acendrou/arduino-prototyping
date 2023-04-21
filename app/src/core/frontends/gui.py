import wx

from core.version import VERSION

SIZE_MAIN_WINDOW_WIDTH = 1920
SIZE_MAIN_WINDOW_HEIGHT = 1080


class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Analysis GUI' + " - " + VERSION,
                         size=(SIZE_MAIN_WINDOW_WIDTH, SIZE_MAIN_WINDOW_HEIGHT))
        # input text for terminal
        self.control = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # STATUS BAR
        self.CreateStatusBar()  # A Statusbar in the bottom of the window
        filemenu = wx.Menu()  # Setting up the menu.
        # wx.ID_ABOUT and wx.ID_EXIT are standard IDs provided by wxWidgets.
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT, "E&xit", " Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")  # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.
        # Set events.
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)

        # TERMINAL OUTPUT
        self.terminal_output = wx.TextCtrl(self, style=wx.TE_MULTILINE)
        self.terminal_output.SetExtraStyle(wx.TE_READONLY)
        #self.terminal_output.SetExtraStyle(wx.TE)
        self.terminal_output.AppendText("test test \n test3")
        self.Show(True)

    def OnAbout(self, e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self,
                               " C3 Command, Control, Console - pretty console output & command and control & see (c) ",
                               'Analysis GUI' + " - " + VERSION, wx.OK)
        dlg.ShowModal()  # Show it
        dlg.Destroy()  # finally destroy it when finished.

    def OnExit(self, e):
        self.Close(True)  # Close the frame.