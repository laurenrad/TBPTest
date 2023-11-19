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

import swi

from tbptest.reporter import Reporter
from tbptest.tbox_const import *

import riscos_toolbox as toolbox
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler

class MenuMenu(Menu):
    template = "MenuMenu"

class MenuWindow(Window):
    template = "MenuWin"
    
    # Gadget constants
    G_RADIO_START        = 0x0D # First radio button in sequential set
    G_RADIO_END          = 0x1A # Last radio button in sequential set
    G_RADIO_TICK         = 0x0D
    G_RADIO_FADE         = 0x0E
    G_RADIO_ENTRY_TEXT   = 0x0F
    G_RADIO_ENTRY_SPRITE = 0x10
    G_RADIO_SUBMENU_SHOW = 0x11
    G_RADIO_SUBMENU_EV   = 0x12
    G_RADIO_CLICK_SHOW   = 0x13
    G_RADIO_CLICK_EV     = 0x14
    G_RADIO_HELP_MSG     = 0x15
    G_RADIO_ENTRY_HELP   = 0x16
    G_RADIO_HEIGHT       = 0x17
    G_RADIO_WIDTH        = 0x18
    G_RADIO_TITLE        = 0x19
    G_RADIO_ADDREMOVE    = 0x1A
    G_INPUT_INT          = 0x1D # Int input
    G_INPUT_STR          = 0x1C # String input
    G_SET_BTN            = 0x23 # Action button: 'Set'
    G_GET_BTN            = 0x1B # Action button: 'Get'
    G_TEXTAREA           = 0x0B # TextArea output
    G_OUTPUT_INT         = 0x22 # Integer output
    
    def __init__(self, *args):
        super().__init__(*args)
        Reporter.print("Creating menu window")
        
        # Set up gadgets
        self.g_inputint = NumberRange(self,MenuWindow.G_INPUT_INT)
        self.g_inputstr = WritableField(self,MenuWindow.G_INPUT_STR)
        self.g_textarea = TextArea(self,MenuWindow.G_TEXTAREA)
        self.g_outputint = NumberRange(self,MenuWindow.G_OUTPUT_INT)
        self.g_test_tick = RadioButton(self,MenuWindow.G_RADIO_TICK)
        self.g_test_fade = RadioButton(self,MenuWindow.G_RADIO_FADE)
        self.g_test_entrytext = RadioButton(self,MenuWindow.G_RADIO_ENTRY_TEXT)
        self.g_test_entrysprite = RadioButton(self,MenuWindow.G_RADIO_ENTRY_SPRITE)
        self.g_test_submenu_show = RadioButton(self,MenuWindow.G_RADIO_SUBMENU_SHOW)
        self.g_test_submenu_ev = RadioButton(self,MenuWindow.G_RADIO_SUBMENU_EV)
        self.g_test_click_show = RadioButton(self,MenuWindow.G_RADIO_CLICK_SHOW)
        self.g_test_click_ev = RadioButton(self,MenuWindow.G_RADIO_CLICK_EV)
        self.g_test_help_msg = RadioButton(self,MenuWindow.G_RADIO_HELP_MSG)
        self.g_test_entry_help = RadioButton(self,MenuWindow.G_RADIO_ENTRY_HELP)
        self.g_test_height = RadioButton(self,MenuWindow.G_RADIO_HEIGHT)
        self.g_test_width = RadioButton(self,MenuWindow.G_RADIO_WIDTH)
        self.g_test_title = RadioButton(self,MenuWindow.G_RADIO_TITLE)
        self.g_test_addremove = RadioButton(self,MenuWindow.G_RADIO_ADDREMOVE)
        
        self.menu = toolbox.create_object(MenuMenu.template,MenuMenu)
        
        self.selected_test = None
        
     
    # Radio event handler; for fading/unfading elements depending on 
    # the test that's selected.   
    @toolbox_handler(RadioButtonStateChangedEvent)
    def radio_test_change(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False # pass along if it's for a different window
         
        if id_block.self.component == MenuWindow.G_RADIO_TICK:
            self.selected_test = "tick"
            #Reporter.print("tick test")
        elif id_block.self.component == MenuWindow.G_RADIO_FADE:
            self.selected_test = "fade"
            #Reporter.print("fade test")
        elif id_block.self.component == MenuWindow.G_RADIO_ENTRY_TEXT:
            self.selected_test = "entrytext"
            #Reporter.print("entry text test")
        elif id_block.self.component == MenuWindow.G_RADIO_ENTRY_SPRITE:
            self.selected_test = "entrysprite"
            #Reporter.print("entry sprite test")
        elif id_block.self.component == MenuWindow.G_RADIO_SUBMENU_SHOW:
            pass
            #Reporter.print("submenu show test")
        elif id_block.self.component == MenuWindow.G_RADIO_SUBMENU_EV:
            pass
            #Reporter.print("submenu event test")
        elif id_block.self.component == MenuWindow.G_RADIO_CLICK_SHOW:
            pass
            #Reporter.print("click show test")
        elif id_block.self.component == MenuWindow.G_RADIO_CLICK_EV:
            pass
            #Reporter.print("click event test")
        elif id_block.self.component == MenuWindow.G_RADIO_HELP_MSG:
            pass
            #Reporter.print("help message test")
        elif id_block.self.component == MenuWindow.G_RADIO_ENTRY_HELP:
            pass
            #Reporter.print("entry help test")
        elif id_block.self.component == MenuWindow.G_RADIO_HEIGHT:
            pass
            #Reporter.print("height test")
        elif id_block.self.component == MenuWindow.G_RADIO_WIDTH:
            pass
            #Reporter.print("width test")
        elif id_block.self.component == MenuWindow.G_RADIO_TITLE:
            pass
            #Reporter.print("title test")
        elif id_block.self.component == MenuWindow.G_RADIO_ADDREMOVE:
            pass
            #Reporter.print("add / remove test")
        else:
            return False
            
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def action_button_press(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        Reporter.print(f"action press on {id_block.self.component}")       
        if id_block.self.component == MenuWindow.G_SET_BTN:
            Reporter.print("Set btn click")
            if self.g_test_tick.state:
                Reporter.print("test tick")
            elif self.g_test_fade.state:
                Reporter.print("test state")
            elif self.g_test_entrytext.state:
                Reporter.print("test entry text")
            elif self.g_test_entrysprite.state:
                Reporter.print("test entry sprite")
            elif self.g_test_submenu_show.state:
                Reporter.print("test submenu show")
            elif self.g_test_submenu_ev.state:
                Reporter.print("test submenu ev")
            elif self.g_test_click_show.state:
                Reporter.print("test click show")
            elif self.g_test_click_ev.state:
                Reporter.print("test click ev")
            elif self.g_test_help_msg.state:
                Reporter.print("test help msg")
            elif self.g_test_entry_help.state:
                Reporter.print("test entry help")
            elif self.g_test_height.state:
                Reporter.print("test height")
            elif self.g_test_width.state:
                Reporter.print("test width")
            elif self.g_test_title.state:
                self.menu.title = self.g_inputstr.value
                Reporter.print("test title")
            elif self.g_test_addremove.state:
                Reporter.print("test addremove")
        elif id_block.self.component == MenuWindow.G_GET_BTN:
            Reporter.print("Get btn click")
        else:
            return False
            
        return True
             