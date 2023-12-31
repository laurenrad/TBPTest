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
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler

# Gadget Constants
G_DISPLAYFIELD = 0x00
G_INPUT        = 0x04
G_OUTPUT       = 0x05

class DisplayFieldWindow(Window):
    template = "DspFieldWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        self.g_displayfield = DisplayField(self,G_DISPLAYFIELD)
        self.g_input = WritableField(self,G_INPUT)
        self.g_output = DisplayField(self,G_OUTPUT)
        
    # Methods for testing DisplayField
    
    def displayfield_set_value(self):
        self.g_displayfield.value = self.g_input.value
        
    def displayfield_get_value(self):
        self.g_output.value = self.g_displayfield.value
        
class DisplayFieldMenu(Menu,TestMenu):
    template = "DispFldMenu"
    
    ## DisplayField event handlers
    @toolbox_handler(EvDisplayFieldSetValue)
    def DisplayFieldSetValue(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.displayfield_set_value()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvDisplayFieldGetValue)
    def DisplayFieldGetValue(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.displayfield_get_value()
        self.menu_tick(id_block.self.component)
        