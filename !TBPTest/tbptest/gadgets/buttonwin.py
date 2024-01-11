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
from riscos_toolbox.gadgets.button import Button
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler

# Gadget Constants
G_BUTTON = 0x00
G_INPUT  = 0x04
G_INPUT2 = 0x07
G_INPUT3 = 0x09
G_OUTPUT = 0x05


class ButtonWindow(Window):
    template = "ButtonWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.g_button = Button(self,G_BUTTON)
        self.g_input = WritableField(self,G_INPUT)
        self.g_input2 = WritableField(self,G_INPUT2)
        self.g_input3 = WritableField(self,G_INPUT3)
        self.g_output = DisplayField(self,G_OUTPUT)
    
    # Methods for testing Button
    def button_set_flags(self):
        try:
            self.g_button.icon_flags = int(self.g_input.value)
        except ValueError:
            self.g_output.value = "Int input required"
        
    def button_get_flags(self):
        self.g_output.value = "Flags: "+hex(self.g_button.icon_flags)
        
    def button_set_value(self):
        self.g_button.value = self.g_input.value
        
    def button_get_value(self):
        self.g_output.value = self.g_button.value
        
    def button_set_validation(self):
        self.g_button.validation = self.g_input.value
        
    def button_get_validation(self):
        self.g_output.value = self.g_button.validation
        
    def button_set_font(self):
        name = self.g_input.value
        try:
            width = int(self.g_input2.value)
            height = int(self.g_input3.value)
        except ValueError:
            self.g_output.value = "Int input required"
        else:
            self.g_button.set_font(name,width,height)

            
class ButtonMenu(Menu,TestMenu):
    template = "ButtonMenu"
    
    # Entry constants
    ENTRY_SET_FLAGS      = 0x00
    ENTRY_GET_FLAGS      = 0x01
    ENTRY_SET_VALUE      = 0x02
    ENTRY_GET_VALUE      = 0x03
    ENTRY_SET_VALIDATION = 0x04
    ENTRY_GET_VALIDATION = 0x05
    ENTRY_SET_FONT       = 0x06
    
    @toolbox_handler(SelectionEvent)
    def menu_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
        
        window = toolbox.get_object(id_block.parent.id)
        self.menu_tick(id_block.self.component)
        
        if id_block.self.component == ButtonMenu.ENTRY_SET_FLAGS:
            window.button_set_flags()
        elif id_block.self.component == ButtonMenu.ENTRY_GET_FLAGS:
            window.button_get_flags()      
        elif id_block.self.component == ButtonMenu.ENTRY_SET_VALUE:
            window.button_set_value()
        elif id_block.self.component == ButtonMenu.ENTRY_GET_VALUE:
            window.button_get_value()
        elif id_block.self.component == ButtonMenu.ENTRY_SET_VALIDATION:  
            window.button_set_validation()
        elif id_block.self.component == ButtonMenu.ENTRY_GET_VALIDATION:
            window.button_get_validation()
        elif id_block.self.component == ButtonMenu.ENTRY_SET_FONT:
            window.button_set_font()
            
        return True
