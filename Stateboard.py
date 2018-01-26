#!/usr/bin/python

import csv
import wx
import win32api
from wx.lib.colourdb import updateColourDB
import matplotlib
import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
matplotlib.use('WXAgg')

userArray = []
userHeaderArray = []
chartArray = []
chartHeaderArray = []

ID_NEW = 1
ID_RENAME = 2
ID_CLEAR = 3
ID_DELETE = 4
ID_CHECK = 5
ID_SAVE = 6

ID_EDIT = 7

ID_COMBO = 8

ID_REFRESH = 9
ID_EXIT = 10

ID_CHARTS = 11

ID_CUR = 12

# A nice Colour scheme


with open('users.csv', 'rt', encoding = 'utf8') as f:  # read in users and their info from .csv
	rowNum = 0
	reader = csv.reader(f)
	for row in reader:
		if rowNum >= 1:
			userArray.append(row)
		else:
			for header in row:
				userHeaderArray.append(header)
		rowNum += 1

with open('charts.csv', 'rt', encoding='utf8') as c:
	rowNum = 0
	reader2 = csv.reader(c)
	for row in reader2:
		if rowNum >= 1:
			chartArray.append(row)
		else:
			for header in row:
				chartHeaderArray.append(header)
		rowNum += 1

for row in userArray:
	row[:] = ["N/A" if cell.strip() == "" else cell for cell in row]  # using list comprehension and ternary operator (a?b:c i.e. b if a is true, else c)
	
for row in chartArray:
	row[:] = ["N/A" if cell.strip() == "" else cell for cell in row]


