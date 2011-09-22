#!/usr/bin/env python

from gnuradio import modulation_utils, gr
from optparse import OptionParser
from gnuradio.eng_option import eng_option
import tuntap

class my_top_block(gr.top_block):

    def __init__(self, mod_class, demod_class,
                 rx_callback, options):
					 
		gr.top_block.__init__(self)
					 
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


    def send_pkt(self, payload='', eof=False):
        return self.txpath.send_pkt(payload, eof)

    def carrier_sensed(self):
        """
        Return True if the receive path thinks there's carrier
        """
        return self.rxpath.carrier_sensed()


def main():
	#mods = modulation_utils.type_1_mods()
	#demods = modulation_utils.type_1_demods()
	
	#print mods.keys()
    
	#parser = OptionParser (option_class=eng_option, conflict_handler="resolve")
	#expert_grp = parser.add_option_group("Expert")
	#expert_grp.add_option("", "--rx-freq", type="eng_float", default=None, help="set Rx frequency to FREQ [default=%default]", metavar="FREQ")
	#expert_grp.add_option("", "--tx-freq", type="eng_float", default=None, help="set transmit frequency to FREQ [default=%default]", metavar="FREQ")
	#parser.add_option("-m", "--modulation", type="choice", choices=mods.keys(), default='gmsk', help="Select modulation from: %s [default=%%default]" % (', '.join(mods.keys()),))
	#parser.add_option("-v","--verbose", action="store_true", default=False)
	#expert_grp.add_option("-c", "--carrier-threshold", type="eng_float", default=30, help="set carrier detect threshold (dB) [default=%default]")
	#expert_grp.add_option("","--tun-device-filename", default="/dev/net/tun", help="path to tun device file [default=%default]")
                                                  
	#for mod in mods.values():
		#mod.add_options(expert_grp)

	#for demod in demods.values():
		#demod.add_options(expert_grp)

	#(options, args) = parser.parse_args ()
	#if len(args) != 0:
		#parser.print_help(sys.stderr)
		#sys.exit(1)

	# open the TUN/TAP interface
	(tun_fd, tun_ifname) = tuntap.open_tun_interface(options.tun_device_filename)

    # Attempt to enable realtime scheduling
	r = gr.enable_realtime_scheduling()
	if r == gr.RT_OK:
		realtime = True
	else:
		realtime = False
		print "Note: failed to enable realtime scheduling"
		
	stdout, stderr, retcode = command.exec_command('sysctl -w net.core.wmem_max=1048576')
	print stdout   
	stdout, stderr, retcode = command.exec_command('sysctl -w net.core.rmem_max=50000000')
	print stdout   
        
        
	mac = tuntap.cs_mac(tun_fd, verbose=True)
        
	# build the graph (PHY)
	tb = my_top_block(mods[options.modulation],
                      demods[options.modulation],
                      mac.phy_rx_callback,
                      options)

	mac.set_top_block(tb)    # give the MAC a handle for the PHY
    
    
	print "modulation:     %s"   % (options.modulation,)
	print "freq:           %s"      % (eng_notation.num_to_str(options.tx_freq))
	print "bitrate:        %sb/sec" % (eng_notation.num_to_str(tb.txpath.bitrate()),)
	print "samples/symbol: %3d" % (tb.txpath.samples_per_symbol(),)
    
	print
	print "Allocated virtual ethernet interface: %s" % (tun_ifname,)
	print "You must now use ifconfig to set its IP address. E.g.,"
	print
	print "  $ sudo ifconfig %s 192.168.200.1" % (tun_ifname,)
	print
	print "Be sure to use a different address in the same subnet for each machine."
	print


	tb.start()    # Start executing the flow graph (runs in separate threads)

	mac.main_loop()    # don't expect this to return...

	tb.stop()     # but if it does, tell flow graph to stop.
	tb.wait()     # wait for it to finish


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
