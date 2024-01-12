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

import riscos_toolbox as toolbox # noqa
from riscos_toolbox.objects.window import Window
from riscos_toolbox.objects.proginfo import ProgInfo, ProgInfoAboutToBeShownEvent
from riscos_toolbox.objects.proginfo import ProgInfoDialogueCompletedEvent
from riscos_toolbox.objects.proginfo import ProgInfoLaunchWebPageEvent
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler


class ProgInfoWindow(Window):
    template = "ProgInfoWin"

    # Gadget constants
    G_RADIO_WIN_ID = 0x01
    G_RADIO_VER = 0x02
    G_RADIO_LICENCE = 0x03
    G_RADIO_TITLE = 0x04
    G_RADIO_URI = 0x05
    G_RADIO_WEB_EV = 0x06
    G_SHOW = 0x00
    G_GET = 0x0C
    G_SET = 0x0D
    G_INPUT_INT = 0x0B
    G_INPUT_STR = 0x0A
    G_RESULT = 0x09
    G_TEXTAREA = 0x08

    def __init__(self, *args):
        super().__init__(*args)
        self.proginfo = toolbox.create_object("ProgInfo")
        self.result = DisplayField(self, ProgInfoWindow.G_RESULT)
        self.textarea = TextArea(self, ProgInfoWindow.G_TEXTAREA)
        self.input_int = NumberRange(self, ProgInfoWindow.G_INPUT_INT)
        self.input_str = WritableField(self, ProgInfoWindow.G_INPUT_STR)

        self.selected_test = ProgInfoWindow.G_RADIO_WIN_ID  # Track which test is selected

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

        if id_block.self.component == ProgInfoWindow.G_SHOW:
            Reporter.print("showing proginfo...")
            self.proginfo.show()
        elif id_block.self.component == ProgInfoWindow.G_GET:
            Reporter.print("get button press")
            if self.selected_test == ProgInfoWindow.G_RADIO_WIN_ID:
                Reporter.print("ProgInfo test: get window id")
                self.result.value = repr(self.proginfo.window_id)
            elif self.selected_test == ProgInfoWindow.G_RADIO_VER:
                Reporter.print("ProgInfo test: get version")
                self.result.value = self.proginfo.version
            elif self.selected_test == ProgInfoWindow.G_RADIO_LICENCE:
                Reporter.print("ProgInfo test: get licence")
                self.result.value = repr(self.proginfo.licence_type)
            elif self.selected_test == ProgInfoWindow.G_RADIO_TITLE:
                Reporter.print("ProgInfo test: get title")
                self.result.value = self.proginfo.title
            elif self.selected_test == ProgInfoWindow.G_RADIO_URI:
                Reporter.print("ProgInfo test: get uri")
                self.result.value = self.proginfo.uri
            elif self.selected_test == ProgInfoWindow.G_RADIO_WEB_EV:
                Reporter.print("ProgInfo test: get web event")
                self.result.value = repr(self.proginfo.web_event)
            else:
                Reporter.print("ProgInfo test: unknown")
        elif id_block.self.component == ProgInfoWindow.G_SET:
            Reporter.print("set button press")
            if self.selected_test == ProgInfoWindow.G_RADIO_VER:
                Reporter.print("ProgInfo test: set version")
                self.proginfo.version = self.input_str.value
            elif self.selected_test == ProgInfoWindow.G_RADIO_LICENCE:
                Reporter.print("ProgInfo test: set licence")
                self.proginfo.licence_type = self.input_int.value
            elif self.selected_test == ProgInfoWindow.G_RADIO_TITLE:
                Reporter.print("ProgInfo test: set title")
                self.proginfo.title = self.input_str.value
            elif self.selected_test == ProgInfoWindow.G_RADIO_URI:
                Reporter.print("ProgInfo test: set uri")
                self.proginfo.uri = self.input_str.value
            elif self.selected_test == ProgInfoWindow.G_RADIO_WEB_EV:
                Reporter.print("ProgInfo test: set web event")
                self.proginfo.web_event = self.input_int.value
        else:
            Reporter.print("unknown button press")
            return False

        return True

    @toolbox_handler(ProgInfoAboutToBeShownEvent)
    def proginfo_shown(self, event, id_block, poll_block):
        Reporter.print("ProgInfoAboutToBeShownEvent")

    @toolbox_handler(ProgInfoDialogueCompletedEvent)
    def proginfo_completed(self, event, id_block, poll_block):
        Reporter.print("ProgInfoDialogueCompletedEvent")

    @toolbox_handler(ProgInfoLaunchWebPageEvent)
    def proginfo_web(self, event, id_block, poll_block):
        Reporter.print("ProgInfoLaunchWebPageEvent")
