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
		
	def set_both_freq(self, freq):
		self.set_tx_freq(freq)
		self.set_rx_freq(freq)
		
	def set_sample_rate(self, rate):
		self.sink.set_samp_rate(rate)
		self.source.set_samp_rate(rate)		
	
	def __init__(self, ipaddr):
		
		self.sampling_freq = 200e3
		self.center_freq = 950e6
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
		
		self.set_both_freq(self.center_freq)
		self.set_sample_rate(self.sampling_freq)
		
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
		self.dqpsk = blks2.dqpsk_demod(
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
		
		self.dbpsk = blks2.dbpsk_demod(
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


class Source():
	def __init__(self):
		
		self.vector_b = gr.vector_source_b((0, 0, 0), True, 1)
		
		
class Sink():
	
	def __init__(self):
		
		self.null_sink= gr.null_sink(1)
		
		
class Packet_Encoder():
	
	def __init__(self, code):
		
		self.pkt_size = 1500
		
		self.txpath = grc_blks2.packet_encoder(
			samples_per_symbol=4,
			bits_per_symbol=2,
			access_code=code,
			pad_for_usrp=True,
		)
		self.enc= grc_blks2.packet_mod_b(
                        self.txpath,
                        payload_length=self.pkt_size,
		)
	
	#def send_pkt(self, payload=''):
		#data = (self.pkt_size - 2) * chr(0xff)
		#payload = struct.pack('!H', 0xffff) + data
		
		#return self.txpath.send_pkt(payload)
		
class Packet_Decoder():
	
	
	def rx_callback(self, ok, payload):

		print "Received a packet!"
		self.dec.recv_pkt(ok, payload)
		
		#if (len(payload) > 0):

                	#(pktno,) = struct.unpack('!H', payload[0:2])
                	
                	#n_rcvd += 1

                        #rcvd_rate = 100 * n_rcvd / pktno
                        
                        #print "pktno = %4d  n_rcvd = %4d  len = %4d  ch = %2d  rcvd_rate = %.2f percent" % (
                    		#pktno, n_rcvd, len(payload), ch, rcvd_rate, )
				
	def __init__(self, code):
		self.pkt_size = 1500
		
		self.n_rcvd = 0
		
		self.dec = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code=code,
				threshold=0,
				callback=lambda ok, payload: self.rx_callback(ok, payload)
			)
		)
		
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


class Debug():
	
	def __init__():
		self.probe = gr.probe_avg_mag_sqrd_c(0.001, 30)
		mywindow = window.blackmanharris(self.fft_size)
		self.fft = gr.fft_vcc(self.fft_size, True, mywindow)	
		
		
class Manager():
	
	def __init__(self, ipaddr):
		
		self.tb = gr.top_block()
		
		access_code="0000111100010111"
		
		self.usrp = USRP(ipaddr)
		self.queue = Queue()
		
		self.src = Source()
		self.encoder = Packet_Encoder(access_code)
		self.mod = Modulation()		
								
		#self.tb.connect((self.src.vector_b, 0), (self.encoder.enc, 0))
		
		self.tb.connect((self.queue.msg_source, 0), (self.encoder.enc, 0))		
		self.tb.connect((self.encoder.enc, 0), (self.mod.dbpsk, 0))
		self.tb.connect((self.mod.dbpsk, 0), (self.usrp.sink, 0))
		
		#self.sink = Sink()
		
		self.demod = Demodulation()
		self.decoder = Packet_Decoder(access_code)
		
		self.tb.connect((self.usrp.source, 0), (self.demod.dbpsk, 0))
		self.tb.connect((self.demod.dbpsk, 0), (self.decoder.dec, 0))
		self.tb.connect((self.decoder.dec, 0), (self.queue.msg_sink, 0))
		
		
		
		

