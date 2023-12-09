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
from riscos_toolbox.objects.scale import Scale, ScaleAboutToBeShownEvent
from riscos_toolbox.objects.scale import ScaleDialogueCompletedEvent, ScaleApplyFactorEvent
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler

class ScaleWindow(Window):
    template = "ScaleWin"
    
    # Gadget constants
    G_RADIO_WIN_ID  = 0x11
    G_RADIO_VALUE   = 0x12
    G_RADIO_BOUNDS  = 0x13
    G_RADIO_TITLE   = 0x14
    G_SHOW          = 0x00
    G_GET           = 0x0C
    G_SET           = 0x0D
    G_INPUT_INT     = 0x0B
    G_INPUT_STR     = 0x0A
    G_RESULT        = 0x09
    G_TEXTAREA	    = 0x08
    
    def __init__(self, *args):
    	super().__init__(*args)
    	self.scale = toolbox.create_object("Scale")