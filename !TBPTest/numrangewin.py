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
import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from tbox_const import *
from tbox_common import TestMenu
try:
    from riscos_toolbox.gadgets.numberrange import NumberRange, NumberRangeValueChangedEvent
except ModuleNotFoundError as e:
    Reporter.print("No NumberRange in riscos_toolbox")
else:
    
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
            self.g_output.value = repr(self.g_numrange.numeric)
        
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
        
        # Event Handlers
        @toolbox_handler(EvNumRangeSetValue)
        def _numrange_set_value(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_set_value()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvNumRangeGetValue)
        def _numrange_get_value(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_value()
            self.menu_tick(id_block.self.component)

        @toolbox_handler(EvNumRangeSetLowerBound)
        def NumRangeSetLowerBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_set_lower_bound()
            self.menu_tick(id_block.self.component)
    
        @toolbox_handler(EvNumRangeGetLowerBound)
        def NumRangeGetLowerBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_lower_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvNumRangeSetUpperBound)
        def NumRangeSetUpperBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_set_upper_bound()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetUpperBound)
        def NumRangeGetUpperBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_upper_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvNumRangeSetStepSize)
        def NumRangeSetStepSize(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_set_step_size()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetStepSize)
        def NumRangeGetStepSize(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_step_size()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvNumRangeSetPrecision)
        def NumRangeSetPrecision(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_set_precision()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetPrecision)
        def NumRangeGetPrecision(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_precision()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvNumRangeGetNumeric)
        def NumRangeGetNumeric(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_numeric()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetLeftAdj)
        def NumRangeGetValue(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_left_adj()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetRightAdj)
        def NumRangeGetRightAdj(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_right_adj()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvNumRangeGetSlider)
        def NumRangeGetSlider(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.numrange_get_slider()
            self.menu_tick(id_block.self.component)
