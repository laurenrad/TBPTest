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

# This is an incomplete draft of ideas for a parent object for creating object tests
# from. The library probably isn't in a state to do that sort of thing yet so they'll
# probably be a little more handmade for now.

import swi

from enum import Enum
from typing import NamedTuple
from typing import Callable

from tbptest.reporter import Reporter

import riscos_toolbox as toolbox
from riscos_toolbox.objects.fileinfo import FileInfo, AboutToBeShownEvent, DialogueCompletedEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.radiobutton import RadioButtonDefinition
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.events import toolbox_handler

# Window.add_gadget appears to be bugged for now, just implement something in here to add 
# radio buttons.
def add_property():
    pass

class GadgetIDs(NamedTuple):
    pass
    
class Property(NamedTuple):
    description: str
    test_get: Callable[..., None]
    test_set: Callable[..., None]
    text: bool = True

class ObjTestWindow(Window):
    template = "ObjTestWin"
    
    # Constants for common gadgets' component IDs
    class Gadgets(Enum):
        INT_INPUT = 0x20
        STR_INPUT = 0x21
        GET = 0x22
        SET = 0x23
        RESULT = 0x24
        EVENTS = 0x25
    
    def __init__(self, *args):
        super().__init__(*args)
        self.event_display = TextArea(self,ObjTestWindow.Gadgets.EVENTS)
        self.result_display = DisplayField(self,ObjTestWindow.Gadgets.RESULT)
        self.input_int = NumberRange(self,ObjTestWindow.Gadgets.INT_INPUT)
        self.input_str = WritableField(self,ObjTestWindow.Gadgets.STR_INPUT)
        self.current_test = None
        self.props = [] # properties
        
    def setup(self,obj_template):
        self.obj = toolbox.create_object(obj_template)
        for prop in self.props:
            r = RadioButtonDefinition(0,prop.description,100,0xFF)
            self.add_gadget(r) # Create radio buttons ...
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def radiobutton_changed(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        self.current_test = id_block.self.component
        
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        return True
        