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

import traceback

from tbox_const import *
from tbox_common import TestMenu
from reporter import Reporter

import riscos_toolbox as toolbox
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.writablefield import WritableField, WritableFieldValueChangedEvent
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.events import toolbox_handler, wimp_handler, message_handler

# some constants
# Gadgets
G_WRITABLE_TEST  = 0x00
G_WRITABLE_INPUT = 0x01
G_DISPLAY_OUTPUT = 0x02

class WritableWindow(Window):
	template = "WritableWin"
	
	def __init__(self, *args):
		super().__init__(*args)
		
		try:
			self.g_writable = WritableField(self,G_WRITABLE_TEST)
			self.g_input = WritableField(self,G_WRITABLE_INPUT)
			self.g_output = DisplayField(self,G_DISPLAY_OUTPUT)
			
		except Exception as e:
			Reporter.print(repr(e))
			with open("<TBPTest$Dir>.Logs.traceback",'w') as fp:
				traceback.print_exc(file=fp)
		
	# Methods for testing WritableField
	def writablefield_set_text(self):
		self.g_writable.value = self.g_input.value
		
	def writablefield_get_text(self):
		self.g_output.value = self.g_writable.value
		
	def writablefield_set_allow(self):
		self.g_writable.allowable = self.g_input.value
		
	def writablefield_get_allow(self):
		self.g_output.value = self.g_writable.allowable
	
	# Event handlers for WritableField
	@toolbox_handler(WritableFieldValueChangedEvent)
	def WritableFieldValueChanged(self,event,id_block,poll_block):
		self.g_output.value = "Writable field change: "+repr(poll_block.string)
			
class WritableFieldMenu(Menu,TestMenu):
	template = "WritFldMenu"
	
	## WritableField event handlers
	@toolbox_handler(EvWritableFieldSetText)
	def WritableFieldSetText(self,event,id_block,poll_block):
		window = toolbox.get_object(id_block.ancestor.id)
		window.writablefield_set_text()
		self.menu_tick(id_block.self.component)
	
	@toolbox_handler(EvWritableFieldGetText)
	def WritableFieldGetText(self,event,id_block,poll_block):
		window = toolbox.get_object(id_block.ancestor.id)
		window.writablefield_get_text()
		self.menu_tick(id_block.self.component)
		
	@toolbox_handler(EvWritableFieldSetAllow)
	def WritableFieldSetAllow(self,event,id_block,poll_block):
		window = toolbox.get_object(id_block.ancestor.id)
		window.writablefield_set_allow()
		self.menu_tick(id_block.self.component)
		
	@toolbox_handler(EvWritableFieldGetAllow)
	def WritableFieldGetAllow(self,event,id_block,poll_block):
		window = toolbox.get_object(id_block.ancestor.id)
		window.writablefield_get_allow()
		self.menu_tick(id_block.self.component)
