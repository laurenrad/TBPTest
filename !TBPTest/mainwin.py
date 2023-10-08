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

from reporter import Reporter
from riscos_toolbox.objects.window import Window
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import UserMessage
import ctypes
import swi
from tbox_const import *

class HelpReplyMessage(UserMessage):
    event_id = 0x503
    _fields_ = UserMessage._fields_ + [ \
        ("help_message",ctypes.c_char*216)
    ]
    
class TestMessage(UserMessage):
    event_id = 0x667
    _fields_ = UserMessage._fields_ + [ \
        ("message_data",ctypes.c_uint32) ]

class MainWindow(Window):
    template = "MainWin"
    
    def __init__(self, *args):
        super().__init__(*args)
        Reporter.print("Creating mainwin")
        
        # Set up gadgets
        self.g_wimphandle = DisplayField(self, 0x01)
        self.g_wimphandle.value = repr(self.wimp_handle)
        
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