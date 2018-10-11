import jsoncfg

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)
		self.autonomy = self.milleniumFalconJson['autonomy']

	def reachedInTime(self, empireJson):
		total = 0
		countdown = empireJson['countdown']
		for routes in self.milleniumFalconJson['routes']:
			# add the travel times until it reaches the first instance of Endor
			total += routes['travelTime']
			if total % self.autonomy == 0:
				total += 1
			if (routes['destination'] == "Endor" and total > countdown):
				return False
		return True

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