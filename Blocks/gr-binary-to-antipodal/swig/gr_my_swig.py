# This file was automatically generated by SWIG (http://www.swig.org).
# Version 1.3.40
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.

from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_gr_my_swig', [dirname(__file__)])
        except ImportError:
            import _gr_my_swig
            return _gr_my_swig
        if fp is not None:
            try:
                _mod = imp.load_module('_gr_my_swig', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _gr_my_swig = swig_import_helper()
    del swig_import_helper
else:
    import _gr_my_swig
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static) or hasattr(self,name):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


def _swig_setattr_nondynamic_method(set):
    def set_attr(self,name,value):
        if (name == "thisown"): return self.this.own(value)
        if hasattr(self,name) or (name == "this"):
            set(self,name,value)
        else:
            raise AttributeError("You cannot add attributes to %s" % self)
    return set_attr


class SwigPyIterator(object):
    """Proxy of C++ swig::SwigPyIterator class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _gr_my_swig.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self):
        """value(self) -> PyObject"""
        return _gr_my_swig.SwigPyIterator_value(self)

    def incr(self, n = 1):
        """incr(self, size_t n = 1) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator_incr(self, n)

    def decr(self, n = 1):
        """decr(self, size_t n = 1) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator_decr(self, n)

    def distance(self, *args, **kwargs):
        """distance(self, SwigPyIterator x) -> ptrdiff_t"""
        return _gr_my_swig.SwigPyIterator_distance(self, *args, **kwargs)

    def equal(self, *args, **kwargs):
        """equal(self, SwigPyIterator x) -> bool"""
        return _gr_my_swig.SwigPyIterator_equal(self, *args, **kwargs)

    def copy(self):
        """copy(self) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator_copy(self)

    def next(self):
        """next(self) -> PyObject"""
        return _gr_my_swig.SwigPyIterator_next(self)

    def __next__(self):
        """__next__(self) -> PyObject"""
        return _gr_my_swig.SwigPyIterator___next__(self)

    def previous(self):
        """previous(self) -> PyObject"""
        return _gr_my_swig.SwigPyIterator_previous(self)

    def advance(self, *args, **kwargs):
        """advance(self, ptrdiff_t n) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator_advance(self, *args, **kwargs)

    def __eq__(self, *args, **kwargs):
        """__eq__(self, SwigPyIterator x) -> bool"""
        return _gr_my_swig.SwigPyIterator___eq__(self, *args, **kwargs)

    def __ne__(self, *args, **kwargs):
        """__ne__(self, SwigPyIterator x) -> bool"""
        return _gr_my_swig.SwigPyIterator___ne__(self, *args, **kwargs)

    def __iadd__(self, *args, **kwargs):
        """__iadd__(self, ptrdiff_t n) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator___iadd__(self, *args, **kwargs)

    def __isub__(self, *args, **kwargs):
        """__isub__(self, ptrdiff_t n) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator___isub__(self, *args, **kwargs)

    def __add__(self, *args, **kwargs):
        """__add__(self, ptrdiff_t n) -> SwigPyIterator"""
        return _gr_my_swig.SwigPyIterator___add__(self, *args, **kwargs)

    def __sub__(self, *args):
        """
        __sub__(self, ptrdiff_t n) -> SwigPyIterator
        __sub__(self, SwigPyIterator x) -> ptrdiff_t
        """
        return _gr_my_swig.SwigPyIterator___sub__(self, *args)

    def __iter__(self): return self
SwigPyIterator_swigregister = _gr_my_swig.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

class gr_binary_to_antipodal_bf_sptr(object):
    """Proxy of C++ boost::shared_ptr<(gr_binary_to_antipodal_bf)> class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    def __init__(self, *args): 
        """
        __init__(self) -> gr_binary_to_antipodal_bf_sptr
        __init__(self, gr_binary_to_antipodal_bf p) -> gr_binary_to_antipodal_bf_sptr
        """
        this = _gr_my_swig.new_gr_binary_to_antipodal_bf_sptr(*args)
        try: self.this.append(this)
        except: self.this = this
    def __deref__(self):
        """__deref__(self) -> gr_binary_to_antipodal_bf"""
        return _gr_my_swig.gr_binary_to_antipodal_bf_sptr___deref__(self)

    __swig_destroy__ = _gr_my_swig.delete_gr_binary_to_antipodal_bf_sptr
    __del__ = lambda self : None;
gr_binary_to_antipodal_bf_sptr_swigregister = _gr_my_swig.gr_binary_to_antipodal_bf_sptr_swigregister
gr_binary_to_antipodal_bf_sptr_swigregister(gr_binary_to_antipodal_bf_sptr)

gr_binary_to_antipodal_bf_sptr.__repr__ = lambda self: "<gr_block %s (%d)>" % (self.name(), self.unique_id ())


def gr_make_binary_to_antipodal_bf():
  """gr_make_binary_to_antipodal_bf() -> gr_binary_to_antipodal_bf_sptr"""
  return _gr_my_swig.gr_make_binary_to_antipodal_bf()
class gr_binary_to_antipodal_bf(object):
    """Proxy of C++ gr_binary_to_antipodal_bf class"""
    thisown = _swig_property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined")
    __repr__ = _swig_repr
    __swig_destroy__ = _gr_my_swig.delete_gr_binary_to_antipodal_bf
    __del__ = lambda self : None;
gr_binary_to_antipodal_bf_swigregister = _gr_my_swig.gr_binary_to_antipodal_bf_swigregister
gr_binary_to_antipodal_bf_swigregister(gr_binary_to_antipodal_bf)



