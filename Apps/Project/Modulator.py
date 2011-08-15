from gnuradio import gr
from gnuradio import blks2

class Modulator(gr.gr_hier_block2)

	def __init__(self, "Modulator",
					gr.io_signature(1,1, gr.sizeof_float,
					gr.io_signature(1,1,gr.sizeof_complex)):
		
		mod = blks2.dqpsk_mod
		(
			samples_per_symbol=4,
			excess_bw=0.3,
			gray_code=True,
			verbose=False,
			log=False,
		)



