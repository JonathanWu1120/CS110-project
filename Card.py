
class Card:
	#to make a card you must type Card("Name of Card")
	def __init__(self,string):
		self.type = string
	def __str__(self):
		return self.type