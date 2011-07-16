#!/usr/bin/env python
#############################################################################
# 
# Copyright 2011 Georgia Institute of Technology
#
# Class: ECE8863 Cognitive Radio Networks
# Title: Lab3 PU
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

import project as Settings

class lab3_cr_tx(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Lab3 CR Sense")

		##################################################
		# Variables
		##################################################
		self.ch_freq = Settings.CHANNEL_LIST    		# Hz
		self.ccc_freq = Settings.CCH_FREQ                   	# Hz
		self.samp_rate = samp_rate = Settings.SAMP_RATE     	# Samples/second
		self.tx_gain = Settings.CR_TX_TRANSMIT_GAIN             # dB
		self.rx_gain = 0		                        # dB
		self.tune_delay = Settings.TUNE_DELAY_SECS              # seconds
		self.dwell_delay = Settings.DWELL_DELAY_SECS            # seconds
		self.pkt_size = Settings.PACKET_SIZE		        # bytes
                self.data_burst_of_pkts = Settings.CR_DATA_NUM_PKTS	# number of packets sent
                                                        		# for continuous transmission                
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
				access_code=Settings.CCH_ACCESS,
				threshold=0,
				callback=lambda ok, payload: self.rx_callback(ok, payload),
			),
		)
		self.txpath = grc_blks2.packet_encoder(
			samples_per_symbol=4,
			bits_per_symbol=2,
			access_code=Settings.DCH_ACCESS,
			pad_for_usrp=True,
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(
                        self.txpath,
                        payload_length=self.pkt_size,
		)
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr="",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_sink_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
		self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr="",
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_source_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
		self.uhd_usrp_source_0.set_antenna("RX2", 0)
		
		##################################################
		# Connections
		##################################################
		self.connect((self.blks2_packet_encoder_0, 0), (self.blks2_dxpsk_mod_0, 0))
		self.connect((self.blks2_dxpsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))
		self.connect((self.blks2_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.blks2_dxpsk_demod_0, 0))

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

   	def rx_callback(self, ok, payload):
                global pktno, n_rcvd, n_right, ShouldSendData, SendingData

		if(not SendingData):
			self.blks2_packet_decoder_0.recv_pkt(ok, payload)

			if (len(payload) > 0):

		        	(ccc_command,) = struct.unpack('!H', payload[0:2])
		        	
		        	n_rcvd += 1
		        	
				(ccc_cmd,) = struct.unpack('!H', payload[0:2])
				print "Received Control packet, Payload = %2x" % ccc_cmd 
				
				if(ccc_cmd == Settings.CTRL_SEND_DATA_0):
		        		print "Send Data on %3d" % self.ch_freq[0]
					tx_tune = tb.uhd_usrp_sink_0.set_center_freq(self.ch_freq[0], 0)
					if not tx_tune:
						print "Failed to set TX frequency to ", self.ch_freq[0]                 
				
				elif(ccc_cmd == Settings.CTRL_SEND_DATA_1):
				        print "Send Data on %3d" % self.ch_freq[1]
					tx_tune = tb.uhd_usrp_sink_0.set_center_freq(self.ch_freq[1], 0)
					if not tx_tune:
						print "Failed to set TX frequency to ", self.ch_freq[1]			
		                        		
				elif(ccc_cmd == Settings.CTRL_SEND_DATA_2):
		        		print "Send Data on %3d" % self.ch_freq[2]
					tx_tune = tb.uhd_usrp_sink_0.set_center_freq(self.ch_freq[2], 0)
					if not tx_tune:
						print "Failed to set TX frequency to ", self.ch_freq[2]	               		
				else:
					return

			ShouldSendData = 1
					 

def freq_hopping():

        global pktno, n_rcvd, n_right,ShouldSendData, SendingData

      	def send_pkt(payload=''):
        	return tb.txpath.send_pkt(payload)

        n_rcvd = 0
        pktno = 0
        n_right = 0
	SendingData = 0
	ShouldSendData = 0
                
        # Set up the CCC for the transmitter to receive on        
        rx_tune = tb.uhd_usrp_source_0.set_center_freq(tb.ccc_freq, 0)
        if not rx_tune:
                print "Failed to set RX frequency to", target_freq
                
        # Set up the DCh for the transmitter to transmit on       
        tx_tune = tb.uhd_usrp_sink_0.set_center_freq(tb.ch_freq[0], 0)
	if not tx_tune:
        	print "Failed to set TX frequency to", tb.ccc_freq

	time.sleep(tb.tune_delay)
	print "Ready"
        	
	while 1:

		if(ShouldSendData):
			SendingData = 1
			print "Sending %2d" % tb.data_burst_of_pkts + " packets"
		     			
     			time.sleep(tb.tune_delay)
			# send a burst of packets
			n = 0
			while n < tb.data_burst_of_pkts:
				# prepare payload of the packet
				data = (tb.pkt_size - 2) * chr(pktno & 0xff)
				payload = struct.pack('!H', pktno & 0xffff) + data

				# send the packet
				send_pkt(payload)
				print "Sent packet %4d" % pktno

				n += 1
				pktno += 1
				time.sleep(tb.dwell_delay)

			SendingData = 0
			ShouldSendData = 0
        	       

if __name__ == '__main__':
    try:
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = lab3_cr_tx()
        tb.start()
        freq_hopping()
    except KeyboardInterrupt:
        pass
