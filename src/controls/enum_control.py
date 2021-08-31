import wx
import typing

from lxml import html
# noinspection PyPep8Naming
from lxml.html import builder as E

import wx.lib.agw.balloontip as bt

if typing.TYPE_CHECKING:
    from functions.enum import Enum


# noinspection PyShadowingBuiltins
class EnumControl(wx.Choice):
    def __init__(self, parent: wx.Window, id, enum: "Enum"):
        super().__init__(parent, id)
        for name, value in enum.values.items():
            self.Append(name, value)
        tooltip_contents = [E.TR(E.TD(E.B(name)), E.TD(html.fromstring(desc)))
                   for name, desc in enum.descriptions.items()]

        tooltip_text = html.tostring(E.TABLE(*tooltip_contents), encoding="unicode")

        tooltip_contents = [f"{name}:\t{html.fromstring(desc).text_content()}" for name, desc in enum.descriptions.items()]
        tooltip_contents = '\n'.join(tooltip_contents)
        self.tooltip_contents = f"{enum.name}\n{tooltip_contents}"
        self.SetToolTip("")

    # noinspection PyPep8Naming
    def GetValue(self):
        index = self.GetSelection()
        result = self.GetClientData(index)
        print(f"Getting value for index{index} result is {result}")
        return result

    def SetToolTip(self, text: str):
        if text:
            text = f"{text}\n\n{self.tooltip_contents}"
        else:
            text = self.tooltip_contents
        super().SetToolTip(text)

