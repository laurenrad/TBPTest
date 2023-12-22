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

# This file is for constants for Toolbox events.
# The rationale behind having a central module for this is so they don't clash.

# Constants - Events
EvTextAreaGetState           = 0x200
EvTextAreaSetState           = 0x201
EvTextAreaSetText            = 0x202
EvTextAreaGetText            = 0x203
EvTextAreaInsertText         = 0x204
EvTextAreaReplaceText        = 0x205
EvTextAreaGetSelection       = 0x206
EvTextAreaSetSelection       = 0x207
EvTextAreaGetSelectionPoints = 0x208
EvTextAreaSetSelectionPoints = 0x209 
EvTextAreaSetFont            = 0x20A
EvTextAreaSetColour          = 0x20B
EvTextAreaGetColour          = 0x20C
EvTextAreaSetCursorPos       = 0x20D
EvTextAreaGetCursorPos       = 0x20E

# Event Constants
EvDraggableSetSprite   = 0x300
EvDraggableGetSprite   = 0x301
EvDraggableSetText     = 0x302
EvDraggableGetText     = 0x303
EvDraggableSetState    = 0x304
EvDraggableGetState    = 0x305
EvDraggableDragStarted = 0x82887 # Raised by the Toolbox
EvDraggableDragEnded   = 0x82888 # Raised by the toolbox

## Here are the events for the gadgets which already existed before I worked on it

# Action button test events
EvActionButtonSetText       = 0x800
EvActionButtonGetText       = 0x801
EvActionButtonSetEvent      = 0x802
EvActionButtonGetEvent      = 0x803
EvActionButtonSetClickShow  = 0x804
EvActionButtonGetClickShow  = 0x805
