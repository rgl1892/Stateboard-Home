import requests
import pandas as pd
import wx
import numpy as np
import math


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

# for j in df:
#     for i in range(len(df)):
#         exec("col{}.append(df[j][i])".format(j))

for j in df:
    for i in range(len(df)):
        if df[j][i] != df[j][i]:
            exec("col{}.append('N/A')".format(j))
        else:
            exec("col{}.append(df[j][i])".format(j))        

for i in range(len(df)):
    exec("row{} =[]".format(i))

for i in range(len(df)):
    for j in df:
        if not(isinstance(df[j][i],str)) and not(isinstance(df[j][i],np.float64)):
            exec("row{}.append('N/A')".format(i))
        elif isinstance(df[j][i],np.float64):
            exec("row{}.append(str(df[j][i]))".format(i))
        else:
            exec("row{}.append(df[j][i])".format(i))

mincol1 = []
mincol2 = []

# for line in col2:
    # print(type(line))

# print(col1[1393])


class TabOne(wx.Panel):
    
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        self.grid = wx.GridBagSizer(10,10)
        
        self.RevList = wx.ListBox(self, -1)
        self.RevList.Bind(wx.EVT_LISTBOX, self.onRevListSelect)

        self.AerodromeList = wx.ListBox(self, -1)
        self.AerodromeList.Bind(wx.EVT_LISTBOX, self.onAerodromeSelect)          

        self.CheckList = wx.ListBox(self, -1)
        self.CheckList.Bind(wx.EVT_LISTBOX, self.onCheckListSelect)
        
        minimaButtonPanel = wx.Panel(self,-1)
        mBox = wx.BoxSizer(wx.VERTICAL)
        self.mbp = wx.ComboBox(minimaButtonPanel, choices=['True','False','All'], style=wx.CB_READONLY)
        self.mbpLabel = wx.StaticText(minimaButtonPanel, label='Show Minima needed', style=wx.ALIGN_CENTER)
        mBox.Add(self.mbpLabel, 0, wx.TOP,5)
        mBox.Add(self.mbp, 0, wx.TOP, 5)
        mBox.AddStretchSpacer()

        self.mbp.Bind(wx.EVT_COMBOBOX,self.onCombo)

        minimaButtonPanel.SetSizer(mBox)

        rev = 0
        for rev in range(52):
            self.RevList.Append(str(rev+1))

        self.grid.Add(self.AerodromeList, (0,1), (10,0), wx.EXPAND, 5)
        self.grid.Add(self.CheckList, (0,2), (10,0), wx.EXPAND, 5)
        self.grid.Add(self.RevList, (0,0), (10,0), wx.EXPAND, 5)
        self.grid.Add(minimaButtonPanel, (0,3), (0,0), wx.EXPAND, 5)

        self.SetSizerAndFit(self.grid)
        self.Center()
        self.Show(True)

        #default is to show all aerodromes not just minimaa
        self.test = 'All'

    def onCombo(self,event):
        if self.mbp.GetValue() == 'True':
            mincol1 = []
            mincol2 = []
            self.test = True
            occurences = ([k for k , j in enumerate(col15) if j == True])
            
            for row in occurences:
                print(row)
                mincol1.append(col1[row])
                mincol2.append(col2[row])
            print(mincol1)
            
        elif self.mbp.GetValue() == 'False':
            self.test = False
        else:
            self.test = 'All'
            
        
    def onRevListSelect(self,event):
        self.AerodromeList.Clear()
        self.CheckList.Clear()
        sel = self.RevList.GetSelection()
        print(sel)
        self.rev = sel + 1.0
        self.occurences = ([k for k , j in enumerate(col2) if j == self.rev])
        for pos in self.occurences:
            self.AerodromeList.Append(mincol1[pos])
        # print(self.occurences)
        self.SetSizerAndFit(self.grid)

    def onAerodromeSelect(self,event):
        sel = self.AerodromeList.GetSelection()
        name = self.AerodromeList.GetString(sel)      
        location = ([k for k , j in enumerate(mincol1) if j == name])
        self.CheckList.Clear()
        if self.test == True:
            print('hi')
        elif self.test == False:
            print('no')
        else:
            print('winner winner')

        for line in self.occurences:
            if float(eval("row{}[2]".format(line))) == self.rev and line in location:
                row = eval("row{}".format(line))
                for data in row:
                    if data == 'N/A' or data == 'nan':
                        continue
                    else:
                        self.CheckList.Append(data)
            else:
                continue
        self.SetSizerAndFit(self.grid)


    def onCheckListSelect(self,event):
        sel = self.CheckList.GetSelection()
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