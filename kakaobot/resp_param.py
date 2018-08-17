class Resp_param():
	def __init__(self, request):
		msg_content = request.get_json()
		self.user_key = msg_content["user_key"]
		self.type = msg_content["type"]
		self.content = msg_content["content"]