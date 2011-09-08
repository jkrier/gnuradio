#!/usr/bin/env python
#############################################################################
# 
# Copyright 2011 Georgia Institute of Technology
#
# Title: Benchmark.py
# Author: Brandon Lo, John Krier
#
# This example demonstrates the frequency hopping between two channels and
# is used to generate the primary user traffic that occupies two out of
# three channels, leaving one channel of white space for opportunistic
# access. 
#
#############################################################################

from gnuradio import blks2
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import window
from gnuradio.eng_option import eng_option
from gnuradio.gr import firdes
from gnuradio.wxgui import constsink_gl
from gnuradio.wxgui import scopesink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import numpy
import wx
import random, time, struct, sys, math

class layout(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Benchmark")

		##################################################
		# Variables
		##################################################
		self.ch_freq = 920e6						    		# Hz
		self.samp_rate = samp_rate = 200e3      	# Samples/second
		self.tx_gain = 10             		# dB
		self.rx_gain = 0           		# dB
		self.pkt_size = 1000		       	# bytes
		self.target_throughput_bps =	100e3
                
		##################################################
		# Blocks
		##################################################
		self.blks2_dxpsk_demod_0 = blks2.dqpsk_demod(
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
		self.blks2_dxpsk_mod_0 = blks2.dqpsk_mod(
			samples_per_symbol=4,
			excess_bw=0.3,
			gray_code=True,
			verbose=False,
			log=False,
		)
		self.blks2_packet_decoder_0 = grc_blks2.packet_demod_b(grc_blks2.packet_decoder(
				access_code="10101011",
				threshold=0,
				#callback=lambda ok, payload: self.blks2_packet_decoder_0.recv_pkt(ok, payload),
				callback=lambda ok, payload: self.rx_callback(ok, payload),
			),
		)
		self.txpath = grc_blks2.packet_encoder(
			samples_per_symbol=4,
			bits_per_symbol=2,
			access_code="10101011",
			pad_for_usrp=True,
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(
                        self.txpath,
                        payload_length=self.pkt_size,
		)
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="addr=192.168.40.1",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_sink_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
		self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="addr=192.168.40.1",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_source_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
		self.uhd_usrp_source_0.set_antenna("RX2", 0)
		
		self.txq = gr.msg_queue()
		self.rxq = gr.msg_queue()
		self.msg_source = gr.message_source(gr.sizeof_char, self.txq)
		self.msg_sink = gr.message_sink(gr.sizeof_char, self.rxq, True)
		
		##################################################
		# Connections
		##################################################
		self.connect((self.msg_source, 0), (self.blks2_packet_encoder_0, 0))
		self.connect((self.blks2_packet_encoder_0, 0), (self.blks2_dxpsk_mod_0, 0))
		self.connect((self.blks2_dxpsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))
		
		self.connect((self.uhd_usrp_source_0, 0), (self.blks2_dxpsk_demod_0, 0))
		self.connect((self.blks2_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))			
		self.connect((self.blks2_packet_decoder_0, 0), (self.msg_sink, 0))

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		
	def check_queue(self):
		print 'Tx Queue: %5d' % (self.txq.count())
		print 'Rx Queue: %5d' % (self.rxq.count())

   	def rx_callback(self, ok, payload):
		
		global n_rcvd, n_sent
		
		n_rcvd += 1
		rate = 100 * n_rcvd / n_sent
		#print n_sent
		#print n_rcvd
		self.check_queue()
		print "Packet Rate = %.8f%%" %rate

		self.blks2_packet_decoder_0.recv_pkt(ok, payload)

		#if (len(payload) > 0):

			#(pktno,) = struct.unpack('!H', payload[0:2])
			
			#n_rcvd += 1

			#rcvd_rate = 100 * n_rcvd / n_sent
			
			#print "pktno = %4d  n_rcvd = %4d  rcvd_rate = %.2f percent" % (
				#pktno, n_rcvd, rcvd_rate, )


def run():

	global n_rcvd, n_sent

	n_rcvd = 0
	n_sent = 0
	
	def send_pkt(payload=''):
		
		if(~tb.txq.full_p()):
			tb.txq.insert_tail(gr.message_from_string(payload))
		
	def recv_pkt():
		pkt = ""
		
		print tb.rxq.count()
		
		if tb.rxq.count():
			print ';as;dfklasd;fj'
			pkt = self.rxq.delete_head().to_string()
			
		return pkt

	#def send_pkt(payload=''):
		#return tb.txpath.send_pkt(payload)

	# generate and send packets
	pktno = 0
	
	packets_per_second = tb.target_throughput_bps / 8 / tb.pkt_size
	seconds_per_packet = 1/packets_per_second
	
	print "Sleep time = " , seconds_per_packet
	
	while 1:
		
		send_pkt('a'*tb.pkt_size)
		#if(recv_pkt() != ""):
		#	print 'Received a Packet'

		n_sent += 1
		time.sleep(seconds_per_packet)       


if __name__ == '__main__':
    try:
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = layout()
	tb.start()
	tb.uhd_usrp_sink_0.set_center_freq(tb.ch_freq, 0)
	tb.uhd_usrp_source_0.set_center_freq(tb.ch_freq, 0)
	time.sleep(1)
	run()
    except KeyboardInterrupt:
        pass
