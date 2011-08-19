from gnuradio import gr

from gnuradio import blks2
from gnuradio import uhd

from grc_gnuradio import blks2 as grc_blks2

class USRP():
		
	def set_rx_freq(self, freq):
		self.source.set_center_freq(freq)
		
	def set_tx_freq(self, freq):
		self.sink.set_center_freq(freq)
		
	def set_both_freq(self, freq):
		self.set_tx_freq(freq)
		self.set_rx_freq(freq)
		
	def set_sample_rate(self, rate):
		self.sink.set_samp_rate(rate)
		self.source.set_samp_rate(rate)		
	
	def __init__(self, ipaddr):
		
		self.sampling_freq = 200e3
		self.ipaddr = "addr="+ipaddr
		
		self.sink = uhd.usrp_sink(
			device_addr=self.ipaddr,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1
		)
		self.sink.set_antenna("TX/RX", 0)
		
		self.source = uhd.usrp_source(
			device_addr=self.ipaddr,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1
		)
		
		self.source.set_antenna("RX2", 0)
		self.set_sample_rate(self.sampling_freq)

class Queue():
	
	def __init__(self):
		
		self.txq = gr.msg_queue()
		self.rxq = gr.msg_queue()
		
		self.msg_source = gr.message_source(gr.sizeof_char, self.txq)
		self.msg_sink = gr.message_sink(gr.sizeof_char, self.rxq, True)
		
	def send_pkt(self, payload):
		self.txq.insert_tail(gr.message_from_string(payload))
		
	def recv_pkt(self):
		pkt = ""
		
		if self.rxq.count():
			pkt = self.rxq.delete_head().to_string()
			
		return pkt
		

class BaseStation():
	
	def rx_callback(self, ok, payload):
			
		print 'BaseStation Received a packet!'
		self.decoder.recv_pkt(ok, payload)
	
	def __init__(self):
		self.tb = gr.top_block()
			
		tx_access_code = "0000111100010111"
		rx_access_code = "1100111100010111"
		ip_addr = "192.168.40.1"
		self.pkt_size = 1500
		
		self.usrp = USRP(ip_addr)
		self.queue = Queue()
		
		self.usrp.set_tx_freq(930e6)
		self.usrp.set_rx_freq(800e6)
		
		self.encoder = grc_blks2.packet_mod_b(
			grc_blks2.packet_encoder(
				samples_per_symbol=4,
				bits_per_symbol=2,
				access_code=access_code,
				pad_for_usrp=True,
			),
			payload_length=self.pkt_size,
		)
		
		self.modulator = self.dbpsk = blks2.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)	
		
		self.decoder = grc_blks2.packet_demod_b(
			grc_blks2.packet_decoder(
				access_code=access_code,
				threshold=0,
				callback=lambda ok, payload: self.rx_callback(ok, payload)
			)
		)
		
		self.demodulator = blks2.dbpsk_demod(
				samples_per_symbol=2,
				excess_bw=0.35,
				costas_alpha=0.175,
				gain_mu=0.175,
				mu=0.5,
				omega_relative_limit=0.005,
				gray_code=True,
				verbose=False,
				log=False,
			)
		

								
		
		self.tb.connect((self.queue.msg_source, 0), (self.encoder, 0))		
		self.tb.connect((self.encoder, 0), (self.modulator, 0))
		self.tb.connect((self.modulator, 0), (self.usrp.sink, 0))
			
		self.tb.connect((self.usrp.source, 0), (self.demodulator, 0))
		self.tb.connect((self.demodulator, 0), (self.decoder, 0))
		self.tb.connect((self.decoder, 0), (self.queue.msg_sink, 0))
	
	
	
class FemtoRelay():
	
	def rx_callback(self, ok, payload):
			
		print 'FemtoRelay received a packet!'
		self.decoder.recv_pkt(ok, payload)
	
	def __init__(self):
		self.tb = gr.top_block()
			
		access_code = "0000111100010111"
		ip_addr = "192.168.40.5"
		self.pkt_size = 1500
			
		self.usrp = USRP(ip_addr)
		self.queue = Queue()
		
		
		self.usrp.set_tx_freq(800e6)
		self.usrp.set_rx_freq(930e6)
		
		self.encoder = grc_blks2.packet_mod_b(
			grc_blks2.packet_encoder(
				samples_per_symbol=4,
				bits_per_symbol=2,
				access_code=access_code,
				pad_for_usrp=True,
			),
			payload_length=self.pkt_size,
		)
		
		self.modulator = self.dbpsk = blks2.dbpsk_mod(
			samples_per_symbol=2,
			excess_bw=0.35,
			gray_code=True,
			verbose=False,
			log=False,
		)	
		
		self.decoder = grc_blks2.packet_demod_b(
			grc_blks2.packet_decoder(
				access_code=access_code,
				threshold=0,
				callback=lambda ok, payload: self.rx_callback(ok, payload)
			)
		)
		
		self.demodulator = blks2.dbpsk_demod(
				samples_per_symbol=2,
				excess_bw=0.35,
				costas_alpha=0.175,
				gain_mu=0.175,
				mu=0.5,
				omega_relative_limit=0.005,
				gray_code=True,
				verbose=False,
				log=False,
			)
					
		self.tb.connect((self.queue.msg_source, 0), (self.encoder, 0))		
		self.tb.connect((self.encoder, 0), (self.modulator, 0))
		self.tb.connect((self.modulator, 0), (self.usrp.sink, 0))
			
		self.tb.connect((self.usrp.source, 0), (self.demodulator, 0))
		self.tb.connect((self.demodulator, 0), (self.decoder, 0))
		self.tb.connect((self.decoder, 0), (self.queue.msg_sink, 0))
