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
__version__ = '1.0b'

import random,json,re,os,logging
from functools import wraps
from flask import Flask, jsonify, request
from .resp_param import Resp_param
from .kboard import Kboard
from .mbutton import Mbutton
from .photo import Photo
from .message import Message
from .log_append import log_append 

logging.basicConfig(level = logging.ERROR)
if not os.path.exists('kakaobot_log'):
	os.makedirs(os.path.join('kakaobot_log'))

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
		log_append("Kakaobot","Construct Client class","SYS","init")
		self.kboard = kboard
		self._command = {}
		self._prefix_command = {}
		self._regex_command = {}
		self._extra = None
		self._friend_add = None
		self._friend_delete = None
		self._room_out = None
		self.app = Flask(__name__)
		self._port = port
		self.error_text = error_text
		log_append("Kakaobot","Success to construct","SYS","init")

	def add_command(self,command_list = []):
		def _al_command(func):
			log_append("Kakaobot","add regular command : "+func.__name__+" in "+str(func),"SYS","event")
			temp_text = ""
			if command_list == []:
				self._command[func.__name__] = func
				temp_text += func.__name__
			else:
				for i in command_list:
					self._command[i] = func
					temp_text += i + ", " 
			log_append("Kakaobot","alias list of "+func.__name__+" : "+temp_text,"SYS","event")
			@wraps(func)
			def wrapper_function(user_id):
				return func(user_id)
			return wrapper_function
		return _al_command
	
	def add_prefix_command(self,command_list = [], preserve_prefix = False):
		def _al_prcom(func):
			if preserve_prefix:
				log_append("Kakaobot","add prefix command : "+func.__name__+" in "+str(func)+" with preserve_prefix","SYS","event")
				temp_text = ""
				if command_list == []:
					self._prefix_command[func.__name__] = (func , True)
					temp_text += func.__name__
				else:
					for i in command_list:
						self._prefix_command[i] = (func , True)
						temp_text += i + ", "
			else:
				log_append("Kakaobot","add prefix command : "+func.__name__+" in "+str(func),"SYS","event")
				temp_text = ""
				if command_list == []:
					self._prefix_command[func.__name__] = (func , False)
					temp_text += func.__name__
				else:
					for i in command_list:
						self._prefix_command[i] = (func , False)
						temp_text += i + ", "
			log_append("Kakaobot","alias list of "+func.__name__+" : "+temp_text,"SYS","event")
			@wraps(func)
			def wrapper_function(user_id, content):
				return func(user_id, content)
			return wrapper_function
		return _al_prcom

	def add_regex_command(self,regex_string):	
		def _reg_command(func):
			log_append("Kakaobot","add regex command : "+func.__name__+" in "+str(func),"SYS","event")
			self._regex_command[regex_string] = func
			log_append("Kakaobot","target regex : "+regex_string,"SYS","event")
			@wraps(func)
			def wrapper_function(user_id, group):
				return func(user_id, group)
			return wrapper_function
		return _reg_command
	
	def set_extra(self,func):
		log_append("Kakaobot","set extra command : "+func.__name__+" in "+str(func),"SYS","event")
		self._extra = func
		@wraps(func)
		def wrapper_function(user_id, content):
			return func(user_id, content)
		return wrapper_function

	def set_friend_add_event(self,func):
		log_append("Kakaobot","set friend add event : "+func.__name__+" in "+str(func),"SYS","event")
		self._friend_add = func
		@wraps(func)
		def wrapper_function(user_id):
			return func(user_id)
		return wrapper_function

	def set_friend_delete_event(self,func):
		log_append("Kakaobot","set friend delete event : "+func.__name__+" in "+str(func),"SYS","event")
		self._friend_delete = func
		@wraps(func)
		def wrapper_function(user_id):
			return func(user_id)
		return wrapper_function

	def set_chatroom_leave_event(self,func):
		log_append("Kakaobot","set chatroom leave event : "+func.__name__+" in "+str(func),"SYS","event")
		self._room_out = func
		@wraps(func)
		def wrapper_function(user_id):
			return func(user_id)
		return wrapper_function

	def run(self):
		log_append("Kakaobot","Ready to run","SYS","run")
		log_append("Kakaobot","Set initial keyboard","SYS","run")
		@self.app.route("/keyboard")
		def _main_set_keyboard():
			return jsonify(self.kboard.make_dict())

		log_append("Kakaobot","Set friend event","SYS","run")
		@self.app.route("/friend", methods = ['POST'])
		def _friend_add_stream():
			if self._friend_add:
				msg_content = request.get_json()
				self._friend_add(msg_content["user_key"])
			return ""

		@self.app.route("/friend/<temp_user_key>", methods = ['DELETE'])
		def _friend_delete_stream(temp_user_key):
			if self._friend_delete:
				self._friend_delete(temp_user_key)
			return ""

		@self.app.route("/chat_room/<temp_user_key>", methods = ['DELETE'])
		def _chatroom_leave_stream(temp_user_key):
			if self._room_out:
				self._room_out(temp_user_key)
			return ""

		log_append("Kakaobot","Set command event","SYS","run")
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
								if self._prefix_command[temp_prefix][1] :
									target = self._prefix_command[temp_prefix][0](get_data.user_key,get_data.content)
								else :
									target = self._prefix_command[temp_prefix][0](get_data.user_key,get_data.content[len(temp_prefix)+1:])
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
		log_append("Kakaobot","Chatbot started","SYS","run")