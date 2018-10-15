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
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']

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
	def calculateMinimumTime(self, paths):
		path_times = []
		for path in paths:
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
			path_times.append(total)
		return path_times

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
		paths = C3PO.generatePaths(self)
		path_times = C3PO.calculateMinimumTime(self, paths)
		empire = Empire(empireJsonFile)
		probabilities = []
		for path in paths:
			probabilities.append(C3PO.calculateProbability(self, path, empire))
		return max(probabilities)

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))