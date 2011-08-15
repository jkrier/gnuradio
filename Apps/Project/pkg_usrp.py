from gnuradio import uhd

class USRPN210():
	
	def __init__(self, ip, samprate):
		
		self.ipaddr = ip
		self.fs = samprate
		
		self.source = uhd.usrp_source
		(
			self.ipaddr,
			uhd.io_type.COMPLEX_FLOAT32,
			1
		)
		#self.source.set_samp_rate(samprate)
		#self.source.set_antenna("RX2", 0)
		#self.source.set_gain(0,0)
		
		self.sink = uhd.usrp_sink
		(
			self.ipaddr,
			uhd.io_type.COMPLEX_FLOAT32,
			1
		)
		#self.sink.set_samp_rate(samprate)
		#self.sink.set_antenna("TX/RX", 0)
		#self.sink.set_gain(0,0)
		
	def get_Addr(self):
		return self.ipaddr
		
	def set_Addr(self, addr):
		self.ipaddr = addr
		
	def get_SampRate(self):
		return self.fs
				
	def set_SampRate(self, rate):
		source.set_samp_rate(rate)
		sink.set_samp_rate(rate)
		self.fs = rate
		
	def get_Source(self):
		return self.source
	
	def get_Sink(self):
		return self.sink
		
	source = property(get_Source)
	sink = property(get_Sink)
	ipaddr = property(get_Addr, set_Addr)
	fs = property(get_SampRate, set_SampRate)
		
		

		
		
		
		
				

		

		

	
	
	
	
	

		
		

