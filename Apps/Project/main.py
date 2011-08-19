#!/usr/bin/env/python

from gnuradio import gr

from gnuradio import blks2
from gnuradio import uhd
import pkg_usrp
import time
import Behaviors
import stupid

from multiprocessing import Process
from multiprocessing import Pool
		
def main():
		
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
		
	bs_downlink_freq = 920e6
	bs_uplink_freq = 930e6
	
	#user_uplink_freq = 960e6
	#user_downlink_freq = 990e6
	

		
	bs = Behaviors.BS("192.168.40.1")
	fr = Behaviors.FR("192.168.40.2", "192.168.40.3")
	#user1 = Behaviors.User("192.168.40.4")
	#user2 = Behaviors.User("192.168.40.5")	
		
		
	bs.phy.tb.start()
	bs.phy.usrp.set_tx_freq(bs_downlink_freq)
	bs.phy.usrp.set_rx_freq(bs_uplink_freq)
	
	fr.bs_down.tb.start()
	#fr.bs_down.usrp.set_tx_freq(bs_downlink_freq)
	fr.bs_down.usrp.set_rx_freq(bs_downlink_freq)
	
	fr.bs_up.tb.start()
	fr.bs_up.usrp.set_tx_freq(bs_uplink_freq)
	#fr.bs_up.usrp.set_rx_freq(bs_uplink_freq)
	
	#user1.phy.usrp.set_tx_freq(user_uplink_freq)
	#user1.phy.usrp.set_rx_freq(user_downlink_freq)
		
	#user2.phy.usrp.set_tx_freq(user_uplink_freq)
	#user2.phy.usrp.set_rx_freq(bs_downlink_freq)
	
	
	raw_input('Press Enter to quit: ')
	while 1:
		bs.phy.queue.send_pkt('a'*1500)
		time.sleep(0.5)
		fr.bs_up.queue.send_pkt('b'*1500)
		time.sleep(0.5)

	
	raw_input('Press Enter to quit: ')
	bs.phy.tb.stop()
	fr.bs_down.tb.stop()
	fr.bs_up.tb.stop()
	#user1.phy.tb.stop()

def main2():
		
	bs = stupid.BaseStation()
	fr = stupid.FemtoRelay()
	
	bs.tb.start()
	fr.tb.start()
	
	raw_input('Press Enter to send a packet: ')
	freq = 925e6
	while 1:
		bs.usrp.set_tx_freq(freq)
		fr.usrp.set_rx_freq(freq)
		bs.queue.send_pkt('a'*1500)
		time.sleep(1)

	
	raw_input('Press Enter to quit: ')
	bs.tb.stop()
	fr.tb.stop()
	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
