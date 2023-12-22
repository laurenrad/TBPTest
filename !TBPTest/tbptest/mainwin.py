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

import ctypes
import swi

from tbptest.reporter import Reporter
from tbptest.tbox_const import *

import riscos_toolbox as toolbox
from riscos_toolbox.objects.window import Window
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import UserMessage

class HelpReplyMessage(UserMessage):
    event_id = 0x503
    _fields_ = UserMessage._fields_ + [ \
        ("help_message",ctypes.c_char*216)
    ]
    
class TestMessage(UserMessage):
    event_id = 0x667
    _fields_ = UserMessage._fields_ + [ \
        ("message_data",ctypes.c_uint32) ]

# The main purpose of this window currently is to create some test objects to hook up to other
# things during testing and show their IDs.
class MainWindow(Window):
    template = "MainWin"
    
    # Gadget constants
    G_DISPLAY_OBJ1       = 0x06
    G_DISPLAY_OBJ2       = 0x08
    G_DISPLAY_MENU1      = 0x0A
    G_DISPLAY_MENU2      = 0x0C
    G_DISPLAY_TASKNAME   = 0x12
    G_DISPLAY_TASKHANDLE = 0x14
    
    def __init__(self, *args):
        super().__init__(*args)
        
        # Set up gadgets
        self.g_disp_obj1 = DisplayField(self, MainWindow.G_DISPLAY_OBJ1)
        self.g_disp_obj2 = DisplayField(self, MainWindow.G_DISPLAY_OBJ2)
        self.g_disp_menu1 = DisplayField(self, MainWindow.G_DISPLAY_MENU1)
        self.g_disp_menu2 = DisplayField(self, MainWindow.G_DISPLAY_MENU2)
        self.g_disp_taskname = DisplayField(self, MainWindow.G_DISPLAY_TASKNAME)
        self.g_disp_handle = DisplayField(self, MainWindow.G_DISPLAY_TASKHANDLE)
        
        # Create test items
        self.tst_obj1 = toolbox.create_object("TestWin1")
        self.tst_obj2 = toolbox.create_object("TestWin2")
        self.tst_menu1 = toolbox.create_object("TestMenu1")
        self.tst_menu2 = toolbox.create_object("TestMenu2")
        
        self.g_disp_obj1.value = repr(self.tst_obj1.id)+" ("+hex(self.tst_obj1.id)+")"
        self.g_disp_obj2.value = repr(self.tst_obj2.id)+" ("+hex(self.tst_obj2.id)+")"
        self.g_disp_menu1.value = repr(self.tst_menu1.id)+" ("+hex(self.tst_menu1.id)+")"
        self.g_disp_menu2.value = repr(self.tst_menu2.id)+" ("+hex(self.tst_menu2.id)+")"
        
        # Fill in any other info
        self.g_disp_taskname.value = toolbox.task_name()
        task_handle = swi.swi("Toolbox_GetSysInfo","I;...i",3)
        self.g_disp_handle.value = repr(task_handle)
        
    # Currently unused but here for future rework
    @toolbox_handler(EvMainTestButton)
    def actionbutton_clicked(self, event, id_block, poll_block):
        Reporter.print("Main test button clicked")
        
        #h = HelpReplyMessage()
        #h.your_ref = 0
        #h.code = HelpReplyMessage.event_id
        #h.size = 256
        #h.help_message = b"This is an example help message.\x00"
        h = TestMessage()
        h.your_ref = 0
        h.code = TestMessage.event_id
        h.msg_data = 420
        h.size = ctypes.sizeof(h)
        dst = ctypes.cast(ctypes.pointer(h),ctypes.POINTER(ctypes.c_byte))
        #msgptr = ctypes.c_char_p(h.help_message)
        #addr = ctypes.cast(msgptr,ctypes.c_void_p).value
        #message = b"This is an example help message."
        #h.help_message = ctypes.create_string_buffer(message,size=236)
        Reporter.print(f"ctypes.addressof(h): {ctypes.addressof(h)}")
        Reporter.print(f"ctypes.addressof(dst): {ctypes.addressof(dst)}")
        Reporter.print(f"ctypes.sizeof(h): {ctypes.sizeof(h)}")
        swi.swi('Wimp_SendMessage',"iii",17,ctypes.addressof(dst),0)      
        #swi.swi('Wimp_SendMessage','iii',17,ctypes.byref(h),0)