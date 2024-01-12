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
from tbptest.tbox_const import *
from tbptest.tbox_common import *

import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea

# Gadget Constants
G_TEXTAREA = 0x00
G_INPUT1 = 0x01
G_INPUT2 = 0x03
G_INPUT3 = 0x05
G_OUTPUT1 = 0x07
G_OUTPUT2 = 0x08


class TextAreaWindow(Window):
    template = "TxtAreaWin"

    def __init__(self, *args):
        super().__init__(*args)

        # Set up gadgets
        self.g_textarea = TextArea(self, G_TEXTAREA)
        self.g_input1 = WritableField(self, G_INPUT1)
        self.g_input2 = WritableField(self, G_INPUT2)
        self.g_input3 = WritableField(self, G_INPUT3)
        self.g_output1 = DisplayField(self, G_OUTPUT1)
        self.g_output2 = TextArea(self, G_OUTPUT2)

    # Test ops for TextArea
    def textarea_get_state(self):
        self.g_output1.value = repr(self.g_textarea.state)

    def textarea_set_state(self):
        try:
            self.g_textarea.state = int(self.g_input1.value)
        except ValueError:
            self.g_output1.value = "Err: expected int in Input1"

    def textarea_set_text(self):
        self.g_textarea.text = self.g_input1.value

    def textarea_get_text(self):
        self.g_output2.text = self.g_textarea.text

    def textarea_insert_text(self):
        try:
            index = int(self.g_input1.value)
        except ValueError:
            self.g_output1.value = "err: expected int in Input1"
        else:
            text = self.g_input2.value
            self.g_textarea.insert(index, text)

    def textarea_replace_text(self):
        try:
            start = int(self.g_input1.value)
            end = int(self.g_input2.value)
        except ValueError:
            self.g_output1.value = "err: Input1=int, Input2=int, Input3=str"
        else:
            text = self.g_input3.value
            self.g_textarea.replace(start, end, text)

    def textarea_get_selection(self):
        self.g_output2.text = self.g_textarea.selection

    def textarea_set_selection(self):
        self.g_textarea.selection = self.g_input1.value

    def textarea_get_selection_points(self):
        start, end = self.g_textarea.selection_points
        s = f"Selection: start={start}, end={end}"
        self.g_output1.value = s

    def textarea_set_selection_points(self):
        try:
            start = int(self.g_input1.value)
            end = int(self.g_input2.value)
        except ValueError:
            self.g_output1.value = "err: Input1=int, Input2=int"
        else:
            self.g_textarea.selection_points = (start, end)

    def textarea_set_font(self):
        try:
            name = self.g_input1.value
            width = int(self.g_input2.value)
            height = int(self.g_input3.value)
        except ValueError:
            self.g_output1.value = "err: Input1=str, Input2=int, Input3=int"
        else:
            self.g_textarea.set_font(name, width, height)

    def textarea_set_colour(self):
        try:
            fg = int(self.g_input1.value)
            bg = int(self.g_input2.value)
        except ValueError:
            self.g_output1.value = "err: Input1=int, Input2=int"
        else:
            self.g_textarea.colour = (fg, bg)

    def textarea_get_colour(self):
        (fg, bg) = self.g_textarea.colour
        self.g_output1.value = f"fg={fg}, bg={bg}"

    def textarea_set_cursor_pos(self):
        try:
            self.g_textarea.cursor = int(self.g_input1.value)
        except ValueError:
            self.g_output1.value = "err: Input1=int"

    def textarea_get_cursor_pos(self):
        self.g_output1.value = repr(self.g_textarea.cursor)


class TextAreaMenu(Menu, TestMenu):
    template = "TxtAreaMenu"

    # Menu event handlers
    @toolbox_handler(EvTextAreaGetState)
    def _textarea_get_state(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_state()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetState)
    def _textarea_set_state(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_state()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetText)
    def _textarea_set_text(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_text()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaGetText)
    def _textarea_get_text(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_text()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaInsertText)
    def _textarea_insert_text(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_insert_text()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaReplaceText)
    def _textarea_replace_text(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_replace_text()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaGetSelection)
    def _textarea_get_selection(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_selection()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetSelection)
    def _textarea_set_selection(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_selection()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaGetSelectionPoints)
    def _textarea_get_selection_points(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_selection_points()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetSelectionPoints)
    def _textarea_set_selection_points(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_selection_points()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetFont)
    def _textarea_set_font(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_font()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetColour)
    def _textarea_set_colour(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_colour()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaGetColour)
    def _textarea_get_colour(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_colour()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaSetCursorPos)
    def _textarea_set_cursor_pos(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_set_cursor_pos()
        self.menu_tick(id_block.self.component)

    @toolbox_handler(EvTextAreaGetCursorPos)
    def _textarea_get_cursor_pos(self, event, id_block, poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.textarea_get_cursor_pos()
        self.menu_tick(id_block.self.component)
