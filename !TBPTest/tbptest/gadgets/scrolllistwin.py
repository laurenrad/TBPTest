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
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu, SelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.scrolllist import ScrollList, ScrollListSelectionEvent

# Gadget constants
G_SCROLLLIST = 0x01
G_INPUT1     = 0x03
G_INPUT2     = 0x05
G_INPUT3     = 0x0B
G_OUTPUT     = 0x08


class ScrollListWindow(Window):
    template = "ScrlLstWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Set up gadgets
        self.g_scrolllist = ScrollList(self,G_SCROLLLIST)
        self.g_input1 = WritableField(self,G_INPUT1)
        self.g_input2 = WritableField(self,G_INPUT2)
        self.g_input3 = WritableField(self,G_INPUT3)
        self.g_output = DisplayField(self,G_OUTPUT)
        
    # Test operations for ScrollList
    def scrolllist_set_state(self):
        try:
            self.g_scrolllist.state = int(self.g_input1.value)
        except ValueError:
            self.g_output.value = "Err: expected int in Input 1"
            
    def scrolllist_get_state(self):
        self.g_output.value = repr(self.g_scrolllist.state)
        
    def scrolllist_add_item(self):
        try:
            text = self.g_input1.value
            index = int(self.g_input2.value)
        except ValueError:
            self.g_output.value = "Err: Expected str in Input 1, int in Input 2"
        else:
            self.g_scrolllist.add_item(text,index)
        
    def scrolllist_delete_items(self):
        try:
            start = int(self.g_input1.value)
            end = int(self.g_input2.value)
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1, int in Input 2"
        else:
            self.g_scrolllist.delete_items(start,end)
        
    def scrolllist_get_selected(self):
        try:
            offset = int(self.g_input1.value)
        except ValueError:
            offset = -1
        self.g_output.value = repr(self.g_scrolllist.get_selected(offset))
        
    def scrolllist_make_visible(self):
        try:
            self.g_scrolllist.make_visible(int(self.g_input1.value))
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1"
            
    def scrolllist_set_multisel(self):
        try:
            self.g_scrolllist.multisel = int(self.g_input1.value)
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1"
            
    def scrolllist_get_multisel(self):
        self.g_output.value = repr(self.g_scrolllist.multisel)
        
    def scrolllist_set_colour(self):
        try:
            fg = int(self.g_input1.value)
            bg = int(self.g_input2.value)
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1+2"
        else:
            self.g_scrolllist.colour = (fg,bg)
        
    def scrolllist_get_colour(self):
        fg, bg = self.g_scrolllist.colour
        self.g_output.value = f"fg={hex(fg)}, bg={hex(bg)}"
        
    def scrolllist_set_item_text(self):
        text = self.g_input2.value
        try:
            index = int(self.g_input1.value)
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1"
        else:
            self.g_scrolllist.set_item_text(index,text)
            
    def scrolllist_get_item_text(self):
        try:
            index = int(self.g_input1.value)
        except ValueError:
            self.g_output.value = "Err: Expected int in Input 1"
        else:
            self.g_output.value = self.g_scrolllist.get_item_text(index)
        
    def scrolllist_select_item(self):
        try:
            index = int(self.g_input1.value)
            all = int(self.g_input2.value)
            send_event = int(self.g_input3.value)
            self.g_scrolllist.select_item(index,all,send_event)
        except ValueError:
            self.g_output.value = "Err: Expected ints"
            
    def scrolllist_deselect_item(self):
        try:
            index = int(self.g_input1.value)
            all = int(self.g_input2.value)
            send_event = int(self.g_input3.value)
            self.g_scrolllist.deselect_item(index,all,send_event)
        except ValueError:
            self.g_output.value = "Err: Expected ints"
        
    def scrolllist_count_items(self):
        self.g_output.value = repr(self.g_scrolllist.count_items())
        
    def scrolllist_set_font(self):
        name = self.g_input1.value
        try:
            width = int(self.g_input2.value)
            height = int(self.g_input3.value)
        except ValueError:
            self.g_output.value = "Err: Expected in in Input 2 and 3"
        else:
            self.g_scrolllist.set_font(name,width,height)
            
    def scrolllist_populate(self):
        items = ('Nashville', 'Seattle', 'El Paso', 'Los Angeles', 'Portland',
                 'New York', 'Chicago', 'Atlanta', 'San Francisco', 'San Diego',
                 'Boston', 'Washington D.C.', 'Dallas', 'Houston', 'Denver')
        for item in items:
            self.g_scrolllist.add_item(item,-1)
    
    # Event handlers
    @toolbox_handler(ScrollListSelectionEvent)
    def _scrolllist_selection(self,event,id_block,poll_block):
        s= f"Selection: item={poll_block.item}, flags={poll_block.sel_flags}"
        self.g_output.value = s
    
