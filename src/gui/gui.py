from functools import partial

import cv2
import wx
from datatypes import ImageData, ParamsTemplate
from functions import Function
from functions.template import FunctionTemplate
from . import basegui
from .pane import FunctionPane


class CVEFrame(basegui.CVEFrame):
    def load_image(self, event):
        # first get our pathname...
        with wx.FileDialog(self,
                           "Open Image file",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fd:
            if fd.ShowModal() != wx.ID_OK:
                return
        path = fd.GetPath()
        params: ParamsTemplate = {"filename": (wx.TextCtrl, {"value": path})}
        results = [ImageData()]
        func = Function("Load image", cv2.imread, params, results)
        self.add_pane_from_func(func)

    def add_pane_from_func(self, func):
        pane = FunctionPane(self.notebook_1)
        func.instantiate(pane)
        self.notebook_1.AddPage(pane, func.name, True)
        func.on_changed(None)
        pane.Refresh()
        self.Layout()
        self.Refresh()

    def add_menu_items(self):
        title, funcs = FunctionTemplate.from_url("d4/d86/group__imgproc__filter.html")
        menu = wx.Menu()
        for func in funcs:
            item: wx.MenuItem = menu.Append(wx.ID_ANY, func.name, "")
            self.Bind(wx.EVT_MENU, partial(self.add_func, func), id=item.GetId())
        self.frame_menubar.Append(menu, title)

    # noinspection PyUnusedLocal
    def add_func(self, func: FunctionTemplate, event):
        print(f"Adding function {func.name}")
        self.add_pane_from_func(func.create_function())

    def exit(self, event):
        self.Close()


class CVExplorer(wx.App):
    def OnInit(self):
        # noinspection PyAttributeOutsideInit
        self.frame = CVEFrame(None, wx.ID_ANY, "")
        self.frame.add_menu_items()
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    # end of class MyApp


if __name__ == "__main__":
    app = CVExplorer(0)
    app.MainLoop()
