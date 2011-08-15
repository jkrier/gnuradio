#!/usr/bin/env python

from gnuradio import gr
from gnuradio import audio
from gnuradio import uhd
from gnuradio import blks2
			
class block():
		
	def conn(self):
				
		self.sink.set_samp_rate(200e3)
		self.sink.set_center_freq(900e6)
		self.sink.set_antenna("TX/RX", 0)
		self.sink.set_gain(0,0)
		
		self.tb.connect((self.vec, 0), (self.mod, 0))
		self.tb.connect((self.mod, 0), (self.sink, 0))
	
	def disconnect(self):
		self.tb.disconnect_all()
		
	def __init__(self):	
	
		self.tb = gr.top_block()	
		self.sampling_freq = 200e6
		self.ampl = 0.1
		self.ipaddr = "addr=192.168.40.2"
		
		self.sink = uhd.usrp_sink(
			device_addr="addr=192.168.40.2",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		
		self.vec = gr.vector_source_b((0, 0, 0), True, 1)
		self.mod = blks2.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)
		
		
class block2():
		
	def conn(self):
		
		self.sink = uhd.usrp_sink(
			device_addr="addr=192.168.40.2",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.sink.set_samp_rate(200e3)
		self.sink.set_center_freq(950e6)
		self.sink.set_antenna("TX/RX", 0)
		self.sink.set_gain(0,0)
		
		self.tb.connect((self.vec, 0), (self.mod, 0))
		self.tb.connect((self.mod, 0), (self.sink, 0))
	
	def disconnect(self):
		self.tb.disconnect_all()
		
	def __init__(self):		
	
		self.sampling_freq = 200e6
		self.ampl = 0.1
		self.ipaddr = "addr=192.168.40.2"	
		self.tb = gr.top_block()
				
		self.vec = gr.vector_source_b((0, 0, 0), True, 1)
		self.mod = blks2.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)

if __name__ == '__main__':
	
	b = block()
	b2 = block2()
	b.conn()
	b.tb.start()
	raw_input('Press Enter to quit: ')
	b.tb.stop()
	b.disconnect()
	
	b2.conn()
	b2.tb.start()
	raw_input('Press Enter to quit: ')
	b2.tb.stop()
	
	#fg = build_graph()
	#fg.connect()
	#fg.start()
	#raw_input('Press Enter to quit: ')
	#fg.stop()
	#del fg
	#fg = build_graph2()
	#fg.start()
	#raw_input('Press Enter to quit: ')
	#fg.stop()
	#del fg
	#fg = build_graph()	
	#fg.start()
	#raw_input('Press Enter to quit: ')
	#fg.stop()	
	#del fg
