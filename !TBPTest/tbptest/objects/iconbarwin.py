# MIT License

# Copyright (c) 2023 Lauren Rad

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from tbptest.reporter import Reporter # noqa

import riscos_toolbox as toolbox
from riscos_toolbox.objects.window import Window
from riscos_toolbox.objects.iconbar import Iconbar, IconbarClickedEvent
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler


class IconbarWindow(Window):
    template = "IconbarWin"

    # Gadget constants
    G_SHOW = 0x00
    G_GET = 0x0C
    G_SET = 0x0D
    G_TEXTAREA = 0x08
    G_RESULT = 0x09
    G_INPUT_STR = 0x0A
    G_RADIO_ICON_HANDLE = 0x11
    G_RADIO_MENU_ID = 0x12
    G_RADIO_SEL_EVENT = 0x13
    G_RADIO_ADJ_EVENT = 0x14
    G_RADIO_SEL_OBJ = 0x15
    G_RADIO_ADJ_OBJ = 0x16
    G_RADIO_HELP_MSG = 0x17
    G_RADIO_TEXT = 0x18
    G_RADIO_SPRITE = 0x19

    def __init__(self, *args):
        super().__init__(*args)
        self.iconbar = toolbox.create_object("Iconbar")
        self.result = DisplayField(self, IconbarWindow.G_RESULT)
        self.textarea = TextArea(self, IconbarWindow.G_TEXTAREA)
        self.input_str = WritableField(self, IconbarWindow.G_INPUT_STR)
        self.showhide = ActionButton(self, IconbarWindow.G_SHOW)
        self.selected_test = IconbarWindow.G_RADIO_ICON_HANDLE
        self.showing = False

    @toolbox_handler(RadioButtonStateChangedEvent)
    def test_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        self.selected_test = id_block.self.component

        return True

    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        if id_block.self.component == IconbarWindow.G_SHOW:
            if not self.showing:
                self.iconbar.show()
                self.showing = True
                self.showhide.text = "Hide"
            else:
                self.iconbar.hide()
                self.showing = False
                self.showhide.text = "Show"
        elif id_block.self.component == IconbarWindow.G_GET:
            if self.selected_test == IconbarWindow.G_RADIO_ICON_HANDLE:
                Reporter.print("test: iconbar: get icon handle")
                self.result.value = repr(self.iconbar.icon_handle)
            elif self.selected_test == IconbarWindow.G_RADIO_MENU_ID:
                self.result.value = repr(self.iconbar.menu_id)+" ("+hex(self.iconbar.menu_id)+")"
            elif self.selected_test == IconbarWindow.G_RADIO_SEL_EVENT:
                self.result.value = repr(self.iconbar.select_event)
            elif self.selected_test == IconbarWindow.G_RADIO_ADJ_EVENT:
                self.result.value = repr(self.iconbar.adjust_event)
            elif self.selected_test == IconbarWindow.G_RADIO_SEL_OBJ:
                self.result.value = repr(self.iconbar.show_select_id)
            elif self.selected_test == IconbarWindow.G_RADIO_ADJ_OBJ:
                self.result.value = repr(self.iconbar.show_adjust_id)
            elif self.selected_test == IconbarWindow.G_RADIO_HELP_MSG:
                self.result.value = self.iconbar.help_message
            elif self.selected_test == IconbarWindow.G_RADIO_TEXT:
                self.result.value = self.iconbar.text
            elif self.selected_test == IconbarWindow.G_RADIO_SPRITE:
                self.result.value = self.iconbar.sprite
            else:
                Reporter.print("test: iconbar: unknown get test")
        elif id_block.self.component == IconbarWindow.G_SET:
            if self.selected_test == IconbarWindow.G_RADIO_MENU_ID:
                try:
                    self.iconbar.menu_id = int(self.input_str.value)
                except ValueError:
                    self.result.value = "Expected integer input."
            elif self.selected_test == IconbarWindow.G_RADIO_SEL_EVENT:
                try:
                    self.iconbar.select_event = int(self.input_str.value)
                except ValueError:
                    self.result.value = "Expected integer input."
            elif self.selected_test == IconbarWindow.G_RADIO_ADJ_EVENT:
                try:
                    self.iconbar.adjust_event = int(self.input_str.value)
                except ValueError:
                    self.result.value = "Expected integer input."
            elif self.selected_test == IconbarWindow.G_RADIO_SEL_OBJ:
                try:
                    self.iconbar.show_select_id = int(self.input_str.value)
                except ValueError:
                    self.result.value = "Expected integer input."
            elif self.selected_test == IconbarWindow.G_RADIO_ADJ_OBJ:
                try:
                    self.iconbar.show_adjust_id = int(self.input_str.value)
                except ValueError:
                    self.result.value = "Expected integer input."
            elif self.selected_test == IconbarWindow.G_RADIO_HELP_MSG:
                self.iconbar.help_message = self.input_str.value
            elif self.selected_test == IconbarWindow.G_RADIO_TEXT:
                self.iconbar.text = self.input_str.value
            elif self.selected_test == IconbarWindow.G_RADIO_SPRITE:
                self.iconbar.sprite = self.input_str.value
            else:
                Reporter.print("test: iconbar: unknown set test")
        else:
            return False

        return True

    @toolbox_handler(IconbarClickedEvent)
    def iconbar_clicked(self, event, id_block, poll_block):
        Reporter.print("IconbarClickedEvent")

        self.textarea.insert(-1, "IconbarClickedEvent | ")

        return True
