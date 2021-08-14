import cv2
import wx
from wx.lib.agw.floatspin import FloatSpin

from controls import InputImage
from datatypes import ImageData, ParamsTemplate
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
        params: ParamsTemplate = {"Filename": (wx.TextCtrl, {"value": path})}
        results = [ImageData()]
        func = Function("Load image", cv2.imread, params, results)
        self.add_pane_from_func(func)

    def transform(self, event):
        params: ParamsTemplate = {"Source 1": (InputImage, {}),
                                  "Weight 1": (FloatSpin, {"value": 0.5,
                                                           "min_val": 0.0,
                                                           "max_val": 1.0,
                                                           "increment": 0.05}),
                                  "Source 2": (InputImage, {}),
                                  "Weight 2": (FloatSpin, {"value": 0.5,
                                                           "min_val": 0.0,
                                                           "max_val": 1.0,
                                                           "increment": 0.05}),
                                  "Gamma": (wx.Slider, {"value": 0,
                                                        "minValue": -100,
                                                        "maxValue": 100})
                                  }
        results = [ImageData()]
        func = Function("Add Weighted", cv2.addWeighted, params, results)
        self.add_pane_from_func(func)

    def add_pane_from_func(self, func):
        pane = FunctionPane(self.notebook_1)
        func.instantiate(pane)
        self.notebook_1.AddPage(pane, func.name, True)
        func.call()
        pane.set_display(func.results[0].display())
        pane.Refresh()
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
