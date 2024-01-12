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
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.gadgets.adjuster import Adjuster, AdjusterClickedEvent
from riscos_toolbox.gadgets.optionbutton import OptionButton

# Gadget Constants
G_ADJ_LEFT = 0x00
G_ADJ_RIGHT = 0x01
G_ADJ_UP = 0x02
G_ADJ_DOWN = 0x03
G_OUTPUT = 0x05
G_RADIO_UP = 0x08
G_RADIO_DOWN = 0x09


class AdjusterWindow(Window):
    template = "AdjusterWin"

    def __init__(self, *args):
        super().__init__(*args)

        # set up gadgets
        # i don't really have to create Adjuster instances for this test, but
        # just to be thorough
        self.g_adj_left = Adjuster(self, G_ADJ_LEFT)
        self.g_adj_right = Adjuster(self, G_ADJ_RIGHT)
        self.g_adj_up = Adjuster(self, G_ADJ_UP)
        self.g_adj_down = Adjuster(self, G_ADJ_DOWN)
        self.g_output = DisplayField(self, G_OUTPUT)
        self.g_up = OptionButton(self, G_RADIO_UP)
        self.g_down = OptionButton(self, G_RADIO_DOWN)

    # Event handler for Adjuster
    @toolbox_handler(AdjusterClickedEvent)
    def AdjusterClicked(self, event, id_block, poll_block):
        s = f"Adjuster click. Direction = {poll_block.direction}"
        self.g_output.value = s
        # The newer version has added a couple extra properties that will for now
        # be represented with these OptionButtons
        self.g_down.state = 0
        self.g_up.state = 0
        if poll_block.down:
            self.g_down.state = 1

        if poll_block.up:
            self.g_up.state = 1
