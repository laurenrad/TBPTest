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
    
    def __init__(self, *args):
        super().__init__(*args)
        self.fileinfo = toolbox.create_object("FileInfo")
        self.output_text = TextArea(self,FontWindow.G_TEXTAREA)
        self.output_display = DisplayField(self,FontWindow.G_RESULT)
        self.input_int = NumberRange(self,FontWindow.G_INT_INPUT)
        self.input_str = WritableField(self,FontWindow.G_STR_INPUT)
        self.current_test = FontWindow.G_RADIO_DBOX_WINID # currently selected test - set default