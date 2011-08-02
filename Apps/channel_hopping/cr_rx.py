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

class lab3_cr_rx(grc_wxgui.top_block_gui):

	def __init__(self):
		grc_wxgui.top_block_gui.__init__(self, title="Lab3 CR Sense")

		##################################################
		# Variables
		##################################################
		self.ch_freq = Settings.CHANNEL_LIST    		# Hz
		self.ccc_freq = Settings.CCH_FREQ                   	# Hz
		self.samp_rate = samp_rate = Settings.SAMP_RATE      	# Samples/second
		self.tx_gain = Settings.CR_RX_TRANSMIT_GAIN             # dB
		self.rx_gain = 0		                        # dB
		self.tune_delay = Settings.TUNE_DELAY_SECS              # seconds
		self.dwell_delay = Settings.DWELL_DELAY_SECS            # seconds
		self.pkt_size = Settings.PACKET_SIZE		        # bytes
                self.data_burst_of_pkts = Settings.CR_DATA_NUM_PKTS	# number of packets sent
                                                        		# for continuous transmission
                self.ccc_burst_of_pkts = Settings.CTRL_NUM_PKTS		# number of times to repeat control code
		self.fft_size = Settings.FFT_SIZE

		self.dch_freq = self.ch_freq[0]
		self.threshold = Settings.THRESHOLD
                
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
				access_code=Settings.DCH_ACCESS,
				threshold=0,
				callback=lambda ok, payload: self.rx_callback(ok, payload),
			),
		)
		self.txpath = grc_blks2.packet_encoder(
			samples_per_symbol=4,
			bits_per_symbol=2,
			access_code=Settings.CCH_ACCESS,
			pad_for_usrp=True,
		)
		self.blks2_packet_encoder_0 = grc_blks2.packet_mod_b(
                        self.txpath,
                        payload_length=self.pkt_size,
		)
		self.uhd_usrp_sink_0 = uhd.usrp_sink(
			device_addr=Settings.CR_RX_IP_ADDR,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_sink_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_sink_0.set_gain(self.tx_gain, 0)
		self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
		self.uhd_usrp_source_0 = uhd.usrp_source(
			device_addr=Settings.CR_RX_IP_ADDR,
			io_type=uhd.io_type.COMPLEX_FLOAT32,
			num_channels=1,
		)
		self.uhd_usrp_source_0.set_samp_rate(samp_rate)
		#self.uhd_usrp_source_0.set_center_freq(tune_freq, 0)
		self.uhd_usrp_source_0.set_gain(self.rx_gain, 0)
		self.uhd_usrp_source_0.set_antenna("RX2", 0)
		
		##################################################
		# Energy Detector
		##################################################

                s2v = gr.stream_to_vector(gr.sizeof_gr_complex, self.fft_size)

        	mywindow = window.blackmanharris(self.fft_size)
        	fft = gr.fft_vcc(self.fft_size, True, mywindow)
        	c2mag = gr.complex_to_mag_squared(self.fft_size)
        	
        	tune_delay_adj  = max(0, int(round(self.tune_delay * self.samp_rate / self.fft_size)))  # in fft_frames
        	dwell_delay_adj = max(1, int(round(self.dwell_delay * self.samp_rate / self.fft_size))) # in fft_frames

        	self.msgq = gr.msg_queue(16)
        	self._tune_callback = tune(self)        # hang on to this to keep it from being GC'd
        	stats = gr.bin_statistics_f(self.fft_size, self.msgq,
                                    self._tune_callback, tune_delay_adj, dwell_delay_adj)
		
		##################################################
		# Connections
		##################################################
		self.connect((self.blks2_packet_encoder_0, 0), (self.blks2_dxpsk_mod_0, 0))
		self.connect((self.blks2_dxpsk_mod_0, 0), (self.uhd_usrp_sink_0, 0))
		self.connect((self.blks2_dxpsk_demod_0, 0), (self.blks2_packet_decoder_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), (self.blks2_dxpsk_demod_0, 0))
		self.connect((self.uhd_usrp_source_0, 0), s2v, fft, c2mag, stats)

	def set_samp_rate(self, samp_rate):
		self.samp_rate = samp_rate
		self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
		self.uhd_usrp_source_0.set_samp_rate(self.samp_rate)

   	def rx_callback(self, ok, payload):
                global n_rcvd, total_expected_packets, WaitingForData,total_received_packets

		self.blks2_packet_decoder_0.recv_pkt(ok, payload)

		#only count valid packets
		if (len(payload) > 0):

                	(pktno,) = struct.unpack('!H', payload[0:2])
                	
                	n_rcvd += 1
			total_received_packets += 1

                        #rcvd_rate = 100 * total_received_packets / total_expected_packets

            		print "Received Data packet", pktno
            		
    		#if (n_rcvd > self.data_burst_of_pkts-1):
    			#rcvd_rate = 100 * total_received_packets / total_expected_packets
    			#n_rcvd = 0
    			#WaitingForData = 0
            		

	def set_dch_freq(self):	    		
	
        	return self.dch_freq
    			
                    		
class tune(gr.feval_dd):
    """
    This class allows C++ code to callback into python.
    """
    def __init__(self, tb):
        gr.feval_dd.__init__(self)
        self.tb = tb

    def eval(self, ignore):
        """
        This method is called from gr.bin_statistics_f when it wants to change
        the center frequency.  This method tunes the front end to the new center
        frequency, and returns the new frequency as its result.
        """
        try:
            new_freq = self.tb.set_dch_freq()
            return new_freq

        except Exception, e:
            print "tune: Exception: ", e


class parse_msg(object):
    def __init__(self, msg):
        self.center_freq = msg.arg1()
        self.vlen = int(msg.arg2())
        assert(msg.length() == self.vlen * gr.sizeof_float)

        # FIXME consider using Numarray or NumPy vector
        t = msg.to_string()
        self.raw_data = t
        self.data = struct.unpack('%df' % (self.vlen,), t)


def freq_hopping():

        global n_rcvd, total_expected_packets, WaitingForData, Receive_Window, total_received_packets
        
        n_rcvd = 0
        n_right = 0
	ch = 0
	total_expected_packets = 0
	total_received_packets = 0
	
        WaitingForData = 0
        Receive_Window = 0
	Switch_Window = 0
        DesiredFrequency = tb.dch_freq
        
        def send_pkt(payload=''):
                return tb.txpath.send_pkt(payload)
        
        # Set up the CCC for the receiver to transmit on       
        tx_tune = tb.uhd_usrp_sink_0.set_center_freq(tb.ccc_freq, 0)
	if not tx_tune:
        	print "Failed to set TX frequency to", tb.ccc_freq
        	
        # Set up the DCh for the receiver to receive on  
        tx_tune = tb.uhd_usrp_source_0.set_center_freq(tb.dch_freq, 0)
	if not tx_tune:
        	print "Failed to set TX frequency to", tb.dch_freq 

	time.sleep(tb.tune_delay)
	
        # generate and send packets
        pkt_size = tb.pkt_size
        ccc_burst_of_pkts = tb.ccc_burst_of_pkts
        data_burst_of_pkts = tb.data_burst_of_pkts

	times = 0
	
        while 1:
        
                # After packet window expires, compute receive rate
 		if (time.clock() > Receive_Window):
 			if (total_expected_packets):
	 			rate = 100 * total_received_packets / total_expected_packets
	 			print "Reception Rate = %.2f" % rate
				WaitingForData = 0
		
		# Make sure we're not waiting for the last round of packets
		if(not WaitingForData):
		
			################
			# sensing
			################
			# Get the next message sent from the C++ code (blocking call).
			# It contains the center frequency and the mag squared of the fft
			m = parse_msg(tb.msgq.delete_head())
	
			# Make sure the tuner has switched.  This is necessary for a valid fft
			if(m.center_freq == DesiredFrequency or time.clock() > Switch_Window): 
			 	# m.data are the mag_squared of the fft output (they are in the
				# standard order.  I.e., bin 0 == DC.)
				data_sum = math.fsum(m.data)
				data_avg = data_sum/tb.fft_size
				data_db = 10*math.log10(data_avg)

				# Print center freq so we know that something is happening...
				center_freq_MHz = m.center_freq/1e6
				print "Sensing %.3f" % center_freq_MHz + " MHz " + "Power = %.2f" % data_db + " dB"
				
				# If you find a primary user then re-tune and try again
				# This could be improved
				if(data_db > tb.threshold):				
					if (tb.dch_freq == tb.ch_freq[0]):
						tb.dch_freq = tb.ch_freq[1]
					elif (tb.dch_freq == tb.ch_freq[1]):
						tb.dch_freq = tb.ch_freq[2]
					elif (tb.dch_freq == tb.ch_freq[2]):
						tb.dch_freq = tb.ch_freq[0]
													
					print "Primary user detected, switching to %3d" %tb.dch_freq
					status = tb.uhd_usrp_source_0.set_center_freq(tb.dch_freq, 0)
					if not status:
		    				print "Failed to set frequency to", tb.dch_freq
		    			
		    			Switch_Window = time.clock() + Settings.SWITCH_WINDOW_SECS	
		    			DesiredFrequency = tb.dch_freq	
					time.sleep(tb.tune_delay)						
					continue
					
				# Clear channel - transmit away
				else:
					if (tb.dch_freq == tb.ch_freq[0]):
						command = Settings.CTRL_SEND_DATA_0 
					elif (tb.dch_freq == tb.ch_freq[1]):
						command = Settings.CTRL_SEND_DATA_1
					elif (tb.dch_freq == tb.ch_freq[2]):
						command = Settings.CTRL_SEND_DATA_2
			
					n = 0
				 	n_rcvd = 0
					total_expected_packets += data_burst_of_pkts
					WaitingForData = 1
				 	Receive_Window = time.clock() + Settings.RECEIVE_WINDOW_SECS
					while n < ccc_burst_of_pkts:
						# prepare payload of the packet
			
						data = (pkt_size - 2) * '\0'
						payload = struct.pack('!H', command) + data

						# send the packet
						send_pkt(payload)

						n += 1
					
					print "Command = ", command
	
                        
if __name__ == '__main__':
    try:
	parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
	(options, args) = parser.parse_args()
	tb = lab3_cr_rx()
        tb.start()
        freq_hopping()
    except KeyboardInterrupt:
        pass
