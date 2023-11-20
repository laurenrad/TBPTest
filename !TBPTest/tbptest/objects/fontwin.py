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
from riscos_toolbox.objects.fontmenu import FontMenu
from riscos_toolbox.objects.fontdbox import FontDbox, FontDboxAboutToBeShownEvent
from riscos_toolbox.objects.fontdbox import FontDboxApplyFontEvent, FontDboxDialogueCompletedEvent
from riscos_toolbox.objects.fontmenu import FontMenuAboutToBeShownEvent, FontMenuHasBeenHiddenEvent
from riscos_toolbox.objects.fontmenu import FontMenuSelectionEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.events import toolbox_handler

#class TestFontMenu(FontMenu):
#    template = "FontMenu"
    
#class TestFontDbox(FontDbox):
#    template = "FontDbox"

class FontWindow(Window):
    template = "FontWin"
    
    # Gadget constants
    G_TEXTAREA          = 0x01
    G_RESULT            = 0x11
    G_RADIO_DBOX_WINID  = 0x05
    G_RADIO_DBOX_FONT   = 0x06
    G_RADIO_DBOX_SIZE   = 0x07
    G_RADIO_DBOX_ASPECT = 0x13
    G_RADIO_DBOX_TRYSTR = 0x08
    G_RADIO_DBOX_TITLE  = 0x09
    G_RADIO_MENU_FONT   = 0x0B
    G_INT_INPUT         = 0x0C
    G_STR_INPUT         = 0x02
    G_GET               = 0x0E
    G_SET               = 0x0F
    
    def __init__(self, *args):
        super().__init__(*args)
        self.font_menu = toolbox.create_object("FontMenu")
        self.font_dbox = toolbox.create_object("FontDbox")
        self.output_text = TextArea(self,FontWindow.G_TEXTAREA)
        self.output_display = DisplayField(self,FontWindow.G_RESULT)
        self.input_int = NumberRange(self,FontWindow.G_INT_INPUT)
        self.input_str = WritableField(self,FontWindow.G_STR_INPUT)
        self.current_test = FontWindow.G_RADIO_DBOX_WINID # Currently selected test - set default
        self.get_btn = ActionButton(self,FontWindow.G_GET)
        self.set_btn = ActionButton(self,FontWindow.G_SET)
        
        # Some elements will fade and unfade depending on test, so set up defaults
        self.set_btn.faded = True
        self.get_btn.faded = False
        
    # As of the current lib version, this event class implements all fields.
    @toolbox_handler(FontMenuSelectionEvent)
    def font_selected(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font selected from menu | ")
        self.output_text.insert(-1,f"Font id: {poll_block.font_id} | ")
        self.output_text.set_font(poll_block.font_id,200,200)
    
    # As of the current lib version, this event class does not implement the fields.
    @toolbox_handler(FontMenuAboutToBeShownEvent)
    def font_menu_shown(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font menu about to be shown | ")

    # This event doesn't have any fields anyway.        
    @toolbox_handler(FontMenuHasBeenHiddenEvent)
    def font_menu_hidden(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font menu has been hidden | ")
    
    # As of the current lib version, this event class does not implement fields.
    @toolbox_handler(FontDboxAboutToBeShownEvent)
    def font_dbox_shown(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font dbox about to be shown | ")
            
    @toolbox_handler(FontDboxApplyFontEvent)
    def font_dbox_applied(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font dbox apply | ")
        Reporter.print(f"height={poll_block.height} aspect={poll_block.aspect} font={poll_block.font}")
       
    @toolbox_handler(FontDboxDialogueCompletedEvent)
    def font_dbox_completed(self,event,id_block,poll_block):
        self.output_text.insert(-1,"Event: Font dbox completed | ")
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def radiobutton_changed(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        self.current_test = id_block.self.component
        
        # Fade and unfade some elements depending on what is selected
        if self.current_test == FontWindow.G_RADIO_DBOX_WINID:
            self.set_btn.faded = True
            self.get_btn.faded = False
        else:
            self.set_btn.faded = False
            self.get_btn.faded = False
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        if id_block.self.component == FontWindow.G_GET:
            if self.current_test == FontWindow.G_RADIO_DBOX_WINID:
                self.output_display.value = "DBox Win ID: "+repr(self.font_dbox.window_id)
                Reporter.print("test: get dbox winid")
            elif self.current_test == FontWindow.G_RADIO_DBOX_FONT:
                self.output_display.value = "DBox Font: "+self.font_dbox.font
                Reporter.print("test: get dbox font")
            elif self.current_test == FontWindow.G_RADIO_DBOX_SIZE:
                self.output_display.value = "DBox Size: "+repr(self.font_dbox.size)
                Reporter.print("test: get dbox size")
            elif self.current_test == FontWindow.G_RADIO_DBOX_ASPECT:
                self.output_display.value = "DBox Aspect: "+repr(self.font_dbox.aspect)
                Reporter.print("test: get dbox aspect")
            elif self.current_test == FontWindow.G_RADIO_DBOX_TRYSTR:
                self.output_display.value = "DBox Try Str: "+self.font_dbox.try_string
                Reporter.print("test: get dbox try string")
            elif self.current_test == FontWindow.G_RADIO_DBOX_TITLE:
                self.output_display.value = self.font_dbox.title
                Reporter.print("test: get dbox title")
            elif self.current_test == FontWindow.G_RADIO_MENU_FONT:
                self.output_display.value = self.font_menu.font
                Reporter.print("test: get menu font")
            else:
                Reporter.print("test: unknown get")
        elif id_block.self.component == FontWindow.G_SET:
            if self.current_test == FontWindow.G_RADIO_DBOX_FONT:
                Reporter.print("test: set dbox font")
                self.font_dbox.font = self.input_str.value
            elif self.current_test == FontWindow.G_RADIO_DBOX_SIZE:
                self.font_dbox.size = self.input_int.value
                Reporter.print("test: set dbox size")
            elif self.current_test == FontWindow.G_RADIO_DBOX_ASPECT:
                self.font_dbox.aspect = self.input_int.value
                Reporter.print("test: set dbox aspect")
            elif self.current_test == FontWindow.G_RADIO_DBOX_TRYSTR:
                self.font_dbox.try_string = self.input_str.value
                Reporter.print("test: set dbox try string")
            elif self.current_test == FontWindow.G_RADIO_DBOX_TITLE:
                self.font_dbox.title = self.input_str.value
                Reporter.print("test: set dbox title")
            elif self.current_test == FontWindow.G_RADIO_MENU_FONT:
                self.font_menu.font = self.input_str.value
                Reporter.print("test: set menu font")
            else:
                Reporter.print("test: unknown set")
        else:
            return False
            
        return True
    