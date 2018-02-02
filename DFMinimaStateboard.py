import requests
import pandas as pd
import wx


url = 'http://newt.ykf.navtech.corp/cgi-bin/mks_query.cgi?Query=Chart%20Orders%20Last%203%20months%20Minima&ColumnSet=default'
html = requests.get(url).content
df_list = pd.read_html(html)
df = df_list[-1]

"""
col index 
0 = mks
1 = Aerodrome + Aerodrome name (need to split)
2 = Revision
"""


for i in range(len(df)):
    exec("col{} =[]".format(i))

for j in df:
    for i in range(len(df)):
        exec("col{}.append(df[j][i])".format(j))

for i in range(len(df)):
    exec("row{} =[]".format(i))

for i in range(len(df)):
    for j in df:
        exec("row{}.append(df[j][i])".format(i))

print(row1)

print(len(col1))
print(len(df))


class TabOne(wx.Panel):
    
    def __init__(self,parent):
        # updateClourDB()
        wx.Panel.__init__(self,parent)
        grid = wx.GridBagSizer(10,10)


        self.AerodromeList = wx.ListBox(self, -1)
        self.AerodromeList.Bind(wx.EVT_LISTBOX, self.onAerodromeSelect)

        i =0
        while i < 2209:
            self.AerodromeList.Append(col1[i])
            i +=1
            # print(i)
            

        self.RevList = wx.ListBox(self, -1)
        self.RevList.Bind(wx.EVT_LISTBOX, self.onRevisionSelect)

        grid.Add(self.AerodromeList, (0,0), (10,0), wx.EXPAND,5)
        grid.Add(self.RevList, (0,1), (10,0), wx.EXPAND,5)

        self.SetSizerAndFit(grid)
        self.Center()
        self.Show(True)

    def onAerodromeSelect(self,event):
        sel = self.AerodromeList.GetSelection()
        self.RevList.Clear()
        print(sel)
        for data in  

        

    def onRevisionSelect():
        sel = self.RevList.GetSelection()
        print(sel)

class MainFrame(wx.Frame):

    def __init__(self):

        wx.Frame.__init__(self, None, title='Minima Stateboard', size = (1280,800))

        p = wx.Panel(self)
        nb = wx.Notebook(p)

        self.tab1 = TabOne(nb)

        nb.AddPage(self.tab1,'Aerodromes')

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)

        #menu
        menuBar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()

        refreshMenuButton = fileMenu.Append(wx.ID_ANY, 'Refresh', 'Refresh App')
        quitMenuButton = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')

        self.showStatus = viewMenu.Append(wx.ID_ANY, 'Show Statusbar', 'Show Statusbar', kind=wx.ITEM_CHECK)
        viewMenu.Check(self.showStatus.GetId(), True)
		
        menuBar.Append(fileMenu, '&File')		
        menuBar.Append(viewMenu, '&View')
        self.SetMenuBar(menuBar)
		
        self.Bind(wx.EVT_MENU, self.onQuit, quitMenuButton)
        self.Bind(wx.EVT_MENU, self.toggleStatusBar, self.showStatus)
		
        self.statusBar = self.CreateStatusBar()
        self.statusBar.SetStatusText('Ready')

        self.Bind(wx.EVT_CLOSE, self.onQuit)

    def onQuit(self, event):
        dlg = wx.MessageDialog(None, 'Do you want to save and overwrite changes?', 'Warning', wx.YES_NO| wx.CANCEL | wx.ICON_QUESTION)
        result = dlg.ShowModal()
        self.Destroy()

    def toggleStatusBar(self, e):
	
        if self.showStatus.IsChecked():
            self.statusBar.Show()
        else:
            self.statusBar.Hide()

if __name__ == '__main__':
    app = wx.App()
    MainFrame().Show()
    app.MainLoop()