class ScrollListMenu(Menu,TestMenu):
    template = "ScrlLstMenu"
    
    # Entry constants
    ENTRY_POPULATE     = 0x10
    ENTRY_SET_STATE    = 0x00
    ENTRY_GET_STATE    = 0x01
    ENTRY_ADD_ITEM     = 0x02
    ENTRY_DELETE_ITEMS = 0x03
    ENTRY_GET_SELECTED = 0x04
    ENTRY_MAKE_VISIBLE = 0x05
    ENTRY_SET_MULTISEL = 0x06
    ENTRY_GET_MULTISEL = 0x07
    # The remaining entries aren't implemented in riscos-toolbox yet but
    # are being left in faded for future testing of these features.
    ENTRY_SET_COLOUR   = 0x08
    ENTRY_GET_COLOUR   = 0x09
    ENTRY_COUNT_ITEMS  = 0x0A
    ENTRY_GET_TEXT     = 0x0B
    ENTRY_SET_TEXT     = 0x0C
    ENTRY_SELECT_ITEM  = 0x0D
    ENTRY_DESELECT     = 0x0E
    ENTRY_SET_FONT     = 0x0F
    
    @toolbox_handler(SelectionEvent)
    def menu_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        window = toolbox.get_object(id_block.parent.id)
        self.menu_tick(id_block.self.component)
        
        if id_block.self.component == ScrollListMenu.ENTRY_POPULATE:
            window.scrolllist_populate()
        elif id_block.self.component == ScrollListMenu.ENTRY_SET_STATE:
            window.scrolllist_set_state()
        elif id_block.self.component == ScrollListMenu.ENTRY_GET_STATE:
            window.scrolllist_get_state()
        elif id_block.self.component == ScrollListMenu.ENTRY_ADD_ITEM:
            window.scrolllist_add_item()
        elif id_block.self.component == ScrollListMenu.ENTRY_DELETE_ITEMS:
            window.scrolllist_delete_items()
        elif id_block.self.component == ScrollListMenu.ENTRY_GET_SELECTED:
            window.scrolllist_get_selected()
        elif id_block.self.component == ScrollListMenu.ENTRY_MAKE_VISIBLE:
            window.scrolllist_make_visible()
        elif id_block.self.component == ScrollListMenu.ENTRY_SET_MULTISEL:
            window.scrolllist_set_multisel()
        elif id_block.self.component == ScrollListMenu.ENTRY_GET_MULTISEL:
            window.scrolllist_get_multisel()
        elif id_block.self.component == ScrollListMenu.ENTRY_SET_COLOUR:
            window.scrolllist_set_colour()
        elif id_block.self.component == ScrollListMenu.ENTRY_GET_COLOUR:
            window.scrolllist_get_colour()
        elif id_block.self.component == ScrollListMenu.ENTRY_COUNT_ITEMS:
            window.scrolllist_count_items()
        elif id_block.self.component == ScrollListMenu.ENTRY_GET_TEXT:
            window.scrolllist_get_item_text()
        elif id_block.self.component == ScrollListMenu.ENTRY_SET_TEXT:
            window.scrolllist_set_item_text()
        elif id_block.self.component == ScrollListMenu.ENTRY_SELECT_ITEM:
            window.scrolllist_select_item()
        elif id_block.self.component == ScrollListMenu.ENTRY_DESELECT:
            window.scrolllist_deselect_item()
        elif id_block.self.component == ScrollListMenu.ENTRY_SET_FONT:
            window.scrolllist_set_font()
            
        return True
