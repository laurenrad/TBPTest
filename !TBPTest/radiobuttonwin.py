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
from riscos_toolbox.gadgets.writablefield import WritableField
from tbox_const import *
from tbox_common import TestMenu
try:
    from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
    
    # Gadget Constants
    G_RADIO_A      = 0x00
    G_RADIO_B      = 0x01
    G_INPUT        = 0x04
    G_INPUT_WIDTH  = 0x08
    G_INPUT_HEIGHT = 0x07
    G_OUTPUT       = 0x03
    
    class RadioButtonWindow(Window):
        template = "RadioWin"
        
        def __init__(self, *args):
            super().__init__(*args)
            
            # Set up gadgets
            self.g_radio_a = RadioButton(self,G_RADIO_A)
            self.g_radio_b = RadioButton(self,G_RADIO_B)
            self.g_input   = WritableField(self,G_INPUT)
            self.g_input_w = WritableField(self,G_INPUT_WIDTH)
            self.g_input_h = WritableField(self,G_INPUT_HEIGHT)
            self.g_output  = DisplayField(self,G_OUTPUT)
            
        # Methods for testing RadioButton ops
        def radiobutton_set_label(self):
            self.g_radio_a.label = self.g_input.value
            
        def radiobutton_get_label(self):
            self.g_output.value = self.g_radio_a.label
            
        def radiobutton_set_event(self):
            try:
                self.g_radio_a.event = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int input expected"
                
        def radiobutton_get_event(self):
            self.g_output.value = repr(self.g_radio_a.event)
            
        def radiobutton_set_state(self):
            try:
                self.g_radio_a.state = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int input expected"
                
        def radiobutton_get_state(self):
            self.g_output.value = repr(self.g_radio_a.state)
            
        def radiobutton_set_font(self):
            font_name = self.g_input.value
            try:
                w = int(self.g_input_w.value)
                h = int(self.g_input_h.value)
            except ValueError as e:
                self.g_output.value = "Err: int input expected"
            else:
                self.g_radio_a.set_font(font_name,w,h)
                
        # RadioButton event handlers
        @toolbox_handler(RadioButtonStateChangedEvent)
        def StateChanged(self,event,id_block,poll_block):
            s = f"State changed: {poll_block.state} {poll_block.old_on_button}"
            self.g_output.value = s
        
        
    class RadioButtonMenu(Menu,TestMenu):
        template = "RadioMenu"
        
        # RadioButton Event handlers
        @toolbox_handler(EvRadioButtonSetLabel)
        def RadioButtonSetLabel(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_set_label()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonGetLabel)
        def RadioButtonGetLabel(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_get_label()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonSetEvent)
        def RadioButtonSetEvent(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_set_event()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonGetEvent)
        def RadioButtonGetEvent(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_get_event()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonSetState)
        def RadioButtonSetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_set_state()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonGetState)
        def RadioButtonGetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_get_state()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvRadioButtonSetFont)
        def RadioButtonSetFont(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.radiobutton_set_font()
            self.menu_tick(id_block.self.component)
    
except ModuleNotFoundError as e:
    Reporter.print("No RadioButton in riscos_toolbox")