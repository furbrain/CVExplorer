from functools import partial
from typing import List

import cv2
import wx

from datatypes import ImageData
from functions import Function, ParameterTemplate, Module
from functions.template import FunctionTemplate
from gui.basegui import CodeDialog
from parser.codeparser import CodeParser
from parser.moduleparser import ModuleParser
from . import basegui
from .pane import FunctionPane


class CVEFrame(basegui.CVEFrame):

    def generate_code(self, event):
        text = '\n'.join(func.as_code() for func in Function.ALL)
        dlg = CodeDialog(None)
        dlg.text.SetValue("import cv2\n\n" + text)
        dlg.Show()

    def load_image(self, event):
        # first get our pathname...
        with wx.FileDialog(self,
                           "Open Image file",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fd:
            if fd.ShowModal() != wx.ID_OK:
                return
        path = fd.GetPath()
        params: List[ParameterTemplate] = [
            ParameterTemplate("filename", "str", "Name of file to be loaded", default=path)]
        results = [ImageData("image")]
        func = Function("Load image", cv2.imread, params, results)
        self.add_pane_from_func(func)

    def add_pane_from_func(self, func):
        pane = FunctionPane(self.notebook)
        func.instantiate(pane)
        self.notebook.AddPage(pane, func.name, True)
        func.on_changed(None)
        pane.Refresh()
        self.Layout()
        self.Refresh()

    def get_menu_from_module(self, module: Module) -> wx.Menu:
        menu = wx.Menu()
        for func in module.functions:
            item: wx.MenuItem = menu.Append(wx.ID_ANY, func.name, "")
            self.Bind(wx.EVT_MENU, partial(self.add_func, func), id=item.GetId())
        for child in module.children:
            if child.count() > 0:
                menu.AppendMenu(wx.ID_ANY, child.name, self.get_menu_from_module(child))
        return menu

    def add_menu_items(self):
        root_module = ModuleParser().get_modules()
        menu = self.get_menu_from_module(root_module)
        self.frame_menubar.Append(menu, "Functions")
        utils_module = CodeParser().get_modules()
        utils_menu = self.get_menu_from_module(utils_module)
        self.frame_menubar.Append(utils_menu, "Utils")

    # noinspection PyUnusedLocal
    def add_func(self, func: FunctionTemplate, event):
        self.add_pane_from_func(func.create_function())

    def exit(self, event):
        self.Destroy()


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
