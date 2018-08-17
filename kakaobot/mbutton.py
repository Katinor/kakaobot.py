class Mbutton():
	"""
	Mbutton class represents message_button object

	Parameters
	----------
	label : String, Required
		Button's Label
	url : String with url, Required
		the URL to pop-up when the opponent click this button.
	"""
	def __init__(self, label, url):
		self.label = label
		self.url = url
	def make_dict(self):
		target = {
			"label" : self.label,
			"url" : self.url
		}
		return target