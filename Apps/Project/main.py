#!/usr/bin/env/python

from gnuradio import gr
import Physical_Layer
from gnuradio import blks2
from gnuradio import uhd
import pkg_usrp
import time
#from gnuradio.qtgui import qtgui

#from PyQt4 import QtGui
import sys, sip

class App():
	def __init__(self):
		self.phy = Physical_Layer.Manager()
				
def main():
	if gr.enable_realtime_scheduling() != gr.RT_OK:
		print "Error: failed to enable realtime scheduling."
	app = App()
	app.phy.tb.start()
	
	raw_input('Press Enter to quit: ')
	#app.phy.queue.send_pkt('a'*1500)
	
	
	
	while 1:
		app.phy.usrp.set_both_freq(900e6)
		app.phy.queue.send_pkt('a'*1500)
		time.sleep(.1)
		
		app.phy.usrp.set_both_freq(950e6)
		app.phy.queue.send_pkt('a'*1500)
		time.sleep(.1)
	
	raw_input('Press Enter to quit: ')	
	print 'received:', app.phy.queue.recv_pkt()
	app.phy.tb.stop()
	
	


	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
