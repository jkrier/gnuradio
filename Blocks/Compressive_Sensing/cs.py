class [[CSBlock]](gr.hier_block2):
	def __init__(self):
		gr.hierblock2.__init__(self, "CSBlock",
					gr.io_signature(1,1, gr.sizeof_float),
					gr.io_signature(0,0,0))
					
		B1 = gr.block1()
		B2 = gr.block2()
		
		self.connect(self, B1, B2, self)
