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
from riscos_toolbox.objects.fileinfo import FileInfo, AboutToBeShownEvent, DialogueCompletedEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.events import toolbox_handler

class FileInfoWindow(Window):
    template = "FileInfoWin"
    
    # Gadget Constants
    G_RADIO_WINID    = 0x03
    G_RADIO_MODIFIED = 0x04
    G_RADIO_FILETYPE = 0x05
    G_RADIO_FILENAME = 0x06
    G_RADIO_FILESIZE = 0x07
    G_RADIO_DATE     = 0x08
    G_RADIO_TITLE    = 0x09
    G_INT_INPUT      = 0x0C
    G_STR_INPUT      = 0x02
    G_GET            = 0x0E
    G_SET            = 0x0F
    G_RESULT         = 0x11
    G_TEXTAREA       = 0x01
    G_HIDE           = 0x14
    
    def __init__(self, *args):
        super().__init__(*args)
        self.fileinfo = toolbox.create_object("FileInfo",FileInfo)
        self.output_text = TextArea(self,FileInfoWindow.G_TEXTAREA)
        self.output_display = DisplayField(self,FileInfoWindow.G_RESULT)
        self.input_int = NumberRange(self,FileInfoWindow.G_INT_INPUT)
        self.input_str = WritableField(self,FileInfoWindow.G_STR_INPUT)
        self.current_test = FileInfoWindow.G_RADIO_WINID # currently selected test - set default
        self.get_btn = ActionButton(self,FileInfoWindow.G_GET)
        self.set_btn = ActionButton(self,FileInfoWindow.G_SET)
        
        self.get_btn.faded = False
        self.set_btn.faded = True
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def radiobutton_changed(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        self.current_test = id_block.self.component
        
        # Fade and unfade some elements depending on what is selected
        if self.current_test == FileInfoWindow.G_RADIO_WINID:
            self.set_btn.faded = True
            self.get_btn.faded = False
        else:
            self.set_btn.faded = False
            self.get_btn.faded = False
            
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        if id_block.self.component == FileInfoWindow.G_GET:
            if self.current_test == FileInfoWindow.G_RADIO_WINID:
                Reporter.print("test: fileinfo: get winid")
                self.output_display.value = repr(self.fileinfo.window_id)
            elif self.current_test == FileInfoWindow.G_RADIO_MODIFIED:
                Reporter.print("test: fileinfo: get modified")
                self.output_display.value = repr(self.fileinfo.modified)
            elif self.current_test == FileInfoWindow.G_RADIO_FILETYPE:
                Reporter.print("test: fileinfo: get filetype")
                self.output_display.value = hex(self.fileinfo.file_type)
            elif self.current_test == FileInfoWindow.G_RADIO_FILENAME:
                Reporter.print("test: fileinfo: get filename")
                self.output_display.value = self.fileinfo.file_name
            elif self.current_test == FileInfoWindow.G_RADIO_FILESIZE:
                Reporter.print("test: fileinfo: get filesize")
                self.output_display.value = repr(self.fileinfo.file_size)
            elif self.current_test == FileInfoWindow.G_RADIO_DATE:
                Reporter.print("test: fileinfo: get date")
                self.output_display.value = repr(self.fileinfo.date)
            elif self.current_test == FileInfoWindow.G_RADIO_TITLE:
                Reporter.print("test: fileinfo: get title")
                self.output_display.value = self.fileinfo.title
            else:
                Reporter.print("FileInfo window: unknown test")
        elif id_block.self.component == FileInfoWindow.G_SET:
            if self.current_test == FileInfoWindow.G_RADIO_MODIFIED:
                Reporter.print("test: fileinfo: set modified")
                self.fileinfo.modified = self.input_int.value
            elif self.current_test == FileInfoWindow.G_RADIO_FILETYPE:
                Reporter.print("test: fileinfo: set filetype")
                self.fileinfo.file_type = self.input_int.value
            elif self.current_test == FileInfoWindow.G_RADIO_FILENAME:
                Reporter.print("test: fileinfo: set filename")
                self.fileinfo.file_name = self.input_str.value
            elif self.current_test == FileInfoWindow.G_RADIO_FILESIZE:
                Reporter.print("test: fileinfo: set filesize")
                self.fileinfo.file_size = self.input_int.value
            elif self.current_test == FileInfoWindow.G_RADIO_DATE:
                Reporter.print("test: fileinfo: set date")
                self.fileinfo.date = self.input_int.value
            elif self.current_test == FileInfoWindow.G_RADIO_TITLE:
                Reporter.print("test: fileinfo: set title")
                self.fileinfo.title = self.input_str.value
            else:
                Reporter.print("FileInfo window: unknown test")
        elif id_block.self.component == FileInfoWindow.G_HIDE:
            self.fileinfo.hide()
        else:
            return False
            
        return True
    
    @toolbox_handler(AboutToBeShownEvent)
    def fileinfo_onshow(self,event,id_block,poll_block):
        Reporter.print("FileInfo: about to show")
        self.output_text.insert(-1,"FileInfo AboutToBeShownEvent |")
        
    @toolbox_handler(DialogueCompletedEvent)
    def fileinfo_completed(self,event,id_block,poll_block):
        Reporter.print("FileInfo: completed")
        self.output_text.insert(-1,"FileInfo DialogueCompletedEvent |")