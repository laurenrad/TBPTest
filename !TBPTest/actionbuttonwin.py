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

from reporter import Reporter
from tbox_const import *
from tbox_common import TestMenu
import riscos_toolbox as toolbox

from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.actionbutton import ActionButton
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler

# Gadget Constants
G_ACTIONBUTTON = 0x00
G_INPUT	       = 0x02
G_OUTPUT       = 0x01
G_SHOW_ID      = 0x07

class ShowableWindow(Window):
    template = "ShowableWin"
    
    def __init__(self, *args):
        super().__init__(*args)

class ActionButtonWindow(Window):
    template = "ActBttnWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.g_actionbutton = ActionButton(self,G_ACTIONBUTTON)
        self.g_input = WritableField(self,G_INPUT)
        self.g_output = DisplayField(self,G_OUTPUT)
        self.g_show_id = DisplayField(self,G_SHOW_ID)
        self.showable_win = toolbox.create_object(ShowableWindow.template,ShowableWindow)
        
        self.g_show_id.value = repr(self.showable_win.id)
        
    # Methods for testing ActionButton
    def actionbutton_set_text(self):
        self.g_actionbutton.text = self.g_input.value
        
    def actionbutton_get_text(self):
        self.g_output.value = self.g_actionbutton.text
        
    def actionbutton_set_event(self):
        try:
            self.g_actionbutton.event = int(self.g_input.value)
        except ValueError as e:
            self.g_output.value = "Int input required"
        
    def actionbutton_get_event(self):
        self.g_output.value = repr(self.g_actionbutton.event)
        
    def actionbutton_set_click_show(self):
        try:
            self.g_actionbutton.click_show = int(self.g_input.value)
        except ValueError as e:
            self.g_output.value = "Int input required"
        
    def actionbutton_get_click_show(self):
        self.g_output = repr(self.g_actionbutton.click_show)
        
    # Event handlers for ActionButton
    @toolbox_handler(EvActionButtonSelected)
    def ActionButtonSelected(self,event,id_block,poll_block):
        self.g_output.value = "Action button selected."

class ActionButtonMenu(Menu,TestMenu):
    template = "ActBttnMenu"
    
    ## ActionButton event handlers
    @toolbox_handler(EvActionButtonSetText)
    def ActionButtonSetText(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_set_text()
        self.menu_tick(id_block.self.component)
    
    @toolbox_handler(EvActionButtonGetText)
    def ActionButtonGetText(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_get_text()
        self.menu_tick(id_block.self.component)
    
    @toolbox_handler(EvActionButtonSetEvent)
    def ActionButtonSetEvent(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_set_event()
        self.menu_tick(id_block.self.component)
    
    @toolbox_handler(EvActionButtonGetEvent)
    def ActionButtonGetEvent(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_get_event()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvActionButtonSetClickShow)
    def ActionButtonSetClickShow(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_set_click_show()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvActionButtonGetClickShow)
    def ActionButtonGetClickShow(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.actionbutton_get_click_show()
        self.menu_tick(id_block.self.component)
