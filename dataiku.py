import jsoncfg
import copy
from empire_class import Empire

class C3PO:

	# @paths: A list of lists. Each element of the outer list contains a possible
	#   	  journey that you can take from Tatooine.
	# @travel_times: A list of lists. Each element of the outer list contains a list
	#         of integers each detailing the time taken to travel from planet to planet
	#         of the respective path in self.paths.
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']
		self.paths = C3PO.generatePaths(self)

	# Copies a single path from the origin until (and including) a planet.
	def copyPath(path, planet):
		indexOf = path.index(planet)
		return copy.copy(path[:(indexOf + 1)])

	# Generate an array (or a python list) of lists, with each element representing a
	# single valid travel path (and their travel times) from Tatooine to Endor.
	def generatePaths(self):
		paths = [[0, 'Tatooine']]
		for route in self.milleniumFalconJson['routes']:
			for path in paths:
				if route['origin'] in path:
					if path[-1] == route['origin']:
						path.extend([route['travelTime'], route['destination']])
					else:
						duplicate_path = C3PO.copyPath(path, route['origin'])
						duplicate_path.extend([route['travelTime'], route['destination']])
						paths.append(duplicate_path)
						break
		# All routes lead to Endor
		for path in paths:
			while path[-1] != 'Endor':
				for route in self.milleniumFalconJson['routes']:
					if path[-1] == route['origin']:
						path.extend([route['travelTime'], route['destination']])
		return paths

	# Generate all the extra float paths, given the current possible paths and the empire's
	# countdown.
	# Float paths are paths that contain 'Wait' at a planet in its routes.
	def generateFloatPaths(self, empire):
		wait = [1, 'Wait']
		float_paths = []
		for path in self.paths:
			float_days = empire.countdown - C3PO.calculateMinimumTime(self.autonomy, path)
			if float_days <= 0:
				continue
			else:
				# only need to use a float day if you're trying to avoid the enemy.
				for danger_planet in empire.paths:
					if danger_planet in path:
					# generate permutations of possible float paths (first with a wait time of 1)
						for i in range(2, path.index(danger_planet), 2):
							new_float_path = copy.copy(path)
							new_float_path[i:i] = wait
							float_paths.append(new_float_path)
		# Add wait times by one if we still have float days.
		for float_path in float_paths:
			float_days = empire.countdown - C3PO.calculateMinimumTime(self.autonomy, float_path)
			if float_days > 0:
				new_float_path = copy.copy(float_path)
				new_float_path[new_float_path.index('Wait') - 1] += 1
				float_paths.append(new_float_path)
		return float_paths

	# Calculate the minimum amount of travel time taken for a path
	def calculateMinimumTime(autonomy, path):
		total = 0
		for route in path:
			if "Endor" not in path:
				break
			if route == "Endor":
				break
			if isinstance(route, int):
				total += route
			if total % autonomy == 0:
				total += 1
		return total

	def probabilityCaptured(k):
		sumProbability = 0
		for i in range(k):
			sumProbability += (9 ** i) / (10 ** (i + 1))
		return (sumProbability)

	# Find the maximum probability of reaching Endor in a given path
	# Need to test force refuel.
	def calculateProbability(self, path, empire):
		times = [d for d in path if type(d) == int]
		paths = [p for p in path if type(p) == str]
		current_day = 0
		k = 0
		autonomy = self.autonomy
		for (planet, travel_time, i) in zip(paths, times, range(len(times))):
			current_day += travel_time
			autonomy -= travel_time
			if current_day > empire.countdown:
				return 0
			if planet in empire.paths and current_day in empire.paths[planet]:
				k += 1
			# Refuel if wait
			if planet == 'Wait':
				autonomy = self.autonomy
			# Force refuel at current planet if the autonomy is 0 
			if autonomy == 0:
				current_day += 1
				autonomy = self.autonomy
				if planet in empire.paths and current_day in empire.paths[planet]:
					k += 1
			# Force refuel if you can't get to the next planet with a full tank
			if paths[-1] != planet:
				if autonomy - times[i + 1] < 0:
					current_day += 1
					autonomy = self.autonomy
		return(1 - C3PO.probabilityCaptured(k))

	def giveMeTheOdds(self, empireJsonFile):
		empire = Empire(empireJsonFile)
		float_paths = C3PO.generateFloatPaths(self, empire)
		if float_paths:
			self.paths.extend(float_paths)
		probabilities = []
		for path in self.paths:
			probabilities.append(C3PO.calculateProbability(self, path, empire))
		return max(probabilities)

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))