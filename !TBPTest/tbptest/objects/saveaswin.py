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

from tbptest.reporter import Reporter # noqa

import riscos_toolbox as toolbox # noqa
from riscos_toolbox.objects.saveas import SaveAs, SaveAsAboutToBeShownEvent
from riscos_toolbox.objects.saveas import SaveAsDialogueCompletedEvent, SaveAsSaveToFileEvent
from riscos_toolbox.objects.saveas import FillBufferEvent, SaveAsSaveCompletedEvent
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.events import toolbox_handler


class SaveAsWindow(Window):
    template = "SaveAsWin"

    # Gadget constants
    G_TEXTAREA = 0x08
    G_RESULT = 0x09
    G_INPUT_STR = 0x0A
    G_INPUT_INT = 0x0B
    G_SHOW = 0x00
    G_GET = 0x0C
    G_SET = 0x0D
    G_RADIO_WIN_ID = 0x11
    G_RADIO_TITLE = 0x12
    G_RADIO_FILENAME = 0x13
    G_RADIO_FILETYPE = 0x14
    G_RADIO_FILESIZE = 0x15
    G_RADIO_SEL_AVAILABLE = 0x16
    G_RADIO_DATA_ADDR = 0x17
    G_RADIO_BUFFER_FILLED = 0x18
    G_RADIO_SAVE_COMPLETED = 0x19

    def __init__(self, *args):
        super().__init__(*args)
        self.saveas = toolbox.create_object("SaveAs1")
        self.savemenu = toolbox.create_object("SaveMenu")
        # Until menu stuff is worked out, this is adding the submenu action manually
        swi.swi("Toolbox_ObjectMiscOp", "0i8ii", self.savemenu.id, 0, self.saveas.id)
        self.menu_id = self.savemenu.id
        self.result = DisplayField(self, SaveAsWindow.G_RESULT)
        self.textarea = TextArea(self, SaveAsWindow.G_TEXTAREA)
        self.input_int = NumberRange(self, SaveAsWindow.G_INPUT_INT)
        self.input_str = WritableField(self, SaveAsWindow.G_INPUT_STR)

        self.selected_test = SaveAsWindow.G_RADIO_WIN_ID

    @toolbox_handler(RadioButtonStateChangedEvent)
    def test_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        self.selected_test = id_block.self.component

        return True

    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self, event, id_block, poll_block):
        if id_block.self.id != self.id:
            return False

        if id_block.self.component == SaveAsWindow.G_SHOW:
            self.saveas.show()
        elif id_block.self.component == SaveAsWindow.G_GET:
            if self.selected_test == SaveAsWindow.G_RADIO_WIN_ID:
                Reporter.print("test: saveas: get window id")
                self.result.value = repr(self.saveas.window_id)+" ("+hex(self.saveas.window_id)+")"
            elif self.selected_test == SaveAsWindow.G_RADIO_TITLE:
                Reporter.print("test: saveas: get title")
                self.result.value = self.saveas.title
            elif self.selected_test == SaveAsWindow.G_RADIO_FILENAME:
                Reporter.print("test: saveas: get filename")
                self.result.value = self.saveas.file_name
            elif self.selected_test == SaveAsWindow.G_RADIO_FILETYPE:
                Reporter.print("test: saveas: get filetype")
                self.result.value = hex(self.saveas.file_type)
            elif self.selected_test == SaveAsWindow.G_RADIO_FILESIZE:
                Reporter.print("test: saveas: get filesize")
                self.result.value = repr(self.saveas.file_size)
            elif self.selected_test == SaveAsWindow.G_RADIO_SEL_AVAILABLE:
                Reporter.print("test: saveas: get selection available")
            elif self.selected_test == SaveAsWindow.G_RADIO_DATA_ADDR:
                Reporter.print("test: saveas: get data addr")
            elif self.selected_test == SaveAsWindow.G_RADIO_BUFFER_FILLED:
                Reporter.print("test: saveas: get buffer filled")
            elif self.selected_test == SaveAsWindow.G_RADIO_SAVE_COMPLETED:
                Reporter.print("test: saveas: get radios save completed")
            else:
                Reporter.print("test: saveas: unknown get test")
        elif id_block.self.component == SaveAsWindow.G_SET:
            if self.selected_test == SaveAsWindow.G_RADIO_TITLE:
                Reporter.print("test: saveas: set title")
                self.saveas.title = self.input_str.value
            elif self.selected_test == SaveAsWindow.G_RADIO_FILENAME:
                Reporter.print("test: saveas: set filename")
                self.saveas.file_name = self.input_str.value
            elif self.selected_test == SaveAsWindow.G_RADIO_FILETYPE:
                Reporter.print("test: saveas: set filetype")
                self.saveas.file_type = self.input_int.value
            elif self.selected_test == SaveAsWindow.G_RADIO_FILESIZE:
                Reporter.print("test: saveas: set filesize")
                self.saveas.file_size = self.input_int.value
            elif self.selected_test == SaveAsWindow.G_RADIO_SEL_AVAILABLE:
                Reporter.print("test: saveas: set selection available")
                self.saveas.selection_available(self.input_int.value)
            elif self.selected_test == SaveAsWindow.G_RADIO_DATA_ADDR:
                Reporter.print("test: saveas: set data addr")
            elif self.selected_test == SaveAsWindow.G_RADIO_BUFFER_FILLED:
                Reporter.print("test: saveas: set buffer filled")
            elif self.selected_test == SaveAsWindow.G_RADIO_SAVE_COMPLETED:
                Reporter.print("test: saveas: set save completed")
            else:
                Reporter.print("test: saveas: unknown set test")
        else:
            return False

        return True

    @toolbox_handler(SaveAsAboutToBeShownEvent)
    def saveas_shown(self, event, id_block, poll_block):
        Reporter.print("SaveAsAboutToBeShownEvent")

        self.textarea.insert(-1, "SaveAsAboutToBeShownEvent | ")

        return True

    @toolbox_handler(SaveAsDialogueCompletedEvent)
    def dialogue_completed(self, event, id_block, poll_block):
        Reporter.print("SaveAsDialogueCompletedEvent")

        self.textarea.insert(-1, "SaveAsDialogueCompletedEvent | ")

        return True

    @toolbox_handler(SaveAsSaveToFileEvent)
    def saveas_save(self, event, id_block, poll_block):
        Reporter.print("SaveAsSaveToFileEvent")

        self.textarea.insert(-1, "SaveAsSaveToFileEvent | ")

        return True

    @toolbox_handler(FillBufferEvent)
    def buffer_fill(self, event, id_block, poll_block):
        Reporter.print("FillBufferEvent")

        self.textarea.insert(-1, "FillBufferEvent | ")

        return True

    @toolbox_handler(SaveAsSaveCompletedEvent)
    def save_completed(self, event, id_block, poll_block):
        Reporter.print("SaveAsSaveCompletedEvent | ")

        self.textarea.insert(-1, "SaveAsSaveCompletedEvent | ")

        return True
