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
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler

try:
    from riscos_toolbox.gadgets.optionbutton import OptionButton, OptionButtonStateChangedEvent
    
    # Gadget Constants
    G_OPTION   = 0x00
    G_INPUT    = 0x04
    G_INPUTOPT = 0x03
    G_OUTPUT   = 0x05

    class OptionButtonWindow(Window):
        template = "OptButtnWin"
    
        def __init__(self, *args):
            super().__init__(*args)
    
            self.g_option = OptionButton(self,G_OPTION)
            self.g_inputopt = OptionButton(self,G_INPUTOPT)
            self.g_input = WritableField(self,G_INPUT)
            self.g_output = DisplayField(self,G_OUTPUT)
    
        ## Methods for testing OptionButton
        def optbutton_set_label(self):
            self.g_option.label = self.g_input.value
        
        def optbutton_get_label(self):
            self.g_output.value = self.g_option.label
        
        def optbutton_set_event(self):
            # As in various other places, this is because I don't want to depend on 
            # NumberRange since it isn't in upstream riscos_toolbox yet
            try:
                self.g_option.event = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Expected int input"
        
        def optbutton_get_event(self):
            self.g_output.value = repr(self.g_option.event)
        
        def optbutton_set_state(self):
            self.g_option.state = self.g_inputopt.state
        
        def optbutton_get_state(self):
            self.g_output.value = repr(self.g_option.state)
        
        ## Event handlers for OptionButton
        @toolbox_handler(OptionButtonStateChangedEvent)
        def OptButtonStateChanged(self,event,id_block,poll_block):
            self.g_display.value = "Option state changed: "+repr(poll_block.new_state)
    
    class OptionButtonMenu(Menu,TestMenu):
        template = "OptBttnMenu"
    
        ## OptionButton event handlers
        @toolbox_handler(EvOptButtonSetLabel)
        def OptButtonSetLabel(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_set_label()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvOptButtonGetLabel)
        def OptButtonGetLabel(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_get_label()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvOptButtonSetEvent)
        def OptButtonSetEvent(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_set_event()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvOptButtonGetEvent)
        def OptButtonGetEvent(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_get_event()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvOptButtonSetState)
        def OptButtonSetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_set_state()
            self.menu_tick(id_block.self.component)
        
        @toolbox_handler(EvOptButtonGetState)
        def OptButtonGetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.optbutton_get_state()
            self.menu_tick(id_block.self.component)
    
except ModuleNotFoundError as e:
    Reporter.print("No OptionButton object in riscos_toolbox")    
