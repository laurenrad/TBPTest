
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
    from riscos_toolbox.gadgets.popup import PopUp, PopUpAboutToBeShownEvent
except ModuleNotFoundError as e:
    Reporter.print("No PopUp in risos_toolbox")
else:
    # Gadget constants
    G_POPUP  = 0x01
    G_INPUT  = 0x02
    G_OUTPUT = 0x04
    
    class PopUpWin(Window):
        template = "PopUpWin"
        
        def __init__(self, *args):
            super().__init__(*args)
            
            # Set up gadgets
            self.g_popup = PopUp(self,G_POPUP)
            self.g_input = WritableField(self,G_INPUT)
            self.g_output = DisplayField(self,G_OUTPUT)
            
        # Methods for testing PopUp
        def popup_set_menu(self):
            try:
                self.g_popup.menu = int(self.g_input.value)
            except ValueError as e:
                self.g_output.value = "Err: int input expected"
        
        def popup_get_menu(self):
            self.g_output.value = repr(self.g_popup.menu)
        
        # Event handlers for PopUp
        @toolbox_handler(PopUpAboutToBeShownEvent)
        def _popup_about_to_be_shown(self,event,id_block,poll_block):
            self.g_output.value = f"AboutToBeShown: {poll_block.menu_id}"
        
    class PopUpMenu(Menu,TestMenu):
        template = "PopUpMenu"
        
        # Event handlers
        @toolbox_handler(EvPopUpSetMenu)
        def _popup_set_menu(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.popup_set_menu()
            self.menu_tick(id_block.self.component)
            
        @toolbox_handler(EvPopUpGetMenu)
        def _popup_get_menu(self,event,id_block,poll_block):
            window = toolbox.get_object(id_block.ancestor.id)
            window.popup_get_menu()
            self.menu_tick(id_block.self.component)
