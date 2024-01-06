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

import riscos_toolbox as toolbox
from riscos_toolbox.objects.window import Window
from riscos_toolbox.objects.colourdbox import ColourDbox, ColourDboxAboutToBeShownEvent
from riscos_toolbox.objects.colourdbox import ColourDboxDialogueCompletedEvent
from riscos_toolbox.objects.colourdbox import ColourDboxColourSelectedEvent
from riscos_toolbox.objects.colourmenu import ColourMenu, ColourMenuAboutToBeShownEvent
from riscos_toolbox.objects.colourmenu import ColourMenuHasBeenHiddenEvent, ColourMenuSelectionEvent
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler

class ColourWindow(Window):
    template = "ColourWin"
    
    # Gadget constants
    G_RADIO_DBOX_WIMPHANDLE = 0x11
    G_RADIO_DBOX_HANDLE     = 0x12
    G_RADIO_DBOX_COLOUR     = 0x13
    G_RADIO_DBOX_MODEL      = 0x14
    G_RADIO_DBOX_NONE       = 0x15
    G_RADIO_MENU_COLOUR     = 0x17
    G_RADIO_MENU_NONE       = 0x18
    G_RADIO_MENU_TITLE      = 0x19
    G_SHOW                  = 0x00
    G_GET                   = 0x0C
    G_SET                   = 0x0D
    G_INPUT_INT             = 0x0B
    G_INPUT_STR             = 0x0A
    G_RESULT                = 0x09
    G_TEXTAREA              = 0x08
    
    def __init__(self, *args):
        super().__init__(*args)
        self.colour_menu = toolbox.create_object("ColourMenu")
        self.colour_dbox = toolbox.create_object("ColourDbox")
        self.result = DisplayField(self,ColourWindow.G_RESULT)
        self.textarea = TextArea(self,ColourWindow.G_TEXTAREA)
        self.input_int = NumberRange(self,ColourWindow.G_INPUT_INT)
        self.input_str = WritableField(self,ColourWindow.G_INPUT_STR)
        
        self.selected_test = ColourWindow.G_RADIO_DBOX_WIMPHANDLE
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def test_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
        
        self.selected_test = id_block.self.component
        
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_bloc,poll_block):
        if id_block.self.id != self.id:
            return False
            
        return True
        
    @toolbox_handler(ColourDboxAboutToBeShownEvent)
    def colour_dbox_shown(self,event,id_block,poll_block):
        Reporter.print("ColourDboxAboutToBeShownEvent")
        
    @toolbox_handler(ColourDboxDialogueCompletedEvent)
    def colour_dbox_completed(self,event,id_block,poll_block):
        Reporter.print("ColourDboxDialogueCompletedEvent")
        
    @toolbox_handler(ColourDboxColourSelectedEvent)
    def colour_dbox_selected(self,event,id_block,poll_block):
        Reporter.print("ColourDboxColourSelectedEvent")
        
    @toolbox_handler(ColourMenuAboutToBeShownEvent)
    def colour_menu_shown(self,event,id_block,poll_block):
        Reporter.print("ColourMenuAboutToBeShownEvent")
    
    @toolbox_handler(ColourMenuHasBeenHiddenEvent)
    def colour_menu_hidden(self,event,id_block,poll_block):
        Reporter.print("ColourMenuHasBeenHiddenEvent")
        
    @toolbox_handler(ColourMenuSelectionEvent)
    def colour_menu_selected(self,event,id_block,poll_block):
        Reporter.print("ColourMenuSelectionEvent")
                