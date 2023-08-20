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
import riscos_toolbox as toolbox
from riscos_toolbox.events import toolbox_handler
from riscos_toolbox.objects.menu import Menu
from riscos_toolbox.objects.window import Window
from riscos_toolbox.gadgets.displayfield import DisplayField
from riscos_toolbox.gadgets.writablefield import WritableField
from tbox_const import *
from tbox_common import TestMenu
try:
	from riscos_toolbox.gadgets.stringset import StringSet
	from riscos_toolbox.gadgets.stringset import StringSetValueChangedEvent
	from riscos_toolbox.gadgets.stringset import StringSetAboutToBeShownEvent
except ModuleNotFoundError as e:
	Reporter.print("No StringSet in riscos_toolbox")
else:
	#Gadget Constants
	G_STRINGSET = 0x01
	G_INPUT     = 0x02
	G_INPUT_W   = 0x04
	G_INPUT_H   = 0x06
	G_OUTPUT    = 0x08
	
	class StringSetWindow(Window):
		template = "StrSetWin"
	
		def __init__(self, *args):
			super().__init__(*args)
		
			# Set up gadgets
			self.g_stringset = StringSet(self,G_STRINGSET)
			self.g_input = WritableField(self,G_INPUT)
			self.g_input_w = WritableField(self,G_INPUT_W)
			self.g_input_h = WritableField(self,G_INPUT_H)
			self.g_output = DisplayField(self,G_OUTPUT)
		
		# Methods for testing StringSet ops
		def stringset_set_available(self):
			self.g_stringset.set_available(self.g_input.value)
			
		def stringset_set_selected_text(self):
			self.g_stringset.selected = self.g_input.value
			
		def stringset_get_selected_text(self):
			self.g_output.value = self.g_stringset.selected
			
		def stringset_set_selected_index(self):
			try:
				self.g_stringset.index = int(self.g_input.value)
			except ValueError as e:
				self.g_output.value = "Err: expected int input"
				
		def stringset_get_selected_index(self):
			self.g_output.value = repr(self.g_stringset.index)
			
		def stringset_set_allowable(self):
			self.g_stringset.set_allowable(self.g_input.value)
			
		def stringset_get_alphanum(self):
			self.g_output.value = repr(self.g_stringset.alphanumeric_field)
			
		def stringset_get_popup(self):
			self.g_output.value = repr(self.g_stringset.popup_menu)
			
		def stringset_set_font(self):
			try:
				name = self.g_input.value
				width = int(self.g_input_w.value)
				height = int(self.g_input_h.value)
			except ValueError as e:
				self.g_output.value = "Err: expected int input"
			else:
				self.g_stringset.set_font(name,width,height)
	
		# Event handlers for StringSet
		@toolbox_handler(StringSetValueChangedEvent)
		def _stringset_value_changed(self,event,id_block,poll_block):
			self.g_output.value = "Value changed"
			
		@toolbox_handler(StringSetAboutToBeShownEvent)
		def _stringset_about_to_be_shown(self,event,id_block,poll_block):
			self.g_output.value = "About to be shown"
		
	class StringSetMenu(Menu,TestMenu):
		template = "StrSetMenu"
		
		# Event handlers
		@toolbox_handler(EvStringSetSetAvailable)
		def _stringset_set_available(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_set_available()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetSetSelectedText)
		def _stringset_set_selected_text(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_set_selected_text()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetGetSelectedText)
		def _stringset_get_selected_text(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_get_selected_text()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetSetSelectedIndex)
		def _stringset_set_selected_index(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_set_selected_index()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetGetSelectedIndex)
		def _stringset_get_selected_index(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_get_selected_index()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetSetAllowable)
		def _stringset_set_allowable(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_set_allowable()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetGetAlphaNum)
		def _stringset_get_alphanum(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_get_alphanum()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetGetPopUp)
		def _stringset_get_popup(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_get_popup()
			self.menu_tick(id_block.self.component)
			
		@toolbox_handler(EvStringSetSetFont)
		def _stringset_set_font(self,event,id_block,poll_block):
			window = toolbox.get_object(id_block.ancestor.id)
			window.stringset_set_font()
			self.menu_tick(id_block.self.component)
