"""
Kakaotalk API Wrapper
~~~~~~~~~~~~~~~~~~~
A basic wrapper for the Kakaotalk API.
:copyright: (c) 2018 Katinor
:license: MIT, see LICENSE for more details.
"""

__title__ = 'kakaobot.py'
__author__ = 'Katinor'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018 Katinor'
__version__ = '0.1'

import random,json,re
from functools import wraps
from flask import Flask, jsonify, render_template, request, abort, redirect, url_for
import logging

from .resp_param import Resp_param
from .kboard import Kboard
from .mbutton import Mbutton
from .photo import Photo
from .message import Message

logging.basicConfig(level = logging.ERROR)

class Client:
	"""
	Client class represents a client that can be hooked by kakaotalk plus-friends API V.2.0.
	This class is used to open a socket to interact wih Kakaotalk webSocket.

	Parameters
	----------
	port : Int, Optional (default : 5000)
		the port number of Flask socket. You have to remember this variable to make a reverse proxy to connect with HTTP.
	kboard : kakaobot.Kboard, Optional (default : empty Kboard)
		the initial kboard when someone use this bot. when it is default, bot can take text instead of buttons.
	error_text : kakaobot.Message, Optional (default : "Error occured")
		the string that will be talked by bot when someone say that is not applyed.
	"""
	def __init__(self, port=5000, kboard = Kboard(), error_text = Message(text = "Error occured")):
		self.kboard = kboard
		self._command = {}
		self._prefix_command = {}
		self._regex_command = {}
		self._extra = None
		self.app = Flask(__name__)
		self._port = port
		self.error_text = error_text

	def add_command(self,func):
		self._command[func.__name__] = func
		@wraps(func)
		def wrapper_function(user_id):
			return func(user_id)
		return wrapper_function
	
	def add_alias_command(self,command_list):
		def _al_command(func):
			for i in command_list:
				self._command[i] = func
			@wraps(func)
			def wrapper_function(user_id):
				return func(user_id)
			return wrapper_function
		return _al_command
	
	def add_prefix_command(self,func):
		self._prefix_command[func.__name__] = func
		@wraps(func)
		def wrapper_function(user_id, content):
			return func(user_id, content)
		return wrapper_function

	def add_regex_command(self,regex_string):	
		def _reg_command(func):
			self._regex_command[regex_string] = func
			@wraps(func)
			def wrapper_function(user_id, group):
				return func(user_id, group)
			return wrapper_function
		return _reg_command
	
	def set_extra(self,func):
		self._extra = func
		@wraps(func)
		def wrapper_function(user_id, content):
			return func(user_id, content)
		return wrapper_function

	def run(self):
		@self.app.route("/keyboard")
		def _main_set_keyboard():
			return jsonify(self.kboard.make_dict())

		@self.app.route("/message", methods = ['POST'])
		def _main_set_message():
			get_data = Resp_param(request)
			target = None
			while(True):
				if get_data.type == "text":
					if get_data.content in self._command.keys():
						target = self._command[get_data.content](get_data.user_key)
						break
					else:
						if self._prefix_command:
							temp_prefix = get_data.content.split(" ")[0]
							if temp_prefix in self._prefix_command.keys():
								target = self._prefix_command[temp_prefix](get_data.user_key,get_data.content[len(temp_prefix)+1:])
								break
						if self._regex_command:
							swt = False
							for i in self._regex_command.keys():
								temp_regex = re.search(i, get_data.content)
								if temp_regex:
									swt = True
									target = self._regex_command[i](get_data.user_key,temp_regex.groups())
									break
							if swt: break
						if self._extra:
							target = self._extra(get_data.user_key,get_data.content)
							break
						target = self.error_text
						break
				else:
					target = self.error_text
					break
			return jsonify(target.make_dict())

		self.app.run(host='0.0.0.0',port=self._port,debug=False)
