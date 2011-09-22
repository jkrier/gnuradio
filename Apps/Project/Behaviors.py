import Physical_Layer

class BS():
	def __init__(self, ipaddr):
		
		self.name = "BaseStation"
		
		self.phy = Physical_Layer.Manager(ipaddr, self.name)

			
class FR():
	def __init__(self, ipaddr1, ipaddr2):
		
		self.name = "FemtoRelay"
		
		self.bs_down = Physical_Layer.Manager(ipaddr1, self.name)
		self.bs_up = Physical_Layer.Manager(ipaddr2, self.name)
	

			
class User():
	def __init__(self, ipaddr):
		
		self.name = "User"
		
		self.phy = Physical_Layer.Manager(ipaddr, self.name)
	
