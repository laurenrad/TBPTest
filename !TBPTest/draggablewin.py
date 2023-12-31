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
    from riscos_toolbox.gadgets.draggable import Draggable
    from riscos_toolbox.gadgets.draggable import DraggableDragStartedEvent
    from riscos_toolbox.gadgets.draggable import DraggableDragEndedEvent

    # Gadget Constants
    G_DRAGGABLE = 0x00
    G_INPUT     = 0x04
    G_OUTPUT    = 0x05

    class DraggableWindow(Window):
        template = "DrggableWin"
    
        def __init__(self, *args):
            super().__init__(*args)
        
            # Set up gadgets
            self.g_draggable = Draggable(self,G_DRAGGABLE)
            self.g_input = WritableField(self,G_INPUT)
            self.g_output = DisplayField(self,G_OUTPUT)
        
        ## Methods for testing draggable ops
    
        def draggable_get_text(self):
            self.g_output.value = "Draggable text: " + self.g_draggable.text
    
        def draggable_set_text(self):
            self.g_draggable.text = self.g_input.value
        
        def draggable_get_sprite(self):
            self.g_output.value = "Draggable sprite: " + self.g_draggable.sprite

        def draggable_set_sprite(self):
            self.g_draggable.sprite = self.g_input.value
                    
        # Output draggable state to display field
        def draggable_get_state(self):
            self.g_output.value = "Draggable state: " + repr(self.g_draggable.state)
        
        # Set draggable state to whatever is in input field
        def draggable_set_state(self):
            try:
                self.g_draggable.state = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Int value expected"
        
        ## Draggable Event handlers 
    
        # Draggable Drag Started Event
        @toolbox_handler(DraggableDragStartedEvent)
        def DraggableDragStarted(self,event,id_block,poll_block):
            self.g_output.value = "Drag started"
        
        # Draggable Drag Ended Event
        @toolbox_handler(DraggableDragEndedEvent)
        def DraggableDragEnded(self,event,id_block,poll_block):
            self.g_output.value = f"Drag ended: window={poll_block.window_handle} icon={poll_block.icon_handle} x={poll_block.x} y={poll_block.y}"

    class DrgableMenu(Menu,TestMenu):
        template = "DrgableMenu"
    
        ## Draggable Event handlers
        
        # Draggable Get Text
        @toolbox_handler(EvDraggableGetText)
        def DraggableGetText(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_get_text()
            self.menu_tick(id_block.self.component)
        
        # Draggable Set Text
        @toolbox_handler(EvDraggableSetText)
        def DraggableSetText(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_set_text()
            self.menu_tick(id_block.self.component)
        
        # Draggable Get Sprite
        @toolbox_handler(EvDraggableGetSprite)
        def DraggableGetSprite(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_get_sprite()
            self.menu_tick(id_block.self.component)
        
        # Draggable Set Sprite
        @toolbox_handler(EvDraggableSetSprite)
        def DraggableSetSprite(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_set_sprite()
            self.menu_tick(id_block.self.component)
        
        # Draggable Get State
        @toolbox_handler(EvDraggableGetState)
        def DraggableGetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_get_state()
            self.menu_tick(id_block.self.component)
        
        # Draggable Set State
        @toolbox_handler(EvDraggableSetState)
        def DraggableSetState(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.draggable_set_state()
            self.menu_tick(id_block.self.component)
        
            
except ModuleNotFoundError as e:
    Reporter.print("No Draggable object in riscos_toolbox")