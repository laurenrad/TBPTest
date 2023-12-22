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

from tbptest.reporter import Reporter
from tbptest.tbox_common import TestMenu

import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu, SelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.numberrange import NumberRange, NumberRangeValueChangedEvent
    
# Gadget Constants
G_NUMRANGE = 0x00
G_INPUT = 0x02
G_OUTPUT = 0x03

class NumberRangeWindow(Window):
    template = "NumRngeWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Set up gadgets
        self.g_numrange = NumberRange(self,G_NUMRANGE)
        self.g_input = NumberRange(self,G_INPUT)
        self.g_output = DisplayField(self,G_OUTPUT)
    
    # Test ops for numberrange
    def numrange_set_value(self):
        self.g_numrange.value = self.g_input.value
        
    def numrange_get_value(self):
        self.g_output.value = repr(self.g_numrange.value)
        
    def numrange_set_lower_bound(self):
        self.g_numrange.lower_bound = self.g_input.value
        
    def numrange_get_lower_bound(self):
        self.g_output.value = repr(self.g_numrange.lower_bound)
        
    def numrange_set_upper_bound(self):
        self.g_numrange.upper_bound = self.g_input.value
        
    def numrange_get_upper_bound(self):
        self.g_output.value = repr(self.g_numrange.upper_bound)
        
    def numrange_set_step_size(self):
        self.g_numrange.step_size = self.g_input.value
        
    def numrange_get_step_size(self):
        self.g_output.value = repr(self.g_numrange.step_size)
        
    def numrange_set_precision(self):
        self.g_numrange.precision = self.g_input.value
        
    def numrange_get_precision(self):
        self.g_output.value = repr(self.g_numrange.precision)
        
    def numrange_get_numeric(self):
        self.g_output.value = repr(self.g_numrange.numerical_field)
    
    def numrange_get_left_adj(self):
        self.g_output.value = repr(self.g_numrange.left_adjuster)
    
    def numrange_get_right_adj(self):
        self.g_output.value = repr(self.g_numrange.right_adjuster)
    
    def numrange_get_slider(self):
        self.g_output.value = repr(self.g_numrange.slider)
        
    # Event handlers for NumberRange
    @toolbox_handler(NumberRangeValueChangedEvent)
    def _numrange_value_changed(self,event,id_block,poll_block):
        self.g_output.value = f"Number range value changed: {poll_block.new_value}"
    
class NumberRangeMenu(Menu,TestMenu):
    template = "NumRngeMenu"
    
    # Entry constants
    ENTRY_SET_VALUE     = 0x00
    ENTRY_GET_VALUE     = 0x01
    ENTRY_SET_LOWER     = 0x02
    ENTRY_GET_LOWER     = 0x03
    ENTRY_SET_UPPER     = 0x04
    ENTRY_GET_UPPER     = 0x05
    ENTRY_SET_STEP      = 0x06
    ENTRY_GET_STEP      = 0x07
    ENTRY_SET_PRECISION = 0x08
    ENTRY_GET_PRECISION = 0x09
    ENTRY_GET_NUMERIC   = 0x0A
    ENTRY_GET_L_ADJ     = 0x0B
    ENTRY_GET_R_ADJ     = 0x0C
    ENTRY_GET_SLIDER    = 0x0D
    
    @toolbox_handler(SelectionEvent)
    def menu_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        window = toolbox.get_object(id_block.ancestor.id)
        self.menu_tick(id_block.self.component)
        
        if id_block.self.component == NumberRangeMenu.ENTRY_SET_VALUE:
            window.numrange_set_value()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_VALUE:
            window.numrange_get_value()
        elif id_block.self.component == NumberRangeMenu.ENTRY_SET_LOWER:
            window.numrange_set_lower_bound()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_LOWER:
            window.numrange_get_lower_bound()
        elif id_block.self.component == NumberRangeMenu.ENTRY_SET_UPPER:
            window.numrange_set_upper_bound()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_UPPER:
            window.numrange_get_upper_bound()
        elif id_block.self.component == NumberRangeMenu.ENTRY_SET_STEP:
            window.numrange_set_step_size()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_STEP:
            window.numrange_get_step_size()
        elif id_block.self.component == NumberRangeMenu.ENTRY_SET_PRECISION:
            window.numrange_set_precision()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_PRECISION:
            window.numrange_get_precision()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_NUMERIC:
            window.numrange_get_numeric()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_L_ADJ:
            window.numrange_get_left_adj()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_R_ADJ:
            window.numrange_get_right_adj()
        elif id_block.self.component == NumberRangeMenu.ENTRY_GET_SLIDER:
            window.numrange_get_slider()
        
        return True
