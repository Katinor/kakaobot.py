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

import random,json
from functools import wraps
from flask import Flask, jsonify, render_template, request, abort, redirect, url_for

class Client:
	def __init__(self, port=5000):
		self.keyboard = []
		self.command = {}
		self.extra = None
		self.app = Flask(__name__)

	def add_keyboard(self, value):
		self.keyboard.append(value)
	
	def set_keyboard(self,value):
		self.keyboard = value

	def add_command(self,func):
		if callable(func):
			self.command[func.__name__] = func