import jsoncfg

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJson = jsoncfg.load(milleniumFalconJsonFile)

	def reachedInTime(milleniumFalconJson, empireJson):
		total = 0
		autonomy = milleniumFalconJson['autonomy']
		countdown = empireJson['countdown']
		for routes in milleniumFalconJson['routes']:
			# add the travel times until it reaches the first instance of Endor
			total += routes['travelTime']
			if total % autonomy == 0:
				total += 1
			if (routes['destination'] == "Endor" and total > countdown):
				return False
		return True

	def giveMeTheOdds(self, empireJsonFile):
		empireJson = jsoncfg.load(empireJsonFile)
		# parse the travelTime from start to finish
		if (C3PO.reachedInTime(self.milleniumFalconJson, empireJson)):
			pass
		return 0

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
initialize = C3PO(milleniumFalconJsonFile)
print(C3PO.giveMeTheOdds(initialize, empireJsonFile))
