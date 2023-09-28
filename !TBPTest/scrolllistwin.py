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
from riscos_toolbox.gadgets.scrolllist import ScrollList, ScrollListSelectionEvent
from tbox_const import *
from tbox_common import TestMenu

# Gadget constants
G_SCROLLLIST = 0x01
G_INPUT1     = 0x03
G_INPUT2     = 0x05
G_OUTPUT     = 0x08

class ScrollListWindow(Window):
    template = "ScrlLstWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Set up gadgets
        self.g_scrolllist = ScrollList(self,G_SCROLLLIST)
        self.g_input1 = WritableField(self,G_INPUT1)
        self.g_input2 = WritableField(self,G_INPUT2)
        self.g_output = DisplayField(self,G_OUTPUT)
        
    # Test operations for ScrollList
    def scrolllist_set_state(self):
        try:
            self.g_scrolllist.state = int(self.g_input1.value)
        except ValueError as e:
            self.g_output.value = "Err: expected int in Input 1"
            
    def scrolllist_get_state(self):
        self.g_output.value = repr(self.g_scrolllist.state)
        
    def scrolllist_add_item(self):
        try:
            text = self.g_input1.value
            index = int(self.g_input2.value)
        except ValueError as e:
            self.g_output.value = "Err: Expected str in Input 1, int in Input 2"
        else:
            self.g_scrolllist.add_item(text,index)
        
    def scrolllist_delete_items(self):
        try:
            start = int(self.g_input1.value)
            end = int(self.g_input2.value)
        except ValueError as e:
            self.g_output.value = "Err: Expected int in Input 1, int in Input 2"
        else:
            self.g_scrolllist.delete_items(start,end)
        
    def scrolllist_get_selected(self):
        try:
            offset = int(self.g_input1.value)
        except ValueError as e:
            offset = -1
        self.g_output.value = repr(self.g_scrolllist.get_selected(offset))
        
    def scrolllist_make_visible(self):
        try:
            self.g_scrolllist.make_visible(int(self.g_input1.value))
        except ValueError as e:
            self.g_output.value = "Err: Expected int in Input 1"
            
    def scrolllist_set_multisel(self):
        try:
            self.g_scrolllist.multisel = int(self.g_input1.value)
        except ValueError as e:
            self.g_output.value = "Err: Expected int in Input 1"
            
    def scrolllist_get_multisel(self):
        self.g_output.value = repr(self.g_scrolllist.multisel)
    
    # Event handlers
    @toolbox_handler(ScrollListSelectionEvent)
    def _scrolllist_selection(self,event,id_block,poll_block):
        s= f"Selection: item={poll_block.item}, flags={poll_block.sel_flags}"
        self.g_output.value = s
    
class ScrollListMenu(Menu,TestMenu):
    template = "ScrlLstMenu"
    
    # Menu event handlers
    @toolbox_handler(EvScrollListSetState)
    def _scrolllist_set_state(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_set_state()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListGetState)
    def _scrolllist_get_state(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_get_state()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListAddItem)
    def _scrolllist_add_item(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_add_item()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListDeleteItems)
    def _scrolllist_delete_items(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_delete_items()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListGetSelected)
    def _scrolllist_get_selected(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_get_selected()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListMakeVisible)
    def _scrolllist_make_visible(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_make_visible()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListSetMultisel)
    def _scrolllist_set_multisel(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_set_multisel()
        self.menu_tick(id_block.self.component)
        
    @toolbox_handler(EvScrollListGetMultisel)
    def _scrolllist_get_multisel(self,event,id_block,poll_block):
        window = toolbox.get_object(id_block.ancestor.id)
        window.scrolllist_get_multisel()
        self.menu_tick(id_block.self.component)
