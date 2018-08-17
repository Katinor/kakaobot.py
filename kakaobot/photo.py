class Photo():
	"""
	Photo class represents photo object

	Parameters
	----------
	url : String with url, Required
		Photo's url.
	width : Int, Optional (default : 720)
		Photo's width.
	height : Int, Optional (default : 630)
		Photo's height.
	"""
	def __init__(self, url, width = 720, height = 630):
		self.url = url
		self.width = width
		self.height = height
	def make_dict(self):
		target = {
			"url" : self.url,
			"width" : self.width,
			"height" : self.height
		}
		return target
