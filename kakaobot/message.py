class Message():
	"""
	Message class represents message object

	Parameters
	----------
	text : string, Optional
		the text the opponent will receive.
	photo : kakaobot.Photo, Optional
		the Photo the opponent will receive.
	message_button : kakaobot.Mbutton, Optional
		the Button the opponent will receive.
	keyboard : kakaobot.Kboard, Optional
		the information to compel the opponent's response
	"""
	def __init__(self, text = None, photo = None, message_button = None, keyboard = None):
		self.text = text
		self.photo = photo
		self.message_button = message_button
		self.keyboard = keyboard

	def set_text(self, text):
		self.text = text

	def set_photo(self, photo):
		self.photo = photo

	def set_button(self, message_button):
		self.message_button = message_button
	
	def set_keyboard(self, keyboard):
		self.keyboard = keyboard

	def make_dict(self):
		target = {
			"message":{
			}
		}
		if self.text: target["message"]["text"] = self.text
		if self.photo: target["message"]["photo"] = self.photo
		if self.message_button: target["message"]["message_button"] = self.message_button
		if self.keyboard : target["keyboard"] = self.keyboard
		return target