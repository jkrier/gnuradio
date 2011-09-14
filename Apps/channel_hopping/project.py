CHANNEL_LIST = [890e6, 900e6, 905e6] 	# Needs to be 3 until code is improved
CCH_FREQ = 420e6			# Common Control channel frequency
SAMP_RATE = 200e3			# Sample Rate
PU_RX_GAIN = 0				# PU Receiver gain
PU_TX_GAIN = 0				# PU Transmitter gain
CR_RX_TRANSMIT_GAIN = 10		# Really the control channel transmit gain
CR_TX_TRANSMIT_GAIN = 10		# Really the data channel transmit gain
TUNE_DELAY_SECS = 0.1			# Time to wait after re-tuning
DWELL_DELAY_SECS = 0.1			# Time to wait after sending a packet? Probably not.
RECEIVE_WINDOW_SECS = 2			# After 2 seconds request next packet burst
PACKET_SIZE = 1500			# Packet Size
FFT_SIZE = 1024				# FFT Window - larger is more acurate, smaller is faster
THRESHOLD = -40				# dB that will identify a primary user	
SWITCH_WINDOW_SECS = 2	

PU_IP_ADDR = "addr=192.168.40.1"
CR_RX_IP_ADDR = "addr=192.168.40.3"
CR_TX_IP_ADDR = "addr=192.168.40.4"	

# 7 inch small antenna bands
# 144 MHz, 430 MHz, 1200 MHz Tri-band
# 118-160, 250-290, 360-390, 420-470, 820-960 MHz
#
#
# 9 inch larger antenna bands
# 824-960 MHz, 1710-1990 MHz Quad-band 
# Cellular/PCS and ISM band

# Control Channel Protocol

CCH_ACCESS = "0101101010100101"

CTRL_SEND_DATA_0 = 0x01		#Send on channel 1
CTRL_SEND_DATA_1 = 0x02		#Send on channel 2
CTRL_SEND_DATA_2 = 0x03		#Send on channel 3

CTRL_NUM_PKTS = 5

# Data Channel

DCH_ACCESS = "0000111100010000"
CR_DATA_NUM_PKTS = 15

# PU Channel
PU_ACCESS = "0000111100010111"
PU_DATA_NUM_PKTS = 2
PU_HOPS_PER_FREQ = 15



