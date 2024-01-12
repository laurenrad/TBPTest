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
from tbptest.tbox_common import TestMenu

import riscos_toolbox as toolbox
from riscos_toolbox.objects.menu import Menu, SelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.gadgets.optionbutton import OptionButton, OptionButtonStateChangedEvent

# Gadget Constants
G_OPTION = 0x00
G_INPUT = 0x04
G_INPUTOPT = 0x03
G_OUTPUT = 0x05


class OptionButtonWindow(Window):
    template = "OptButtnWin"

    def __init__(self, *args):
        super().__init__(*args)

        self.g_option = OptionButton(self, G_OPTION)
        self.g_inputopt = OptionButton(self, G_INPUTOPT)
        self.g_input = WritableField(self, G_INPUT)
        self.g_output = DisplayField(self, G_OUTPUT)

    # Methods for testing OptionButton

    def optbutton_set_label(self):
        self.g_option.label = self.g_input.value

    def optbutton_get_label(self):
        self.g_output.value = self.g_option.label

    def optbutton_set_event(self):
        # As in various other places, this is because I don't want to depend on
        # NumberRange since it isn't in upstream riscos_toolbox yet
        try:
            self.g_option.event = int(self.g_input.value)
        except ValueError:
            self.g_output.value = "Expected int input"

    def optbutton_get_event(self):
        self.g_output.value = repr(self.g_option.event)

    def optbutton_set_state(self):
        self.g_option.state = self.g_inputopt.state

    def optbutton_get_state(self):
        self.g_output.value = repr(self.g_option.state)

    # Event handlers for OptionButton

    @toolbox_handler(OptionButtonStateChangedEvent)
    def optbutton_state_changed(self, event, id_block, poll_block):
        msg = "Option state changed: "+repr(poll_block.new_state)
        if poll_block.on:
            msg += " on"
        if poll_block.off:
            msg += " off"

        self.g_output.value = msg


class OptionButtonMenu(Menu, TestMenu):
    template = "OptBttnMenu"

    # Constants for menu entries
    ENTRY_SET_LABEL = 0x00
    ENTRY_GET_LABEL = 0x01
    ENTRY_SET_EVENT = 0x02
    ENTRY_GET_EVENT = 0x03
    ENTRY_SET_STATE = 0x04
    ENTRY_GET_STATE = 0x05

    @toolbox_handler(SelectionEvent)
    def menu_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        window = toolbox.get_object(id_block.parent.id)
        self.menu_tick(id_block.self.component)

        if id_block.self.component == OptionButtonMenu.ENTRY_SET_LABEL:
            window.optbutton_set_label()
        elif id_block.self.component == OptionButtonMenu.ENTRY_GET_LABEL:
            window.optbutton_get_label()
        elif id_block.self.component == OptionButtonMenu.ENTRY_SET_EVENT:
            window.optbutton_set_event()
        elif id_block.self.component == OptionButtonMenu.ENTRY_GET_EVENT:
            window.optbutton_get_event()
        elif id_block.self.component == OptionButtonMenu.ENTRY_SET_STATE:
            window.optbutton_set_state()
        elif id_block.self.component == OptionButtonMenu.ENTRY_GET_STATE:
            window.optbutton_get_state()

        return True
