#!/usr/bin/env python
#############################################################################
# 
# Copyright 2011 Georgia Institute of Technology
#
# Title: Benchmark.py
# Author: John Krier
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
from gnuradio import packet_utils
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
import tuntap
import os
import Layer_2_3
import commands


class layout(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Benchmark")
		
		self.debug = False

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
		#"10101011"
		self.mod = blks2.mod_pkts(self.blks2_dxpsk_mod_0,
                           access_code=None,
                           msgq_limit=4,
                           pad_for_usrp=True)
                           
		self.demod = blks2.demod_pkts(self.blks2_dxpsk_demod_0,
						 access_code="10101011",
						 callback=self.rx_callback,
						 threshold=-1)
		
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="addr=192.168.40.5",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_sink_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
		self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="addr=192.168.40.5",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_source_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
		self.uhd_usrp_source_0.set_antenna("RX2", 0)

		
		# Carrier Sensing Blocks
		
		# Parks-McClellen filter options:
		pm_gain = 1           # gain
		pm_sr = 1             # sample rate
		pm_pb = 0.13          # end of passband
		pm_sb = 0.2675        # start of stop band
		pm_pb_ripple = 0.01   # passband ripple (dB)
		pm_sb_atten = 60      # stopband attenuation (dB)
		
		lpf_taps = blks2.optfir.low_pass(pm_gain, pm_sr, pm_pb, pm_sb,
                                      pm_pb_ripple, pm_sb_atten)
                                      
		self.lpf = gr.fft_filter_ccc(1, lpf_taps)
		
		alpha = 0.001
		thresh = 30   # in dB, will have to adjust
		self.probe = gr.probe_avg_mag_sqrd_c(thresh,alpha)
		
		##################################################
		# Connections
		##################################################
		#self.connect((self.msg_source, 0), (self.blks2_packet_encoder_0, 0))
		#self.connect((self.blks2_packet_encoder_0, 0), (self.blks2_dxpsk_mod_0, 0))
		#self.connect((self.blks2_dxpsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))
		self.connect((self.mod, 0), self.uhd_usrp_sink_0)
		
		# connect block input to channel filter
		self.connect((self.uhd_usrp_source_0, 0), (self.lpf, 0))
		self.connect((self.lpf, 0), (self.demod, 0))
		#self.connect((self.uhd_usrp_source_0, 0), (self.demod, 0))
		
		#self.connect((self.lpf, 0), (self.blks2_dxpsk_demod_0, 0))
		#self.connect((self.blks2_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))			
		#self.connect((self.blks2_packet_decoder_0, 0), (self.msg_sink, 0))
		
		# connect the channel input filter to the carrier power detector
		self.connect((self.lpf, 0), (self.probe, 0))

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)
		
	def check_queue(self):
		print 'Tx Queue: %5d' % (self.txq.count())
		print 'Rx Queue: %5d' % (self.rxq.count())

   	def rx_callback(self, ok, payload):
		
		#print "Rx: ok = %r  len(payload) = %4d" % (ok, len(payload))           
		if ok:
			msg = "Rx %d bytes" % len(payload)
			self.debug_msg(msg) 
			self.datalink.recv_pkt(payload)	
			
	def send_pkt(self, payload='', eof=False):
		if ~eof:
			msg = "Tx %d bytes" % len(payload)
			self.debug_msg(msg)

		self.mod.send_pkt(payload, eof)

			
	def set_DataLink_Layer(self, datalink):
		self.datalink = datalink
		
	def debug_msg(self, msg):
		if (self.debug):
			print "Physical: ", msg
    


if __name__ == '__main__':
    try:
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	
	commands.getoutput('sysctl -w net.core.wmem_max=1048576')
	 
	commands.getoutput('sysctl -w net.core.rmem_max=50000000') 
	
	Physical_Layer = layout()
	DataLink_Layer = Layer_2_3.DataLink()
	DataLink_Layer.set_Physical_Layer(Physical_Layer)
	Network_Layer = Layer_2_3.Network()	
	Network_Layer.set_DataLink(DataLink_Layer)
	
	DataLink_Layer.set_Network_Layer(Network_Layer)
	Physical_Layer.set_DataLink_Layer(DataLink_Layer)
	
		
	Physical_Layer.start()
	Physical_Layer.uhd_usrp_sink_0.set_center_freq(930e6, 0)
	Physical_Layer.uhd_usrp_source_0.set_center_freq(930e6, 0)
	
	ipaddr = raw_input('\nEnter an IP Address for this device: ')	
	Network_Layer.set_ip_address(ipaddr)
	
	Network_Layer.debug = False
	Physical_Layer.debug = True
	
	while True:
		Network_Layer.check_for_data_to_send(10*1024)
		time.sleep(0.01)
		
    except KeyboardInterrupt:
        pass
