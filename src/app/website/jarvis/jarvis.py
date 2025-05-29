import ollama

system_message = """
You are a helpful AI assistant.
"""

class Jarvis():
	def __init__(self, model: str):
		self.model = model
		self.conversation: list[dict[str, str]] = []
		self.stream = True

		self.conversation.append({
			'role': 'system',
			'content': system_message
			})


	def chat(self, query):
		self.conversation.append({
			'role': 'user',
			'content': query
			})

		self.response = ollama.chat(
			model=self.model,
			messages=self.conversation,
			stream=self.stream
			)

		for chunk in self.response:
			yield chunk


	def stream_response(self, query):
		complete_response = ''
		for chunk in self.chat(query):
			complete_response += chunk['message']['content']
			yield chunk['message']['content']

		self.conversation.append({
			'role': 'assistant',
			'content': complete_response
			})
