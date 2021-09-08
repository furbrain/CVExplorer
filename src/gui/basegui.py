# -*- coding: UTF-8 -*-
#
# generated by wxGlade 0.9.4 on Sun Sep  5 17:38:56 2021
#

import wx

# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
import wx.dataview
# end wxGlade


class CVEFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CVEFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((825, 578))
        
        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(wx.ID_OPEN, "Open Project", "")
        self.Bind(wx.EVT_MENU, self.open_project, id=wx.ID_OPEN)
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Load Image", "")
        self.Bind(wx.EVT_MENU, self.load_image, id=item.GetId())
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Generate Code", "")
        self.Bind(wx.EVT_MENU, self.generate_code, id=item.GetId())
        wxglade_tmp_menu.Append(wx.ID_SAVE, "Save project", "")
        self.Bind(wx.EVT_MENU, self.save_project, id=wx.ID_SAVE)
        wxglade_tmp_menu.Append(wx.ID_SAVEAS, "Save project as", "")
        self.Bind(wx.EVT_MENU, self.save_project_as, id=wx.ID_SAVEAS)
        item = wxglade_tmp_menu.Append(wx.ID_ANY, "Export Script", "")
        self.Bind(wx.EVT_MENU, self.export_script, id=item.GetId())
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(wx.ID_EXIT, "Exit", "")
        self.Bind(wx.EVT_MENU, self.exit, id=wx.ID_EXIT)
        self.frame_menubar.Append(wxglade_tmp_menu, "File")
        self.SetMenuBar(self.frame_menubar)
        # Menu Bar end
        self.notebook_1 = wx.Notebook(self, wx.ID_ANY)
        self.intro_pane = wx.Panel(self.notebook_1, wx.ID_ANY)
        self.panel_2 = wx.ScrolledWindow(self.intro_pane, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.panel_1 = wx.ScrolledWindow(self.intro_pane, wx.ID_ANY, style=wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()

        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CVEFrame.__set_properties
        self.SetTitle("frame")
        self.panel_2.SetScrollRate(10, 10)
        self.panel_1.SetMinSize((200, -1))
        self.panel_1.SetScrollRate(10, 10)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CVEFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.FlexGridSizer(1, 2, 0, 0)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        label_1 = wx.StaticText(self.panel_2, wx.ID_ANY, "Welcome to CVExplorer. Start by loading a sample image")
        label_1.Wrap(600)
        sizer_4.Add(label_1, 0, wx.ALL | wx.EXPAND, 3)
        self.panel_2.SetSizer(sizer_4)
        sizer_2.Add(self.panel_2, 1, wx.ALL | wx.EXPAND, 3)
        static_line_1 = wx.StaticLine(self.intro_pane, wx.ID_ANY, style=wx.LI_VERTICAL)
        sizer_2.Add(static_line_1, 0, wx.EXPAND, 0)
        label_4 = wx.StaticText(self.panel_1, wx.ID_ANY, "label_4")
        grid_sizer_1.Add(label_4, 0, wx.ALL, 3)
        label_5 = wx.StaticText(self.panel_1, wx.ID_ANY, "Params")
        grid_sizer_1.Add(label_5, 0, wx.ALL, 3)
        sizer_3.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        static_line_2 = wx.StaticLine(self.panel_1, wx.ID_ANY)
        sizer_3.Add(static_line_2, 0, wx.EXPAND, 0)
        label_3 = wx.StaticText(self.panel_1, wx.ID_ANY, "Result params")
        label_3.SetMinSize((120, 300))
        sizer_3.Add(label_3, 0, wx.ALL, 3)
        self.panel_1.SetSizer(sizer_3)
        sizer_2.Add(self.panel_1, 0, wx.ALL | wx.EXPAND, 3)
        self.intro_pane.SetSizer(sizer_2)
        self.notebook_1.AddPage(self.intro_pane, "Introduction")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def open_project(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'open_project' not implemented!")
        event.Skip()

    def load_image(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'load_image' not implemented!")
        event.Skip()

    def generate_code(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'generate_code' not implemented!")
        event.Skip()

    def save_project(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'save_project' not implemented!")
        event.Skip()

    def save_project_as(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'save_project_as' not implemented!")
        event.Skip()

    def export_script(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'export_script' not implemented!")
        event.Skip()

    def exit(self, event):  # wxGlade: CVEFrame.<event_handler>
        print("Event handler 'exit' not implemented!")
        event.Skip()

# end of class CVEFrame

class CodeDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        # begin wxGlade: CodeDialog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetSize((800, 500))
        self.text = wx.TextCtrl(self, wx.ID_ANY, "", style=wx.TE_DONTWRAP | wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY)
        self.button_1 = wx.Button(self, wx.ID_OK, "")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: CodeDialog.__set_properties
        self.SetTitle("dialog")
        self.SetSize((800, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: CodeDialog.__do_layout
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, "Generated Code"), wx.VERTICAL)
        sizer_6.Add(self.text, 1, wx.ALL | wx.EXPAND, 3)
        sizer_5.Add(sizer_6, 1, wx.ALL | wx.EXPAND, 3)
        sizer_5.Add(self.button_1, 0, wx.ALIGN_RIGHT | wx.ALL, 3)
        self.SetSizer(sizer_5)
        self.Layout()
        # end wxGlade

# end of class CodeDialog

class FunctionPaneBase(wx.Panel):
    def __init__(self, *args, **kwds):
        # begin wxGlade: FunctionPaneBase.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL
        wx.Panel.__init__(self, *args, **kwds)
        self.window_1 = wx.SplitterWindow(self, wx.ID_ANY)
        self.display_pane = wx.ScrolledWindow(self.window_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)
        self.results_bitmap = wx.StaticBitmap(self.display_pane, wx.ID_ANY, wx.Bitmap(32, 32))
        self.results_text = wx.TextCtrl(self.display_pane, wx.ID_ANY, "", style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.results_matrix = wx.dataview.DataViewListCtrl(self.display_pane, wx.ID_ANY)
        self.params_pane = wx.ScrolledWindow(self.window_1, wx.ID_ANY, style=wx.TAB_TRAVERSAL)

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: FunctionPaneBase.__set_properties
        self.display_pane.SetScrollRate(10, 10)
        self.params_pane.SetScrollRate(10, 10)
        self.window_1.SetMinimumPaneSize(20)
        self.window_1.SetSashGravity(1.0)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: FunctionPaneBase.__do_layout
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        self.params_sizer = wx.BoxSizer(wx.VERTICAL)
        self.input_param_sizer = wx.FlexGridSizer(0, 2, 3, 3)
        sizer_8 = wx.BoxSizer(wx.VERTICAL)
        sizer_8.Add(self.results_bitmap, 1, wx.ALL, 3)
        sizer_8.Add(self.results_text, 1, wx.ALL | wx.EXPAND, 3)
        sizer_8.Add(self.results_matrix, 1, wx.EXPAND, 0)
        self.display_pane.SetSizer(sizer_8)
        self.input_param_sizer.AddGrowableCol(1)
        self.params_sizer.Add(self.input_param_sizer, 1, wx.EXPAND, 0)
        static_line_3 = wx.StaticLine(self.params_pane, wx.ID_ANY)
        self.params_sizer.Add(static_line_3, 0, wx.ALL | wx.EXPAND, 3)
        self.params_pane.SetSizer(self.params_sizer)
        self.window_1.SplitVertically(self.display_pane, self.params_pane, 0)
        sizer_7.Add(self.window_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_7)
        sizer_7.Fit(self)
        self.Layout()
        # end wxGlade

# end of class FunctionPaneBase
