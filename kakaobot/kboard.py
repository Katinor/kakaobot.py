class Kboard():
	"""
	Kboard class represents information with method of input.

	Parameters
	----------
	button : String or [String], Optional
		button's label. When this parameter is not empty, Bot compel the opponent using buttons instead of text. 
	"""
	def __init__(self, button = None):
		if button:
			if type(button) == type(["hello"]):
				self.button = []
				for i in button:
					self.button.append(i)
			else:
				self.button = [button]
		else:
			self.button = []
	
	def add_button(self, button):
		self.button.append(button)

	def make_dict(self):
		if self.button:
			target = {
				"type" : "buttons",
				"buttons" : self.button
			}
		else:
			target = { "type" : "text" }
		return target
