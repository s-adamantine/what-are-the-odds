import jsoncfg
from copy import deepcopy

class Empire:
	def __init__(self, empireJsonFile):
		self.json = jsoncfg.load(empireJsonFile)
		self.paths = Empire.grabEmpirePath(self.json)
		self.countdown = self.json['countdown']

	# Convert empireJsonFile into an easier to read data structure
	def grabEmpirePath(empireJson):
		empire_path = {}
		for path in empireJson['bounty_hunters']:
			if path['planet'] not in empire_path:
				empire_path[path['planet']] = [path['day']]
			else:
				empire_path[path['planet']].append(path['day'])
		return empire_path

class C3PO:

	# @paths: A list of lists. Each element of the outer list contains a possible
	#   	  journey that you can take from Tatooine.
	# @travel_times: A list of lists. Each element of the outer list contains a list
	#         of integers each detailing the time taken to travel from planet to planet
	#         of the respective path in self.paths.
	# @min_path_times: List. Each element in this list corresponds to a corresponding
	#         path in self.paths. Integer. The minimum time you would take to complete
	#         the total journey, including refuels.
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']
		self.paths = C3PO.generatePaths(self)
		self.min_path_times = C3PO.calculateMinimumTime(self)

	# Generate an array (or a python list) of linked lists, each representing a 
	# single valid travel path from Tatooine to Endor.
	def generatePaths(self):
		paths = [[0, 'Tatooine']]
		# iterate through each new destination and add it to an origin 
		for route in self.milleniumFalconJson['routes']:
			for path in paths:
				if route['origin'] in path:
					if path[-1] == route['origin']:
						path.append(route['travelTime'])
						path.append(route['destination'])
					else:
						indexOf = path.index(route['origin'])
						toAppend = path[:indexOf + 1]
						toAppend.append(route['travelTime'])
						toAppend.append(route['destination'])
						paths.append(toAppend)
						break
		return paths

	# Calculate the minimum amount of travel time taken for a route
	def calculateMinimumTime(self):
		min_path_times = []
		for path in self.paths:
			total = 0
			for route in path:
				if "Endor" not in path:
					break
				if route == "Endor":
					break
				if isinstance(route, int):
					total += route
				if total % self.autonomy == 0:
					total += 1
			min_path_times.append(total)
		return min_path_times

	def probabilityCaptured(k):
		sumProbability = 0
		for i in range(k):
			sumProbability += (9 ** i) / (10 ** (i + 1))
		return (sumProbability)

	# Find the maximum probability of reaching Endor in the path
	# (assuming no float time)
	def calculateProbability(self, path, empire):
		times = [d for d in path if type(d) == int]
		paths = [p for p in path if type(p) == str]
		current_day = 0
		k = 0
		for (planet, travel_time) in zip(paths, times):
			current_day += travel_time
			if current_day > empire.countdown:
				return 0
			if planet in empire.paths and current_day in empire.paths[planet]:
				k += 1
			if current_day != 0 and current_day % self.autonomy == 0: #force refuel
				current_day += 1
				if planet in empire.paths and current_day in empire.paths[planet]:
					k += 1
		return(1 - C3PO.probabilityCaptured(k))

	def giveMeTheOdds(self, empireJsonFile):
		empire = Empire(empireJsonFile)
		probabilities = []
		for path in self.paths:
			probabilities.append(C3PO.calculateProbability(self, path, empire))
		return max(probabilities)

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))