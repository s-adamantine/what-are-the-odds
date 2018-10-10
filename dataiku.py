import json

class C3PO:
	def __init__(self, milleniumFalconJsonFile):
		self.milleniumFalconJsonFile = milleniumFalconJsonFile

	def reachedInTime(milleniumFalconJson):
		total = 0
		autonomy = milleniumFalconJson['autonomy']
		for routes in milleniumFalconJson['routes']:
			# add the travel times until it reaches the first instance of Endor
			total += routes['travelTime']
			if total % autonomy == 0:
				total += 1
			if (routes['destination'] == "Endor" and total > 6):
				return False
		return True

	def giveMeTheOdds(milleniumFalconJsonFile, empireJsonFile): 
		milleniumFalconJson = json.load(open(milleniumFalconJsonFile))
		empireJson = json.load(open(empireJsonFile))
		# parse the travelTime from start to finish
		if (C3PO.reachedInTime(milleniumFalconJson)):
			pass
		return 0

milleniumFalconJsonFile = "./millenium-falcon.json"
empireJsonFile = "./empire.json"
print(C3PO.giveMeTheOdds(milleniumFalconJsonFile, empireJsonFile))
