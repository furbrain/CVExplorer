from typing import Optional, TYPE_CHECKING

import wx
if TYPE_CHECKING:
    from gui.pane import FunctionPane


# noinspection PyPep8Naming
class ArrayControl(wx.ComboBox):
    # noinspection PyShadowingBuiltins
    def __init__(self, parent, id):
        from functions import Function
        choices = list(Function.get_all_vars().keys())
        super().__init__(parent, id, choices=choices, value=choices[0])

    def get_pane(self, window: wx.Window) -> "FunctionPane":
        from gui.pane import FunctionPane
        parent = window.GetParent()
        if isinstance(parent, FunctionPane):
            return parent
        if parent is None:
            raise ValueError("Could not find a FunctionPane parent for element")
        return self.get_pane(parent)

    def SetValue(self, value: Optional[str]):
        if value is None:
            self.SetSelection(0)
        else:
            super().SetValue(value)

    def GetValue(self):
        from gui.gui import MainFrame
        frame: MainFrame = self.GetTopLevelParent()
        return eval(super().GetValue(), frame.get_vars(self))

    def GetCode(self):
        return super().GetValue()
