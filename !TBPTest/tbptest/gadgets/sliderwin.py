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
from tbptest.tbox_const import *
from tbptest.tbox_common import TestMenu


import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField

try:
    from riscos_toolbox.gadgets.slider import Slider, SliderValueChangedEvent
    
    # Gadget constants
    G_SLIDER = 0x00
    G_INPUT  = 0x01
    G_INPUT2 = 0x06
    G_OUTPUT = 0x02
    
    class SliderWindow(Window):
        template = "SliderWin"
        
        def __init__(self, *args):
            super().__init__(*args)
            
            # Set up gadgets
            self.g_slider = Slider(self,G_SLIDER)
            self.g_input = WritableField(self,G_INPUT)
            self.g_input2 = WritableField(self,G_INPUT2)
            self.g_output = DisplayField(self,G_OUTPUT)
            
        ## Methods for testing slider ops
        def slider_set_value(self):
            try:
                self.g_slider.value = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int value expected"
        
        def slider_get_value(self):
            self.g_output.value = repr(self.g_slider.value)
            
        def slider_set_lower_bound(self):
            try:
                self.g_slider.lower_bound = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int value expected"
                
        def slider_get_lower_bound(self):
            self.g_output.value = repr(self.g_slider.lower_bound)
            
        def slider_set_upper_bound(self):
            try:
                self.g_slider.upper_bound = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int value expected"
                
        def slider_get_upper_bound(self):
            self.g_output.value = repr(self.g_slider.upper_bound)
            
        def slider_set_step_size(self):
            try:
                self.g_slider.step_size = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int value expected"
        
        def slider_get_step_size(self):
            self.g_output.value = repr(self.g_slider.step_size)
            
        def slider_set_colour(self):
            try:
                fg = int(self.g_input.value)
                bg = int(self.g_input2.value)
            except ValueError as e:
                self.g_output.value = "Err: Input1=int, Input2=int"
            else:
                self.g_slider.colour = (fg, bg)
            
        def slider_get_colour(self):
            fg, bg = self.g_slider.colour
            self.g_output.value = f"fg={fg}, bg={bg}"
        
        # Event handlers for Slider Events
        @toolbox_handler(SliderValueChangedEvent)
        def SliderValueChanged(self,event,id_block,poll_block):
            self.g_output.value = "Slider value change: "+repr(poll_block.new_value)
        
    class SliderMenu(Menu,TestMenu):
        template = "SliderMenu"
        
        ## Slider event handlers
        @toolbox_handler(EvSliderSetValue)
        def SliderSetValue(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_set_value()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderGetValue)
        def SliderGetValue(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_get_value()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderSetLowerBound)
        def SliderSetLowerBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_set_lower_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderGetLowerBound)
        def SliderGetLowerBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_get_lower_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderSetUpperBound)
        def SliderSetUpperBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_set_upper_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderGetUpperBound)
        def SliderGetUpperBound(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_get_upper_bound()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderSetStepSize)
        def SliderSetStepSize(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_set_step_size()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderGetStepSize)
        def SliderGetStepSize(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_get_step_size()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderSetColour)
        def SliderSetColour(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_set_colour()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvSliderGetColour)
        def SliderGetColour(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.slider_get_colour()
            self.menu_tick(id_block.self.component)
    
except ModuleNotFoundError as e:
    Reporter.print("No Draggable object in riscos_toolbox")