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

# Number range test events
EvNumRangeSetValue          = 0x400
EvNumRangeGetValue          = 0x401
EvNumRangeSetLowerBound     = 0x402
EvNumRangeGetLowerBound     = 0x403
EvNumRangeSetUpperBound     = 0x404
EvNumRangeGetUpperBound     = 0x405
EvNumRangeSetStepSize       = 0x406
EvNumRangeGetStepSize       = 0x407
EvNumRangeSetPrecision      = 0x408
EvNumRangeGetPrecision      = 0x409
EvNumRangeGetNumeric        = 0x40A
EvNumRangeGetLeftAdj        = 0x40B
EvNumRangeGetRightAdj       = 0x40C
EvNumRangeGetSlider         = 0x40D
# Number range events (Raised by Toolbox)
EvNumRngeValueChanged       = 0x8288D

# Option button test events
EvOptButtonSetLabel         = 0x500
EvOptButtonGetLabel         = 0x501
EvOptButtonSetEvent         = 0x502
EvOptButtonGetEvent         = 0x503
EvOptButtonSetState         = 0x504
EvOptButtonGetState         = 0x505
# Option button events (Raised by Toolbox)
EvOptButtonStateChanged     = 0x82882

## Here are the events for the gadgets which already existed before I worked on it

# Display field test events
EvDisplayFieldSetValue      = 0x600
EvDisplayFieldGetValue      = 0x601

# Writable field test events
EvWritableFieldSetText      = 0x700
EvWritableFieldGetText      = 0x701
EvWritableFieldSetAllow     = 0x702
EvWritableFieldGetAllow     = 0x703

# Action button test events
EvActionButtonSetText       = 0x800
EvActionButtonGetText       = 0x801
EvActionButtonSetEvent      = 0x802
EvActionButtonGetEvent      = 0x803
EvActionButtonSetClickShow  = 0x804
EvActionButtonGetClickShow  = 0x805
# Action button events (Raised by Toolbox)
EvActionButtonSelected      = 0x82881

# Button test events
EvButtonSetFlags            = 0x900
EvButtonGetFlags            = 0x901
EvButtonSetValue            = 0x902
EvButtonGetValue            = 0x903
EvButtonSetValidation       = 0x904
EvButtonGetValidation       = 0x905
EvButtonSetFont             = 0x906
EvButtonGetFont             = 0x907

# Scroll List test events - these aren't to be implemented yet
EvScrollListSetState         = 0xA00
EvScrollListGetState         = 0xA01
EvScrollListAddItem          = 0xA02
EvScrollListDeleteItems      = 0xA03
EvScrollListGetSelected      = 0xA04
EvScrollListMakeVisible      = 0xA05
EvScrollListSetMultisel      = 0xA06
EvScrollListGetMultisel      = 0xA07
EvScrollListSetColour        = 0xA08
EvScrollListGetColour        = 0xA09
EvScrollListCountItems       = 0xA0A
EvScrollListGetItemText      = 0xA0B
EvScrollListSetItemText      = 0xA0C
EvScrollListSelectItem       = 0xA0D
EvScrollListDeselectItem     = 0xA0E
EvScrollListSetFont          = 0xA0F
EvScrollListPopulate         = 0xA10

# Slider test events
EvSliderSetValue             = 0xB00
EvSliderGetValue             = 0xB01
EvSliderSetLowerBound        = 0xB02
EvSliderGetLowerBound        = 0xB03
EvSliderSetUpperBound        = 0xB04
EvSliderGetUpperBound        = 0xB05
EvSliderSetStepSize          = 0xB06
EvSliderGetStepSize          = 0xB07
EvSliderSetColour            = 0xB08
EvSliderGetColour            = 0xB09

# RadioButton test events
EvRadioButtonSetLabel        = 0xC00
EvRadioButtonGetLabel        = 0xC01
EvRadioButtonSetEvent        = 0xC02
EvRadioButtonGetEvent        = 0xC03
EvRadioButtonSetState        = 0xC04
EvRadioButtonGetState        = 0xC05
EvRadioButtonSetFont         = 0xC06

# StringSet test events
EvStringSetSetAvailable      = 0xD00
EvStringSetSetSelectedText   = 0xD01
EvStringSetGetSelectedText   = 0xD02
EvStringSetSetSelectedIndex  = 0xD03
EvStringSetGetSelectedIndex  = 0xD04
EvStringSetSetAllowable      = 0xD05
EvStringSetGetAlphaNum       = 0xD06
EvStringSetGetPopUp          = 0xD07
EvStringSetSetFont           = 0xD08

# PopUp test events
EvPopUpSetMenu               = 0xE00
EvPopUpGetMenu               = 0xE01
