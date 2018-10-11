import jsoncfg

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']

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
		empireJson = jsoncfg.load(empireJsonFile)
		# parse the travelTime from start to finish
		if (C3PO.reachedInTime(self, empireJson)):
			pass
		return 0

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))
print(C3PO.probabilityCaptured(0))