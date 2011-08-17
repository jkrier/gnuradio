import Physical_Layer

class BS():
	def __init__(self, ipaddr):
		self.phy = Physical_Layer.Manager(ipaddr)

			
class FR():
	def __init__(self, ipaddr1, ipaddr2):
		self.bs_down = Physical_Layer.Manager(ipaddr1)
		self.bs_up = Physical_Layer.Manager(ipaddr2)
	

			
class User():
	def __init__(self, ipaddr):
		self.phy = Physical_Layer.Manager(ipaddr)
	

