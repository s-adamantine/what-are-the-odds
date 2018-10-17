import jsoncfg

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
