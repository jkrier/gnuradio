from fcntl import ioctl
import os
import struct
import commands

IFF_TUN		= 0x0001   # tunnel IP packets
IFF_TAP		= 0x0002   # tunnel ethernet frames
IFF_NO_PI	= 0x1000   # don't pass extra packet info
IFF_ONE_QUEUE	= 0x2000   # beats me ;)
TUNSETIFF = 0x400454ca

class Network():
	
	def open_tun_interface(self, instructions=True, tun_device_filename="/dev/net/tun"):
      
		mode = IFF_TAP #| IFF_NO_PI
		
		tun = os.open(tun_device_filename, os.O_RDWR)
		ifs = ioctl(tun, TUNSETIFF, struct.pack("16sH", "gr%d", mode))
		ifname = ifs[:16].strip("\x00")
		
		if instructions:
			print
			print "Allocated virtual ethernet interface: %s" % (ifname,)
			print "You must now use ifconfig to set its IP address. E.g.,"
			print
			print "  $ sudo ifconfig %s 192.168.200.1" % (ifname,)
			print
			print "Be sure to use a different address in the same subnet for each machine."
			print
		
		return (tun, ifname)
		
	def check_for_data_to_send(self, max_length_bytes):		
			payload = os.read(self.tun_fd, max_length_bytes)
			
			if(payload):
				self.datalink.send_pkt(payload)
				msg = "Tx %d bytes" % len(payload)
				self.debug_msg(msg)
			return payload
		
	def receive_data(payload):
		msg = "Rx %d bytes " % len(payload)
		self.debug_msg(msg)
		os.write(self.tun_fd, payload)	
		
	def set_ip_address(self, ipaddr):
	
		self.ipaddr = ipaddr
			
		conf = "ifconfig %s %s" % (self.ifname, self.ipaddr)
		commands.getoutput(conf)
		
	def debug_msg(self, msg):
		if (self.debug):
			print "Network: ", msg
		
	def set_DataLink(self, datalink):
		self.datalink = datalink
		
	def __init__(self, ipaddr=False, setDataLink=True):
		
		self.debug = False
		(self.tun_fd, self.ifname) = self.open_tun_interface(False)	
		
		if (setDataLink):
			self.set_DataLink(DataLink())
			
		if (ipaddr):
			self.set_ip_address(ipaddr)
		
class DataLink():
	
	def __init__(self):
		
		self.debug = False
		
	def mac(self):
		return True
		
	def debug_msg(self, msg):
		if (self.debug):
			print "DataLink: ", msg
		
	def send_pkt(self, payload):
		if(self.mac()):
			self.phy.send_pkt(payload)
	
	def recv_pkt(self, payload):
		network.receive_data(payload)
			
	def set_phy(self, phy):
		self.phy = phy
		
	def set_Network_Layer(self, network):
		self.network = network
