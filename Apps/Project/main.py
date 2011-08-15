#!/usr/bin/env/python

from gnuradio import gr
import Physical_Layer
from gnuradio import blks2
from gnuradio import uhd
import pkg_usrp
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
	app.phy.encoder.send_pkt()
	
	raw_input('Press Enter to quit: ')	
	app.phy.tb.stop()

	
if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		pass
