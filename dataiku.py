import jsoncfg
from copy import deepcopy

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']

	# Generate an array (or a python list) of linked lists, each representing a 
	# single valid travel path from Tatooine to Endor.
	def generatePaths(self):
		paths = [['Tatooine']]
		# iterate through each new destination and add it to an origin 
		for route in self.milleniumFalconJson['routes']:
			print('the current route is ' + route['origin'] + ' to ' + route['destination'])
			for path in paths:
				if route['origin'] in path:
					if path[-1] == route['origin']:
						path.append(route['destination'])
					else:
						indexOf = path.index(route['origin'])
						toAppend = path[:indexOf + 1]
						toAppend.append(route['destination'])
						paths.append(toAppend)
						break
			print(paths)

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