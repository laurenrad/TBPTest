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
from riscos_toolbox.objects.window import WindowAboutToBeShownEvent, WindowHasBeenHidden
from riscos_toolbox.gadgets.radiobutton import RadioButton, RadioButtonStateChangedEvent
from riscos_toolbox.gadgets.radiobutton import RadioButtonDefinition
from riscos_toolbox.gadgets.actionbutton import ActionButton, ActionButtonSelectedEvent
from riscos_toolbox.gadgets.numberrange import NumberRange
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from riscos_toolbox.gadgets.textarea import TextArea
from riscos_toolbox.events import toolbox_handler

class WinWindow(Window):
    template = "WinWin"
    
    # Gadget constants
    G_RADIO_WIMP_HANDLE = 0x11
    G_RADIO_MENU        = 0x12
    G_RADIO_POINTER     = 0x13
    G_RADIO_HELPMSG     = 0x14
    G_RADIO_TITLE       = 0x15
    G_RADIO_FOCUS       = 0x16
    G_RADIO_EXTENT      = 0x17
    G_RADIO_TOOLBARS    = 0x1F
    G_SHOW              = 0x00
    G_GET               = 0x0C
    G_SET               = 0x0D
    G_ADD_GADGET        = 0x31
    G_REMOVE_GADGET     = 0x32
    G_INPUT_INT1        = 0x0B
    G_INPUT_INT2        = 0x18
    G_INPUT_INT3        = 0x1A
    G_INPUT_INT4        = 0x1C
    G_INPUT_STR         = 0x0A
    G_RESULT            = 0x09
    G_TEXTAREA          = 0x08
    G_MENU1_ID          = 0x2B
    G_MENU2_ID          = 0x2C
    G_HTBAR_ID          = 0x2F
    G_VTBAR_ID          = 0x30
    
    def __init__(self, *args):
        super().__init__(*args)
        self.win = toolbox.create_object("Win")
        self.result = DisplayField(self,WinWindow.G_RESULT)
        self.textarea = TextArea(self,WinWindow.G_TEXTAREA)
        self.input_int1 = NumberRange(self,WinWindow.G_INPUT_INT1)
        self.input_int2 = NumberRange(self,WinWindow.G_INPUT_INT2)
        self.input_int3 = NumberRange(self,WinWindow.G_INPUT_INT3)
        self.input_int4 = NumberRange(self,WinWindow.G_INPUT_INT4)
        self.input_str = WritableField(self,WinWindow.G_INPUT_STR)
        self.menu1_id = DisplayField(self,WinWindow.G_MENU1_ID)
        self.menu2_id = DisplayField(self,WinWindow.G_MENU2_ID)
        self.htbar_id = DisplayField(self,WinWindow.G_HTBAR_ID)
        self.vtbar_id = DisplayField(self,WinWindow.G_VTBAR_ID)
        
        self.selected_test = WinWindow.G_RADIO_WIMP_HANDLE
        
        # Set up some test objects to use in testing object linkage
        self.tbar_h = toolbox.create_object("ToolbarH")
        self.tbar_v = toolbox.create_object("ToolbarV")
        self.menu1 = toolbox.create_object("TestMenu1")
        self.menu2 = toolbox.create_object("TestMenu2")
        self.menu1_id.value = repr(self.menu1.id)+" ("+hex(self.menu1.id)+")"
        self.menu2_id.value = repr(self.menu2.id)+" ("+hex(self.menu2.id)+")"
        self.htbar_id.value = repr(self.tbar_h.id)+" ("+hex(self.tbar_h.id)+")"
        self.vtbar_id.value = repr(self.tbar_v.id)+" ("+hex(self.tbar_v.id)+")"
        
    @toolbox_handler(RadioButtonStateChangedEvent)
    def test_selected(self,event,id_block,poll_block):
        if id_block.self.id != self.id:
            return False
            
        self.selected_test = id_block.self.component
        
        return True
        
    @toolbox_handler(ActionButtonSelectedEvent)
    def actionbutton_selected(self,event,id_block,poll_block):
        Reporter.print("actionbuttonselected event")
        if id_block.self.id != self.id:
            return False
            
        Reporter.print("handling")
            
        if id_block.self.component == WinWindow.G_SHOW:
            Reporter.print("showing test window")
            self.win.show()
        elif id_block.self.component == WinWindow.G_GET:
            if self.selected_test == WinWindow.G_RADIO_WIMP_HANDLE:
                Reporter.print("test: window: get wimp handle")
                self.result.value = hex(self.win.wimp_handle)
            elif self.selected_test == WinWindow.G_RADIO_MENU:
                Reporter.print("test: window: get menu")
                self.result.value = repr(self.win.menu_id)+" ("+hex(self.win.menu_id)+")"
            elif self.selected_test == WinWindow.G_RADIO_POINTER:
                Reporter.print("test: window: get pointer")
                name, hot_spot = self.win.get_pointer()
                self.result.value = f"x={hot_spot.x} y={hot_spot.y} name={name}"
            elif self.selected_test == WinWindow.G_RADIO_HELPMSG:
                Reporter.print("test: window: get help msg")
                self.result.value = self.win.help_message
            elif self.selected_test == WinWindow.G_RADIO_TITLE:
                Reporter.print("test: window: get title")
                self.result.value = self.win.title
            elif self.selected_test == WinWindow.G_RADIO_FOCUS:
                Reporter.print("test: window: get default focus")
                self.result.value = repr(self.win.default_focus)
            elif self.selected_test == WinWindow.G_RADIO_EXTENT:
                Reporter.print("test: window: get extent")
                extent = self.win.extent
                self.result.value = f"min_x={extent.min.x} min_y={extent.min.y} "\
                                     f"max_x={extent.max.x} max_y={extent.max.y}"
            elif self.selected_test == WinWindow.G_RADIO_TOOLBARS:
                Reporter.print("test: window: get toolbars")
                ibl = self.win.get_toolbar_id(Window.InternalBottomLeftToolbar)
                itl = self.win.get_toolbar_id(Window.InternalTopLeftToolbar)
                ebl = self.win.get_toolbar_id(Window.ExternalBottomLeftToolbar)
                etl = self.win.get_toolbar_id(Window.ExternalTopLeftToolbar)
                self.result.value = f"ibl={ibl} itl={itl} ebl={ebl} etl={etl}"                   
            else:
                Reporter.print("test: window: unknown get test")
        elif id_block.self.component == WinWindow.G_SET:
            if self.selected_test == WinWindow.G_RADIO_MENU:
                Reporter.print("test: window: set menu")
                # NumberRange seems to have trouble with the extreme int values, which
                # would be needed to handle ObjectIDs properly. This will convert str field
                # to int instead.
                try:
                    self.win.menu_id = int(self.input_str.value)
                except ValueError as e:
                    self.result.value = "Must enter ObjectID as int in str input."
            elif self.selected_test == WinWindow.G_RADIO_POINTER:
                Reporter.print("test: window: set pointer")
                hot_spot = toolbox.Point(self.input_int1.value, self.input_int2.value)
                self.win.set_pointer(self.input_str.value,hot_spot)
            elif self.selected_test == WinWindow.G_RADIO_HELPMSG:
                Reporter.print("test: window: set help msg")
                self.win.help_message = self.input_str.value
            elif self.selected_test == WinWindow.G_RADIO_TITLE:
                Reporter.print("test: window: set title")
                self.win.title = self.input_str.value
            elif self.selected_test == WinWindow.G_RADIO_FOCUS:
                Reporter.print("test: window: set focus")
                self.win.default_focus = self.input_int1.value
            elif self.selected_test == WinWindow.G_RADIO_EXTENT:
                Reporter.print("test: window: set extent")
                extent = toolbox.BBox(self.input_int1.value, self.input_int2.value,
                                      self.input_int3.value, self.input_int4.value)
                self.win.extent = extent
            elif self.selected_test == WinWindow.G_RADIO_TOOLBARS:
                Reporter.print("test: window: set toolbars")
                # This is a little clunky but will do it this way to avoid redoing interface for now
                
                try:
                    if self.input_int1.value == 0: # ibl
                        self.win.set_toolbar_id(Window.InternalBottomLeftToolbar,
                                                int(self.input_str.value))
                    elif self.input_int1.value == 1: # itl
                        self.win.set_toolbar_id(Window.InternalTopLeftToolbar,
                                                int(self.input_str.value))
                    elif self.input_int1.value == 2: # ebl
                        self.win.set_toolbar_id(Window.ExternalBottomLeftToolbar,
                                                int(self.input_str.value))
                    elif self.input_int1.value == 3: # etl
                        self.win.set_toolbar_id(Window.ExternalTopLeftToolbar,
                                                int(self.input_str.value))
                    else:
                        self.result.value = "int1: 0=ibl, 1=itl, 2=ebl, 3=etl" 
                except ValueError as e:
                    self.result.value = "Must enter ObjectID as int in str input"                   
            else:
                Reporter.print("test: window: unknown set test")
        elif id_block.self.component == WinWindow.G_ADD_GADGET:
            Reporter.print("test: window: add gadget")
            # I'm not really clear on how this is supposed to work, so this test
            # is not completed yet.
            #flags = 0
            #type = 384 # RadioButton
            #box = toolbox.BBox(0,0,50,100)
            #id = 0xF0
            #r = RadioButtonDefinition(flags,type,box,id,"helpmsg")
            #r.grouop_number = 0
            #r.label = b"hi"
            #r.max_label_len = 30
            #r.event = 0
            #self.win.add_gadget(r)
            self.result.value = "Add Gadget test not yet implemented."
        elif id_block.self.component == WinWindow.G_REMOVE_GADGET:
            Reporter.print("test: window: remove gadget")
            component = self.input_int1.value
            self.win.remove_gadget(component)
        else:
            return False
            
        return True
        
    @toolbox_handler(WindowAboutToBeShownEvent)
    def window_shown(self,event,id_block,poll_block):
        if id_block.self.id != self.win.id:
            return False

        Reporter.print("window shown")
        self.textarea.insert(-1,"WindowAboutToBeShownEvent | ")   
             
        return True
        
    @toolbox_handler(WindowHasBeenHidden)
    def window_hidden(self,event,id_block,poll_block):
        if id_block.self.id != self.win.id:
            return False
            
        Reporter.print("window hidden")
        self.textarea.insert(-1,"WindowHasBeenHidden | ")
        
        return True
