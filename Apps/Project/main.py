#!/usr/bin/env/python

from gnuradio import gr

from gnuradio import blks2
from gnuradio import uhd
import pkg_usrp
import time
import Behaviors

from multiprocessing import Process
from multiprocessing import Pool
		
def main():
	
	def stuff(bs):

		
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
		
	bs_downlink_freq = 900e6
	bs_uplink_freq = 930e6
	
	user_uplink_freq = 960e6
	user_downlink_freq = 990e6
	

		
	bs = Behaviors.BS("192.168.40.1")
	fr = Behaviors.FR("192.168.40.2", "192.168.40.3")
	user1 = Behaviors.User("192.168.40.4")
	#user2 = Behaviors.User("192.168.40.5")	
		
		
	bs.phy.tb.start()
	bs.phy.usrp.set_tx_freq(bs_downlink_freq)
	bs.phy.usrp.set_rx_freq(bs_uplink_freq)
	
	fr.bs_down.tb.start()
	fr.bs_down.usrp.set_tx_freq(user_downlink_freq)
	fr.bs_down.usrp.set_rx_freq(user_uplink_freq)
	
	fr.bs_up.tb.start()
	fr.bs_up.usrp.set_tx_freq(bs_uplink_freq)
	fr.bs_up.usrp.set_rx_freq(bs_uplink_freq)
	
	user1.phy.usrp.set_tx_freq(user_uplink_freq)
	user1.phy.usrp.set_rx_freq(user_downlink_freq)
		
	#user2.phy.usrp.set_tx_freq(user_uplink_freq)
	#user2.phy.usrp.set_rx_freq(bs_downlink_freq)
	
	p = Process(target=stuff, args=(bs,))

	
	raw_input('Press Enter to quit: ')
	p.start()
	p.join()
	
	raw_input('Press Enter to quit: ')
	bs.phy.tb.stop()
	fr.bs_down.tb.stop()
	fr.bs_up.tb.stop()
	user1.phy.tb.stop()

	
def main2():
		
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
