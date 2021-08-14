import cv2
import wx

from datatypes import ImageData
from datatypes.base import ParamsTemplate
from functions import Function
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
            pane = FunctionPane(self.notebook_1)
            params: ParamsTemplate = {"Filename": (wx.TextCtrl, (path,))}
            results = [ImageData("Image")]
            func = Function("Load image", cv2.imread, params, results)
            func.instantiate(pane)
            self.notebook_1.AddPage(pane, "image", True)
            func.call()
            pane.set_display(func.results[0].display())
            pane.Refresh()
        # self.Fit()
        self.Layout()
        self.Refresh()

    def exit(self, event):
        self.Close()


class CVExplorer(wx.App):
    def OnInit(self):
        # noinspection PyAttributeOutsideInit
        self.frame = CVEFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

    # end of class MyApp


if __name__ == "__main__":
    app = CVExplorer(0)
    app.MainLoop()
