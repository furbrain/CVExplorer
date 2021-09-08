import typing

import wx

# noinspection PyPep8Naming

if typing.TYPE_CHECKING:
    from functions.enum import Enum


# noinspection PyShadowingBuiltins
class EnumControl(wx.Choice):
    def __init__(self, parent: wx.Window, id, enum: "Enum"):
        super().__init__(parent, id)
        self.reverse_mapping = {}
        for name, value in enum.values.items():
            self.Append(name, value)
        tooltip_contents = [f"{name}:\t{desc}" for name, desc in enum.descriptions.items()]
        tooltip_contents = '\n'.join(tooltip_contents)
        self.tooltip_contents = f"{enum.name}\n{tooltip_contents}"
        self.SetToolTip("")

    # noinspection PyPep8Naming
    def GetValue(self):
        index = self.GetSelection()
        result = self.GetClientData(index)
        return result

    # noinspection PyPep8Naming
    def SetValue(self, value: str):
        if value is None:
            self.SetSelection(0)
        self.SetStringSelection(value)

    def SetToolTip(self, text: str):
        if text:
            text = f"{text}\n\n{self.tooltip_contents}"
        else:
            text = self.tooltip_contents
        super().SetToolTip(text)

    # noinspection PyPep8Naming
    def GetCode(self) -> str:
        return f"cv2.{self.GetStringSelection()}"
