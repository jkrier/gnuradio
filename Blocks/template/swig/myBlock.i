/* -*- c++ -*- */

GR_SWIG_BLOCK_MAGIC(myModule,myBlock);

myBlock_sptr make_myBlock (int param1);

class myBlock : public gr_sync_block
{
private:
  int d_param1;
  myBlock (int param1);  

public:
  int param1 () const { return d_param1; }
  void set_param1 (int param1) { d_param1 = param1; }

};