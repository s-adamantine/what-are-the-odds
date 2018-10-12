# Not sure whether to store it as a dictionary, as an array, or as a whatever, but for now
# i'm just going to use an array and see if it works. 

class LinkedList:
	def __init__(self, name, travel_time):
		self.name = name
		self.travel_time = travel_time
		self.next = None

