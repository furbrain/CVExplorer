import wx
import typing

from lxml import html
# noinspection PyPep8Naming
from lxml.html import builder as E
if typing.TYPE_CHECKING:
    from functions.enum import Enum


# noinspection PyShadowingBuiltins
class EnumControl(wx.Choice):
    def __init__(self, parent: wx.Window, id, enum: "Enum"):
        super().__init__(parent, id)
        for name, value in enum.values.items():
            self.Append(name, value)

        tooltip = [html.tostring(E.TR(E.TD(name), E.TD(desc)), encoding='unicode')
                   for name, desc in enum.descriptions.items()]
        self.SetToolTip(html.tostring(E.TABLE(''.join(tooltip))))

    # noinspection PyPep8Naming
    def GetValue(self):
        index = self.GetSelection()
        result = self.GetClientData(index)
        return result

