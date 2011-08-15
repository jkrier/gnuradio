from gnuradio import gr
from gnuradio import blks2
from gnuradio import uhd
from grc_gnuradio import blks2 as grc_blks2
import struct

class USRP():
		
	def set_rx_freq(self, freq):
		self.source.set_center_freq(freq)
		
	def set_tx_freq(self, freq):
		self.sink.set_center_freq(freq)
		
	def set_sample_rate(self, rate):
		self.sink.set_samp_rate(rate)
		self.source.set_samp_rate(rate)		
	
	def __init__(self, ipaddr):
		
		self.sampling_freq = 200e6
		self.ipaddr = "addr="+ipaddr
		
		self.sink = uhd.usrp_sink(
			device_addr=self.ipaddr,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1
		)
		self.sink.set_samp_rate(200e3)
		self.sink.set_center_freq(950e6)
		self.sink.set_antenna("TX/RX", 0)
		self.sink.set_gain(0,0)
		
		self.source = uhd.usrp_source(
			device_addr=self.ipaddr,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1
		)
		self.source.set_samp_rate(200e3)
		self.source.set_center_freq(950e6)
		self.source.set_antenna("RX2", 0)
		self.source.set_gain(0,0)
		
class Modulation():
	
	def __init__(self):
		
		self.dbpsk = blks2.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)
		
		self.dqpsk = blks2.dqpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)
		
		self.qam8 = blks2.qam8_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)
	
		
class Demodulation():
	def __init__(self):
		self.demod = blks2.dqpsk_demod(
			samples_per_symbol=4,
			excess_bw=0.3,
			costas_alpha=0.175,
			gain_mu=0.175,
			mu=0.5,
			omega_relative_limit=0.005,
			gray_code=True,
			verbose=False,
			log=False,
		)


class Source():
	def __init__(self):
		
		self.vector_b = gr.vector_source_b((0, 0, 0), True, 1)
		
		
class Sink():
	
	def __init__(self):
		
		self.null_sink= gr.null_sink(1)
		
		
class Packet_Encoder():
	
	def __init__(self):
		
		self.pkt_size = 1500
		
		self.txpath = grc_blks2.packet_encoder(
			samples_per_symbol=4,
			bits_per_symbol=2,
			access_code="0000111100010111",
			pad_for_usrp=True,
		)
		self.enc= grc_blks2.packet_mod_b(
                        self.txpath,
                        payload_length=self.pkt_size,
		)
	
	def send_pkt(self, payload=''):
		data = (self.pkt_size - 2) * chr(0xff)
		payload = struct.pack('!H', 0xffff) + data
		
		return self.txpath.send_pkt(payload)
		
class Packet_Decoder():
	def __init__(self):
		
		self.n_rcvd = 0
		
		self.dec = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="0000111100010111",
				threshold=0,
				callback=lambda ok, payload: rx_callback(ok, payload),
			),
		)
		
	def rx_callback(self, ok, payload):

		print "Received a packet!"
		self.dec.recv_pkt(ok, payload)
	
		
		
class Manager():
	
	def __init__(self):
		
		self.tb = gr.top_block()
		
		self.usrp = USRP("192.168.40.2")
		
		self.src = Source()
		self.encoder = Packet_Encoder()
		self.mod = Modulation()		
								
		self.tb.connect((self.src.vector_b, 0), (self.encoder.enc, 0))
		self.tb.connect((self.encoder.enc, 0), (self.mod.dbpsk, 0))
		self.tb.connect((self.mod.dbpsk, 0), (self.usrp.sink, 0))
		
		self.sink = Sink()
		self.demod = Demodulation()
		self.decoder = Packet_Decoder()
		
		self.tb.connect((self.usrp.source, 0), (self.demod.demod, 0))
		self.tb.connect((self.demod.demod, 0), (self.decoder.dec, 0))
		self.tb.connect((self.decoder.dec, 0), (self.sink.null_sink, 0))
		
		
		
		