class TabOne(wx.Panel):
	
	def __init__(self, parent):
		updateColourDB()
		# panel with grid
		wx.Panel.__init__(self, parent)
		grid = wx.GridBagSizer(10,10)
		
		# left listbox
		self.userList = wx.ListBox(self, -1)
		self.userList.Bind(wx.EVT_LISTBOX, self.onUserSelect)
		for row in userArray:
			self.userList.Append(row[0])
		
		# right listbox
		self.userDetails = wx.ListBox(self, -1)
		self.userDetails.Bind(wx.EVT_LISTBOX, self.onDetailSelect)

		# buttons that do various things on lists
		mainbtnPanel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.new = wx.Button(mainbtnPanel, ID_NEW, 'New', size=(90, 30))
		self.ren = wx.Button(mainbtnPanel, ID_RENAME, 'Rename', size=(90, 30))
		self.dlt = wx.Button(mainbtnPanel, ID_DELETE, 'Delete', size=(90, 30))
		self.clr = wx.Button(mainbtnPanel, ID_CLEAR, 'Clear', size=(90, 30))
		self.sve = wx.Button(mainbtnPanel, ID_SAVE, 'Save', size=(90, 30))
		
		self.Bind(wx.EVT_BUTTON, self.newItem, id=ID_NEW)
		self.Bind(wx.EVT_BUTTON, self.onRename, id=ID_RENAME)
		self.Bind(wx.EVT_BUTTON, self.onDelete, id=ID_DELETE)
		self.Bind(wx.EVT_BUTTON, self.onClear, id=ID_CLEAR)
		self.Bind(wx.EVT_BUTTON, self.onSave, id=ID_SAVE)
		self.Bind(wx.EVT_LISTBOX_DCLICK, self.onRename)
		
		self.btnPad = 0
		vbox.Add((-1, 0))
		vbox.Add(self.new, 1, wx.TOP, self.btnPad)
		vbox.Add(self.ren, 1, wx.TOP, self.btnPad)
		vbox.Add(self.dlt, 1, wx.TOP, self.btnPad)
		vbox.Add(self.clr, 1, wx.TOP, self.btnPad)
		vbox.Add(self.sve, 1, wx.TOP, self.btnPad)
		
		mainbtnPanel.SetSizer(vbox)
		
		# buttons underneath right listbox (edit etc)
		detailsbtnPanel = wx.Panel(self, -1)
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		self.edt = wx.Button(detailsbtnPanel, ID_EDIT, 'Edit', size=(90,30))
		
		self.Bind(wx.EVT_BUTTON, self.onEdit, id=ID_EDIT)
		
		hbox.Add(self.edt, 1, wx.TOP, 5)
		
		detailsbtnPanel.SetSizer(hbox)
	
		# True/False combobox
		comboboxPanel = wx.Panel(self, -1)
		cbox = wx.BoxSizer(wx.VERTICAL)
		self.tfc = wx.ComboBox(comboboxPanel, choices=['TRUE', 'FALSE'], style=wx.CB_READONLY)
		self.tfcLabel = wx.StaticText(comboboxPanel, label='Change permission:', style=wx.ALIGN_CENTRE)
		cbox.Add(self.tfcLabel, 0, wx.TOP, 5)
		cbox.Add(self.tfc, 0, wx.TOP, 5)
		cbox.AddStretchSpacer()
		
		self.tfc.Bind(wx.EVT_COMBOBOX, self.onCombo)
		
		comboboxPanel.SetSizer(cbox)
		
		grid.Add(mainbtnPanel, (0,2), (0,0), wx.EXPAND, 5)
		grid.Add(comboboxPanel, (0,3), (0,0), wx.EXPAND, 5)
		grid.Add(detailsbtnPanel, (1,2), (0,0), wx.EXPAND, 5)
		grid.Add(self.userList, (0,0), (10,0), wx.EXPAND, 5)
		grid.Add(self.userDetails, (0,1), (2,0), wx.EXPAND, 5)
		
		self.SetSizerAndFit(grid)
		self.Centre()
		self.Show(True)
		
	def deselect(self):
	
		self.userList.SetSelection(-1)
		self.userDetails.SetSelection(-1)
		self.userDetails.Clear()
		self.edt.Hide()
		self.tfc.Hide()
		self.tfcLabel.Hide()
		
	def refreshDetails(self):
	
		sel = self.userList.GetSelection()
		self.userDetails.Clear()
		n = 0
		for item in userArray[sel]:
			header = userHeaderArray[n]
			self.userDetails.Append('{}{}'.format(header, item))
			n += 1
	
	def newItem(self, event):
	
		text = wx.GetTextFromUser('Enter a name', 'Insert dialog')
		text2 = wx.GetTextFromUser('Enter a user name', 'Insert dialog')
		if text.strip() != '' and text2.strip != '':
			self.userDetails.Clear()
			self.userList.Append(text.strip())
			self.deselect()
			userArray.append([text.strip(), text2, 'N/A', 'N/A','N/A','N/A','N/A','N/A','N/A','N/A'])
			# print(userArray)

	def onRename(self, event):
	
		sel = self.userList.GetSelection()
		text = self.userList.GetString(sel)
		renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
		while True:
			if renamed.strip() != '':
				self.userList.Delete(sel)
				self.userList.Insert(renamed.strip(), sel)
				userArray[sel][0] = renamed.strip()
				self.userList.SetSelection(sel)
				self.refreshDetails()
				# print(userArray)
				break
			else:
				win32api.MessageBox(0, 'Please enter valid name (non-empty)', 'Error')
				renamed = wx.GetTextFromUser('Rename item', 'Rename dialog', text)

	def onDelete(self, event):
	
		sel = self.userList.GetSelection()
		if sel != -1:
			self.userList.Delete(sel)
			del userArray[sel]
			self.deselect()
			# print(userArray)
			
	def onClear(self, event):
	
		dlg = wx.MessageDialog(None, 'This will delete all entries. Are you sure?', 'Warning', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			self.userList.Clear()
			self.deselect()
			del userArray[:]
			# print(userArray)
	
	def onSave(self, event):

		self.deselect()
		dlg = wx.MessageDialog(None, 'Are you sure you want to save and overwrite changes?', 'Warning', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			with open('userscopy.csv', 'w', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(userHeaderArray)
				writer.writerows(userArray)
			with open('chartscopy.csv', 'w', newline='') as c:
				writer = csv.writer(c)
				writer.writerow(chartHeaderArray)
				writer.writerows(chartArray)
	
	def onUserSelect(self, event):
		
		sel = self.userList.GetSelection()
		print(sel)
		self.userDetails.Clear()
		n = 0
		for item in userArray[sel]:
			header = userHeaderArray[n]
			self.userDetails.Append('{}{}'.format(header, item))
			n += 1
		
	def onDetailSelect(self, event):
		sel = self.userDetails.GetSelection()
		print(sel)
		if sel == 0:
			self.edt.Hide()
			self.tfcLabel.Hide()
			self.tfc.Hide()
		elif sel == 1:
			self.edt.Show()
			self.tfcLabel.Hide()
			self.tfc.Hide()
		elif sel >= 2:
			self.tfcLabel.Show()
			self.tfc.Show()
			self.edt.Hide()
	
	def onEdit(self, event):
		
		userSel = self.userList.GetSelection()
		itemSel = self.userDetails.GetSelection()
		text = self.userDetails.GetString(itemSel)
		text = text.split(":")[-1].strip()
		edited = wx.GetTextFromUser('Edit Item', 'Edit dialog', text)
		while True:
			if edited != '':
				userArray[userSel][itemSel] = edited
				self.refreshDetails()
				break
			else:
				win32api.MessageBox(0, 'Please enter valid name (non-empty)', 'Error')
				edited = wx.GetTextFromUser('Rename item', 'Rename dialog', text)
	
	def onCombo(self, event):
	
		userSel = self.userList.GetSelection()
		itemSel = self.userDetails.GetSelection()
		choice = self.tfc.GetValue()
		
		userArray[userSel][itemSel] = choice
		self.refreshDetails()

		
class TabTwo(wx.Panel):

	def __init__(self, parent):
	
		wx.Panel.__init__(self, parent)
		
		grid = wx.GridBagSizer(10,10)
		
		# 'Checks required' label
		self.t = wx.StaticText(self, -1, 'Checks required: ', (20, 20))
		font = wx.Font(20, wx.SWISS, wx.ITALIC, wx.BOLD)
		self.t.SetFont(font)
		self.t.SetForegroundColour((137, 218, 89))
		
		# ListCtrl of charts
		self.chartCtrl = wx.ListCtrl(self, size=(-1, 100), style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.BORDER_SUNKEN)
		
		i = 0
		for header in chartHeaderArray:
			self.chartCtrl.InsertColumn(i, str(header), width=80)
			i += 1
		
		index = 0
		for chart in chartArray:
			self.chartCtrl.InsertItem(index, str(chart[0]))
			
			noOfCols = self.chartCtrl.GetColumnCount()
			print(noOfCols)
			currentColumn = 0
			while currentColumn < noOfCols:
				self.chartCtrl.SetItem(index, currentColumn, chart[currentColumn])
				if chart[noOfCols-1] == 'TRUE':
					self.chartCtrl.SetItemBackgroundColour(index, (128, 189, 158))
				currentColumn += 1
			index += 1

		# Check button
		chartbtnPanel = wx.Panel(self, -1)
		self.chk = wx.Button(chartbtnPanel, ID_CHECK, 'Check', size=(90, 30))
		self.Bind(wx.EVT_BUTTON, self.onCheck, id=ID_CHECK)
		
		grid.Add(self.t, (0,0), (0,0), wx.EXPAND, 5)
		grid.Add(self.chartCtrl, (1,0), (11,11), wx.EXPAND, 20)
		grid.Add(chartbtnPanel, (12,0), (0,0), wx.EXPAND, 5)

		self.SetSizerAndFit(grid)
		self.Centre()
		self.Show(True)
	
	def onUserSelect(self, event):
		
		sel = self.chartList.GetSelection()
		print(sel)
		self.chartDetails.Clear()
		n = 0
		for item in chartArray[sel]:
			header = chartHeaderArray[n]
			self.chartDetails.Append('{}{}'.format(header, item))
			n += 1
			
	def refreshChartDetails(self):
	
		sel = self.chartCtrl.GetFocusedItem()
		n = 0
		for item in chartArray[sel]:
			self.chartCtrl.SetItem(sel, 10, item)
			if item == 'TRUE':
				self.chartCtrl.SetItemBackgroundColour(sel, 'INDIAN RED')
			else:
				self.chartCtrl.SetItemBackgroundColour(sel, 'LIGHT STEEL BLUE')
			self.chartCtrl.RefreshItem(sel)
			n += 1
		
	def onCheck(self, event):
	
		sel = self.chartCtrl.GetFocusedItem()
		current = chartArray[sel][10]
		changeTo = 'FALSE' if chartArray[sel][10] == 'TRUE' else 'TRUE'
		
		dlg = wx.MessageDialog(None, 'Current value is {}, do you want to change to {}?'.format(current, changeTo), 'Warning', wx.YES_NO | wx.ICON_QUESTION)
		result = dlg.ShowModal()
		if result == wx.ID_YES:
			chartArray[sel][10] = 'FALSE' if current == 'TRUE' else 'TRUE'
			# print(userArray)

		self.refreshChartDetails()


class TabThree(wx.Panel):
	
	def __init__(self, parent):
	
		updateColourDB()
		wx.Panel.__init__(self, parent)
		grid = wx.GridBagSizer(10,10)
		
		self.userList = wx.ListBox(self,-1)
		self.userList.Bind(wx.EVT_LISTBOX, self.onUserSelect)
		for row in userArray:
			self.userList.Append(row[0])
			
		mainbtnPanel = wx.Panel(self, -1)
		vbox = wx.BoxSizer(wx.VERTICAL)
		self.charts = wx.Button(mainbtnPanel, ID_CHARTS, 'Charts', size=(90,30))
		self.cur = wx.Button(mainbtnPanel, ID_CUR, 'Current',size=(90,30))
			
		self.Bind(wx.EVT_BUTTON, self.onCharts, id=ID_CHARTS)
		self.Bind(wx.EVT_BUTTON, self.onCurrent, id=ID_CUR)
		
		self.btnpad = 0
		vbox.Add((-1,0))
		vbox.Add(self.charts,1,wx.TOP,self.btnpad)
		vbox.Add(self.cur, 1, wx.TOP, self.btnpad)
		
		mainbtnPanel.SetSizer(vbox)

		chartPanel = wx.Panel(self,-1)
		self.chartBox = wx.BoxSizer()
		self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self, -1, self.figure)
		self.chartBox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
		self.SetSizer(self.chartBox)
		self.Fit()
		self.drawGraph()
		

		# self.figure2 = Figure()
		# self.axes = self.figure2.add_subplot(111)
		# self.canvas2 = FigureCanvas(self, -1, self.figure2)
		# self.chartBox.Add(self.canvas2, 1, wx.LEFT | wx.TOP | wx.GROW)
		# self.SetSizer(self.chartBox)
		# self.Fit()
		# self.drawGraph()
		# self.drawGraph2()

		grid.Add(mainbtnPanel, (10,0), (0,0), wx.EXPAND, 5)
		grid.Add(self.userList, (0,0), (10,0), wx.EXPAND, 5)
		grid.Add(self.canvas, (0,5), (0,0), wx.EXPAND, 5)
		# grid.Add(self.canvas2, (0,6), (0,0), wx.EXPAND, 5)
		self.SetSizerAndFit(grid)

		self.charts.Enable(False)
		self.cur.Enable(False)

		self.Centre()
		self.Show(True)

		
	def drawGraph(self):
		t = np.arange(0.0, 2.0, 0.01)
		s = 1 + np.sin(2 * np.pi *t) * np.exp(-t)
		self.axes.plot(t, s)
		
	def drawGraph2(self):
		t = np.linspace(0.0, 2.0, num=100,)
		s = 1 + np.sin(2 * np.pi *t)
		self.axes.plot(t, s,'r:')

	def onUserSelect(self, event):
		
		sel = self.userList.GetSelection()
		print(sel)
		self.charts.Enable(True)
		self.cur.Enable(True)

		# self.userDetails.Clear()
		n = 0
		for item in userArray[sel]:
			header = userHeaderArray[n]
			# self.userDetails.Append('{}{}'.format(header, item))
			n+=1
		
		
	def onCurrent(self,event):
		self.axes.clear()
		chartPanel = wx.Panel(self,-1)
		# self.chartBox = wx.BoxSizer()
		# self.figure = Figure()
		self.axes = self.figure.add_subplot(111)
		self.canvas = FigureCanvas(self, -1, self.figure)
		# self.chartBox.Add(self.canvas, 1, wx.LEFT | wx.TOP | wx.GROW)
		# self.SetSizer(self.chartBox)
		# self.Fit()
		self.drawGraph2()

	def onCharts(self,event):
		print(100)
		self.figure.drawGraph()
		
		
class MainFrame(wx.Frame):
	
	def __init__(self):
		
		wx.Frame.__init__(self, None, title='Stateboard V3', size = (1920,1200))
		
		p = wx.Panel(self)
		nb = wx.Notebook(p)
		
		self.tab1 = TabOne(nb)
		self.tab2 = TabTwo(nb)
		self.tab3 = TabThree(nb)
		
		nb.AddPage(self.tab1, 'Users')
		nb.AddPage(self.tab2, 'Checks')
		nb.AddPage(self.tab3, 'Stats')
		
		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		p.SetSizer(sizer)
		
		# menu
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
		if  result == wx.ID_YES:
			with open('userscopy.csv', 'w', newline='') as f:
				writer = csv.writer(f)
				writer.writerow(userHeaderArray)
				writer.writerows(userArray)
			with open('chartscopy.csv', 'w', newline='') as c:
				writer = csv.writer(c)
				writer.writerow(chartHeaderArray)
				writer.writerows(chartArray)
			self.Destroy()
		elif result == wx.ID_NO:	
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

	