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
from riscos_toolbox.objects.quit import Quit, QuitAboutToBeShownEvent, QuitQuitEvent
from riscos_toolbox.objects.quit import QuitDialogueCompletedEvent, QuitCancelEvent
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler

class QuitWindow(Window):
    template = "QuitWin"
    
    # Gadget constants
    G_RADIO_WIN_ID  = 0x11
    G_RADIO_MESSAGE = 0x12
    G_RADIO_TITLE   = 0x13
    G_SHOW          = 0x00
    G_GET           = 0x0C
    G_SET           = 0x0D
    G_INPUT_INT     = 0x0B
    G_INPUT_STR     = 0x0A
    G_RESULT        = 0x09
    G_TEXTAREA      = 0x08
    
    def __init__(self, *args):
        super().__init__(*args)
        self.quit = toolbox.create_object("Quit")
        self.result = DisplayField(self,QuitWindow.G_RESULT)
        self.textarea = TextArea(self,QuitWindow.G_TEXTAREA)
        self.input_int = NumberRange(self,QuitWindow.G_INPUT_INT)
        self.input_str = WritableField(self,QuitWindow.G_INPUT_STR)
        
        self.selected_test = QuitWindow.G_RADIO_WIN_ID
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def test_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
        
        self.selected_test = id_block.self.component
        
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        if id_block.self.component == QuitWindow.G_SHOW:
            self.quit.show()
        elif id_block.self.component == QuitWindow.G_GET:
            if self.selected_test == QuitWindow.G_RADIO_WIN_ID:
                Reporter.print("test: quit: get window id")
                self.result.value = repr(self.quit.window_id)+" ("+hex(self.quit.window_id)+")"
            elif self.selected_test == QuitWindow.G_RADIO_MESSAGE:
                Reporter.print("test: quit: get message")
                self.result.value = self.quit.message
            elif self.selected_test == QuitWindow.G_RADIO_TITLE:
                Reporter.print("test: quit: get title")
                self.result.value = self.quit.title
            else:
                Reporter.print("test: quit: unknown get test")
        elif id_block.self.component == QuitWindow.G_SET:
            if self.selected_test == QuitWindow.G_RADIO_MESSAGE:
                Reporter.print("test: quit: set message")
                self.quit.message = self.input_str.value
            elif self.selected_test == QuitWindow.G_RADIO_TITLE:
                Reporter.print("test: quit: set title")
                self.quit.title = self.input_str.value
            else:
                Reporter.print("test: quit: unknown set test")
        else:
            return False
            
        return True
        
    @toolbox_handler(QuitAboutToBeShownEvent)
    def quit_shown(self,event,id_block,poll_block):
        Reporter.print("QuitAboutToBeShownEvent")
        
        self.textarea.insert(-1,"QuitAboutToBeShown | ")
        
        return True
        
    @toolbox_handler(QuitQuitEvent)
    def quit_quit(self,event,id_block,poll_block):
        Reporter.print("QuitQuitEvent")
        
        self.textarea.insert(-1,"QuitQuitEvent | ")
        
        return True
        
    @toolbox_handler(QuitDialogueCompletedEvent)
    def quit_completed(self,event,id_block,poll_block):
        Reporter.print("QuitDialogueCompletedEvent")
        
        self.textarea.insert(-1,"QuitDialogueCompletedEvent | ")
        
        return True
        
    @toolbox_handler(QuitCancelEvent)
    def quit_cancel(self,event,id_block,poll_block):
        Reporter.print("QuitCancelEvent")
        
        self.textarea.insert(-1, "QuitCancelEvent | ")
        
        return True
        