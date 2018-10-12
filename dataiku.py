import jsoncfg
from anytree import Node, RenderTree

class Node:
	def __init__(self, name, travel_time=0):
		self.name = name
		self.travel_time = travel_time
		self.next = None

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']

	# Generate an array (or a python list) of linked lists, each representing a 
	# single valid travel path from Tatooine to Endor.
	def generatePaths(self):
		nodes = []
		# a dictionary would make this easier to access  
		routes = {}
		nodes.append('Tatooine')
		nodes.append('Endor')
		# Create one route called Tatooine 
		routes['Tatooine'] = Node('Tatooine', 0)
		# iterate through each new destination and add it to an origin 
		for route in self.milleniumFalconJson['routes']:
			# check if a node with the name already exists
				if route['destination'] in nodes:
					if route['origin'] in nodes:
						#add the destination to the origin
							#can't access the specific node unfortunately
					else:
						nodes.append(Node(route['destination'], route['travelTime']))
					pass
				else:
					# if it doesn't exist, create one
					nodes.append(Node(route['destination'], route['travelTime']))

	# Check if the Millenium can reach Endor before the Death Star
	# annilihates it. 
	def reachedInTime(self, empireJson):
		total = 0
		countdown = empireJson['countdown']
		for routes in self.milleniumFalconJson['routes']:
			total += routes['travelTime']
			if total > countdown:
				return False
			if routes['destination'] == "Endor":
				return True
			if total % self.autonomy == 0:
				total += 1
		return False

	def probabilityCaptured(k):
		sumProbability = 0
		for i in range(k):
			sumProbability += (9 ** i) / (10 ** (i + 1))
		return (sumProbability)

	def giveMeTheOdds(self, empireJsonFile):
		C3PO.generatePaths(self)
		empireJson = jsoncfg.load(empireJsonFile)
		# parse the travelTime from start to finish
		if (C3PO.reachedInTime(self, empireJson)):
			return 1
		return 0

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))