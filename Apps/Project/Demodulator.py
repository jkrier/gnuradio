from gnuradio import gr
from gnuradio import blks2

class Demodulator(gr.gr_hier_block2)
	
	def __init__(self, "Demodulator",
					gr.io_signature(1,1, gr.sizeof_complex),
					gr.io_signature(1,1,gr.sizeof_complex)):
		
		demod = blks2.dqpsk_demod(
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
	
	
