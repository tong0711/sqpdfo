# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 11:28:36 2014

@author: jaco_da
"""

# SMOP compiler runtime support library
# Copyright 2014 Victor Leikehman

# MIT license

"""
Main differences between Matlab matrices and numpy arrays
=========================================================

#. Array indices start with one, not with zero.  Accordingly, the last
   element of an N-element array is N, not N-1 as in C.

#. Matrix elements are ordered column-first, aka "Fortran" order.

#. Arrays auto-expand on out-of-bound lhs indexing.

#. In matlab, arrays can be updated before they are created::

      clear a
      a(17) = 42

   is legal in matlab, but not in numpy

#. Array data is not shared by copying or slice indexing. Instead there
   is copy-on-write.

#. There are no zero or one-dimensional arrays. Scalars are
   two-dimensional rather than zero=dimensional as in numpy.

#. Single subscript implies ravel.

#. Boadcasting rules are different

Coexistence of matlab matrices and numpy arrays
===============================================

#. Empty vector::

        []                  matlabarray()

#. Scalars are 1x1 matrices::

        17                  [[ 17 ]]

#. Rectangular char arrays::

        'hello world'       char('hello world')

#. Row vector::

        [1 2 3]             [[1, 2, 3]]

#. Column vector::
 
        [1;2;3]             [[1], [2], [3]]

#. Cell strings::

        cellstr('abc','hello',[97 98 99])       


(*) Such expressions _are_ legal in Octave.  TBD

"""
import version
from numpy import inf
import scipy
import numpy as np
import os,sys,copy
try:
    from scipy.io import loadmat
except:
    pass
import unittest
from version import __version__

def isvector_or_scalar(a):
    """
    one-dimensional arrays having shape [N],
    row and column matrices having shape [1 N] and
    [N 1] correspondingly, and their generalizations
    having shape [1 1 ... N ... 1 1 1].
    Scalars have shape [1 1 ... 1].
    Empty arrays dont count
    """
    try:
        return a.size and a.ndim-a.shape.count(1) <= 1
    except:
        return False
def isvector(a):
    """
    one-dimensional arrays having shape [N],
    row and column matrices having shape [1 N] and
    [N 1] correspondingly, and their generalizations
    having shape [1 1 ... N ... 1 1 1]
    """
    try:
        return a.ndim-a.shape.count(1) == 1
    except:
        return False

class matlabarray(np.ndarray):
    """
    >>> matlabarray()
    matlabarray([], shape=(0, 0), dtype=float64)
    """

    #def __new__(cls,a=[],dtype=None):
     #   cls.obj = np.array(a,
      #                 dtype=dtype,
       #                copy=False,
        #               order="F",
         #              ndmin=2).view(cls).copy(order="F")
        #if cls.obj.size == 0:
         #   cls.obj.shape = (0,0)
        #return cls.obj

#Unveränderte Funktion
    def __new__(cls,a=[],dtype=None):
        cls = np.array(a,
                       dtype=dtype,
                       copy=False,
                       order="F",
                       ndmin=2).view(cls).copy(order="F")
        if cls.size == 0:
            cls.shape = (0,0)
        return cls

    #def __new__(cls,a=[],dtype=None):
    #    original = np.array(a,
     #                  dtype=dtype,
      #                 copy=False,
       #                order="F",
        #               ndmin=2)#.copy(order="F")					
        ##print "original", original																							
        ##myoriginal = original[0]																							
        #cls = original.view(cls).copy(order="F")
        #print "original", original								
        #cls.original = original								
        #if cls.size == 0:
        #    cls.shape = (0,0)
        #return cls

    #def __array_finalize__(self,obj):

    def __mul__(self, other):
        print "HERE mul"
        #return matlabarray(float(self) * other[1])
        print "self\n", self, "\nother\n", other
        if self.shape == (1,1):
            print "self[1]", float(self[1]), "other", other									
            #sys.exit(1)																								
            return float(self[1]) * other
            #sys.exit(1)												
        elif other.shape == (1,1):
            print "self", self, "other[1]", float(other[1])
            #sys.exit(1)																								
            return np.dot(self , float(other[1]))
        ret = np.dot(self, other)            
        print "ret", ret, "\n-------\n"																		
        return ret
								
    def __rmul__(self, other):
        print "HERE rmul"
        #return matlabarray(float(self) * other[1])
        print "self\n", self, "\nother\n", other
        ret = np.dot(other, self)								
        print "ret", ret, "\n-------\n"					
        return ret
								
    def dot(self, other):
        return np.multiply(self, other)								
								
    def __eq__(self, other):
        #print "npa array self", np.array(self)
        #print "np array other", np.array(other)								
        #print "np comparisoon",np.array(self) == np.array(other)
        if other is None:
            return False									
        elif type(other) is list:#len(self) != len(other):
            return self in other
        elif (type(other) is float or type(other) is int):
		if self.shape == (1,1):
		      return float(other) == float(self)
		else:
			return False								
        if self.shape != other.shape:
            return False									
        print "self", self, "other", other												
        return (np.array(self) == np.array(other)).all()
								
    #def T(self):								
    #    if self.shape == (1,1):
    #        print "DO SOMETHIONG"																					
    #    else:
    #        return super(self).T									

    def __copy__(self):
        return np.ndarray.copy(self,order="F")

    def __iter__(self):
        """ must define iter or char won't work"""
        return np.asarray(self).__iter__()

    def compute_indices(self,index):
        if not isinstance(index,tuple):
           index = index,
        if len(index) != 1 and len(index) != self.ndim:
            raise IndexError
        indices = []
        for i,ix in enumerate(index):
            if ix.__class__ is end:
                indices.append(self.shape[i]-1+ix.n)
            elif ix.__class__ is slice:
                if self.size == 0 and ix.stop is None:
                    raise IndexError
                if len(index) == 1:
                    n = self.size
                else:
                    n = self.shape[i]
                indices.append(np.arange((ix.start or 1)-1,
                                          ix.stop  or n,
                                          ix.step  or 1,
                                          dtype=int))
            else:
                try:
                    indices.append(int(ix)-1)
                except:
                    indices.append(np.asarray(ix).astype("int32")-1)
        if len(indices) == 2 and isvector(indices[0]) and isvector(indices[1]):
            indices[0].shape = (-1,1)
            indices[1].shape = (-1,)
        return tuple(indices)

    def __getslice__(self,i,j):
        if i == 0 and j == sys.maxsize:
            return self.reshape(-1,1,order="F")
        return self.__getitem__(slice(i,j))

    def __getitem__(self,index):
        return matlabarray(self.get(index))

    def get(self,index):
        #import pdb; pdb.set_trace()
        indices = self.compute_indices(index)
        if len(indices) == 1:
            return np.ndarray.__getitem__(self.reshape(-1,order="F"),indices)
        else:
            return np.ndarray.__getitem__(self,indices)

    def __setslice__(self,i,j,value):
        print "__setslice__ i,j", i, j					
        								
        if i == 0 and j == sys.maxsize:
            index = slice(None,None)
        else:
            index = slice(i,j)
        self.__setitem__(index,value)
        
    def sizeof(self,ix):
        if isinstance(ix,int):
            n = ix+1
        elif isinstance(ix,slice):
            n = ix.stop
        elif isinstance(ix,(list,np.ndarray)):
            n = max(ix)+1
        else:
            assert 0,ix
        if not isinstance(n,int):
            raise IndexError
        return n 

    def __setitem__(self,index,value):
        print "value at start of set item", value					
        #if type(index) is tuple:
        #    if len(index) == 2:									
        #        print "__setitem__ index: ", index					
        #        print "self.shape", self.shape
        #        if index[0] == slice(None,None,None) and index[1] >= self.shape[1]:
        #        ##concatenate/append column									
        #            ret = concatenate_([self, value.T], axis=1)								
	#																		
      #              #newshape = (self.shape[0], index[1])																
      #              #print "newshape", newshape																				
      #              #np.asarray(self).resize(newshape)
      #              #print "resized self", self																				
      #              #super(self).__setitem__(index, value)																				
      #              #self.__dict__ = ret.__dict__																				
      #              print "ret", ret												
      #              self.__class__ = int#ret																				
      #              return #ret												
      #          elif index[1] == slice(None,None,None) and index[0] >= self.shape[0]:
      #          ##concatenate/append row
      #              ret = concatenate_([self, value])								
      #              #self.__dict__ = ret.__dict__																																								
      #              print "ret", ret																								
      #              return #ret											
									
        #import pdb; pdb.set_trace()
        indices = self.compute_indices(index)
        try:
            if len(indices) == 1:
                np.asarray(self).reshape(-1,order="F").__setitem__(indices,value)
            else:
                np.asarray(self).__setitem__(indices,value)
        except (ValueError,IndexError):
            #import pdb; pdb.set_trace()
            if not self.size:
                new_shape = [self.sizeof(s) for s in indices]
                print "resizing---", index, value, indices, new_shape																
                self.resize(new_shape,refcheck=0)
                np.asarray(self).__setitem__(indices,value)
            elif len(indices) == 1:
                # One-dimensional resize is only implemented for
                # two cases:
                #
                # a. empty matrices having shape [0 0]. These
                #    matries may be resized to any shape.  A[B]=C
                #    where A=[], and B is specific -- A[1:10]=C
                #    rather than A[:]=C or A[1:end]=C
                if self.size and not isvector_or_scalar(self):
                    raise IndexError("One-dimensional resize "
                                     "works only on vectors, and "
                                     "row and column matrices")
                # One dimensional resize of scalars creates row matrices
                # ai = 3
                # a(4) = 1
                # 3 0 0 1
                n = self.sizeof(indices[0]) # zero-based
                if max(self.shape) == 1:
                    new_shape = list(self.shape)
                    new_shape[-1] = n
                else:
                    new_shape = [(1 if s==1 else n) for s in self.shape]
                self.resize(new_shape,refcheck=0)
                np.asarray(self).reshape(-1,order="F").__setitem__(indices,value)
            else:
                new_shape = list(self.shape)
                if self.flags["C_CONTIGUOUS"]:
                    new_shape[0] = self.sizeof(indices[0])
                elif self.flags["F_CONTIGUOUS"]:
                    new_shape[-1] = self.sizeof(indices[-1])
                self.resize(new_shape,refcheck=0)
                print "indices", indices
                print "value", value
                print "np.asarray(self)", np.asarray(self)																
                np.asarray(self).__setitem__(indices,value)

    def __repr__(self):
        return self.__class__.__name__ + repr(np.asarray(self))[5:]

    def __str__(self):
        return str(np.asarray(self))
 
    def __add__(self,other):
        return matlabarray(np.asarray(self)+np.asarray(other))

    def __neg__(self):
        return matlabarray(np.asarray(self).__neg__())
								
    #def zzzQuatsch():
    #    print "quatsch"								

class end(object):
    def __add__(self,n):
        self.n = n
        return self
    def __sub__(self,n):
        self.n = -n
        return self
####
class cellarray(matlabarray):
    """
    Cell array corresponds to matlab ``{}``


    """

    def __new__(cls, a=[]):
        """
        Create a cell array and initialize it with a.
        Without arguments, create an empty cell array.

        Parameters:
        a : list, ndarray, matlabarray, etc.

        >>> a=cellarray([123,"hello"])
        >>> print a.shape
        (1, 2)

        >>> print a[1]
        123

        >>> print a[2]
        hello
        """
        obj = np.array(a,
                       dtype=object,
                       order="F",
                       ndmin=2).view(cls).copy(order="F")
        if obj.size == 0:
            obj.shape = (0,0)
        return obj

    def __getitem__(self,index): 
        return self.get(index)

#    def __str__(self):
#        if self.ndim == 0:
#            return ""
#        if self.ndim == 1:
#            return "".join(s for s in self)
#        if self.ndim == 2:
#            return "\n".join("".join(s) for s in self)
#        raise NotImplementedError


class cellstr(matlabarray):
    """
    >>> s=cellstr(char('helloworldkitty').reshape(3,5))
    >>> s
    cellstr([['hello', 'world', 'kitty']], dtype=object)
    >>> print s
    hello
    world
    kitty
    >>> s.shape
    (1, 3)
    """

    def __new__(cls, a):
        """
        Given a two-dimensional char object,
        create a cell array where each cell contains
        a line.
        """
        obj = np.array(["".join(s) for s in a], 
                       dtype=object,
                       copy=False,
                       order="C",
                       ndmin=2).view(cls).copy(order="F")
        if obj.size == 0:
            obj.shape = (0,0)
        return obj

    def __str__(self):
        return "\n".join("".join(s) for s in self.reshape(-1))

    def __getitem__(self,index): 
        return self.get(index)


class char(matlabarray):
    """
    class char is a rectangular string matrix, which
    inherits from matlabarray all its features except
    dtype.

    >>> s=char()
    >>> s.shape
    (0, 0)

    >>> s=char('helloworld').reshape(2,5)
    >>> print s
    hello
    world

    >>> s.shape
    (2, 5)
    """

    def __new__(cls, a=""):
        if not isinstance(a,str):
            raise NotImplementedError
        obj = np.array(list(a),
                       dtype='|S1',
                       copy=False,
                       order="F",
                       ndmin=2).view(cls).copy(order="F")
        if obj.size == 0:
            obj.shape = (0,0)
        return obj

    def __getitem__(self,index): 
        return self.get(index)

    def __str__(self):
        if self.ndim == 0:
            return ""
        if self.ndim == 1:
            return "".join(s for s in self)
        if self.ndim == 2:
            return "\n".join("".join(s) for s in self)
        raise NotImplementedError
								
    #def __eq__(self, other):
     #   #print "npa array self", np.array(self)
      #  #print "np array other", np.array(other)								
       # #print "np comparisoon",np.array(self) == np.array(other)
        #if type(other) is list:#len(self) != len(other):
         #   return self in other
        #if self.shape != other.shape:
         #   return False									
        #print "self", self, "other", other												
        #return (np.array(self) == np.array(other)).all()


def abs_(a):
    """
    Unless the argument is already as subclass of ndarray,
    convert the argument to ndarray, then apply numpy.abs
    """
    return np.abs(np.asanyarray(a))

def arange_(start,stop,step=1,**kwargs):
    """
    >>> a=arange_(1,10) # 1:10
    >>> size_(a)
    matlabarray([[ 1, 10]])
    """
    return matlabarray(np.arange(start,
                                 stop+1,
                                 step,
                                 **kwargs).reshape(1,-1),**kwargs)

def ceil_(a):
    """
    Unless the argument is already as subclass of ndarray,
    convert the argument to ndarray, then apply numpy.ceil
    """
    return np.ceil(np.asanyarray(a))

def cell_(*args):
    if len(args) == 1:
        args += args
    return cellarray(np.zeros(args,dtype=object,order="F"))

def copy_(a):
    return matlabarray(np.asanyarray(a).copy(order="F"))

def disp_(*args):
    print (args)

false = False

def false_(*args):
    if len(args) == 1:
        args += args
    return np.zeros(args,dtype=bool,order="F")

def find_(a,n=None,d=None,nargout=1):
    if d:
        raise NotImplementedError

    # there is no promise that nonzero or flatnonzero
    # use or will use indexing of the argument without
    # converting it to array first.  So we use asarray
    # instead of asanyarray
    if nargout == 1:
        i = np.flatnonzero(np.asarray(a)).reshape(1,-1)+1
        print "a\n", a
        print "i\n", i	
        if isempty_(i):
            return matlabarray([])
												
        if n is not None:
            i = i.take(range(n))
        return matlabarray(i)
    if nargout == 2:
        i,j = np.nonzero(np.asarray(a))
        if n is not None:
            i = i.take(n)
            j = j.take(n)
        return (matlabarray((i+1).reshape(-1,1)),
                matlabarray((j+1).reshape(-1,1)))
    raise NotImplementedError

def floor_(a):
    return np.floor_(np.asanyarray(a))

def fopen_(*args):
    try:
        fp = open(*args)
        assert fp != -1
        return fp
    except:
        return -1

def fullfile_(*args):
    return os.path.join(*args)

def intersect_(a,b,nargout=1):
    if nargout == 1:
        c = sorted(set(a) & set(b))
        if isinstance(a,str):
            return "".join(c)
        elif isinstance(a,list):
            return c
        else:
            # FIXME: the result is a column vector if
            # both args are column vectors; otherwise row vector
            return np.array(c)
    raise NotImplementedError

#def inf_(*args):
#    t = np.empty(np.prod(args))
#    t[:] = np.inf
#    return t.reshape(args)
#
#Inf_ = inf_
#
#def int_(t):
#    return np.int(t)
#
#def int32_(t):
#    return np.int(t)
#

def iscellstr_(a):
    return isinstance(a,cellarray) and all(isinstance(t,str) for t in a)

def ischar_(a):
    try:
        return a.dtype == "|S1"
    except AttributeError:
        return False

def isempty_(a):
    try:
        return 0 in np.asarray(a).shape
    except AttributeError:
        return False

def isequal_(a,b):
    return np.array_equal(np.asanyarray(a),
                          np.asanyarray(b))
                          
def isscalar_(a):
    """np.isscalar returns True if a.__class__ is a scalar
    type (i.e., int, and also immutable containers str and
    tuple, but not list.) Our requirements are different"""
    try:
        return a.size == 1
    except AttributeError:
        return np.isscalar(a)

def length_(a):
    try:
        return max(np.asarray(a).shape)
    except ValueError:
        return 1

try:
    def load_(a):
        return loadmat(a) # FIXME
except:
    pass

def max_(a, d=None):
    if d is not None:
        return np.maximum(a,d)
    else:
        return np.amax(a)

def min_(a, d=None, nargout=None):#, nargout=0):
    print "a", a
#    print "len(a)", len(a)				
    if isempty_(a):
        ret = matlabarray([])					
    elif d is not None:
        ret = np.minimum(a,d)
    else:
        ret = np.amin(a)
								
    if nargout == 2:
        if isempty_(a):
            ret2 = matlabarray([])									
        else:
            ret2 = np.argmin(a)												
        return ret, ret2
    else:
        return ret								

def mod_(a,b):
    try:
        return a % b
    except ZeroDivisionError:
        return a
def ndims_(a):
    return np.asarray(a).ndim

def numel_(a):
    return np.asarray(a).size

#def ones_(*args,**kwargs):
#    #zs = np.ones(shape)
#    #print "os", zs				
#    #return matlabarray(zs)
#    if not args:
#        return 1.0
#    print "args", args								
#    print "args ones", np.ones(shape=args)				
#    #print "ones args", args[0].cls
#    #print "ones type args", type(args)				
#    return matlabarray(np.ones(args))
				
				#,order="F",**kwargs))
    #return matlabarray(np.ones(shape[1]))
				
#recent one				
#def ones_(*args,**kwargs):
#    if not args:
#        return 1.0
#    #if len(args) == 1:
#    #    print "helllooo!"					
#    #    args += args
#    #print tuple(args)								
#    print "ones_:"								
#    print "args", args								
#    ret = matlabarray(np.ones(args,order="F",**kwargs))				
#    print "ret", ret				
#    print "----"				
#    return ret

def rand_(*args,**kwargs):
    if not args:
        return np.random.rand()
    if len(args) == 1:
        args += args
    try:
        return np.random.rand(np.prod(args)).reshape(args,order="F")
    except:
        pass

def ravel_(a):
    return np.asanyarray(a).reshape(-1,1)

def round_(a):
    return np.round(np.asanyarray(a))

def rows_(a):
    return np.asarray(a).shape[0]

def size_(a, b=0, nargout=1):
    """
    >>> size_(zeros_(3,3)) + 1
    matlabarray([[4, 4]])
    """
    s = np.asarray(a).shape
    if s is ():
        return 1 if b else (1,)*nargout
    # a is not a scalar
    try:
        if b:
            return s[b-1]
        else:
            return matlabarray(s) if nargout <= 1 else s
    except IndexError:
        return 1

def strread_(s, format="", nargout=1):
    if format == "":
        a = [float(x) for x in s.split()]
        return tuple(a) if nargout > 1 else np.asanyarray([a])
    raise NotImplementedError

def strrep_(a,b,c):
    if isinstance(a,str):
        return a.replace(b,c)
    raise NotImplementedError # cell arrays

def sum_(a, dim=None):
    if dim is None:
        return np.asanyarray(a).sum()
    else:
        return np.asanyarray(a).sum(dim-1)

def toupper_(a):
    return char(str(a.data).upper())

true = True

def true_(*args):
    if len(args) == 1:
        args += args
    return matlabarray(np.ones(args,dtype=bool,order="F"))


def zeros_(*args,**kwargs):
    if not args:
        return 0.0

    if type(args[0]) is matlabarray:
        print "zeros_:"								
    #print "args[0]", [rg for rg in args[0]]
    #for rg in args:
    #    print "type rg", type(rg)					
    #    print "rg", rg								
								
    #print "---look at args[0]---"								
    #for rg0 in args[0]:
    #    print "type rg0", type(rg0)
    #    print "rg0", rg0		
								
        print "\nargs[0] as array", np.asarray(args[0])[0]
        print "type args[0] as array", type(np.asarray(args[0])[0])
        ret = matlabarray(np.zeros(np.asarray(args[0])[0], *args[1:],order="F",**kwargs))
        print "ret", ret				
        print "----"
    else:
        print "np.zeros(args)"					
        ret = matlabarray(np.zeros(args, **kwargs))
    return ret

#def zeros_(*args):#shape, *args,**kwargs):
#    #if not args:
#    #    return 0.0
#    #if len(args) == 1:
#    #    args += args
#    #return matlabarray(np.zeros(args,**kwargs))
#    #print "shape", shape
#    zs = np.zeros(args)#np.zeros(shape)
#    print "zs", zs				
#    return matlabarray(zs)

def ones_(*args,**kwargs):
    if not args:
        return 0.0

    if type(args[0]) is matlabarray:
        print "ones_:"								
    #print "args[0]", [rg for rg in args[0]]
    #for rg in args:
    #    print "type rg", type(rg)					
    #    print "rg", rg								
								
    #print "---look at args[0]---"								
    #for rg0 in args[0]:
    #    print "type rg0", type(rg0)
    #    print "rg0", rg0		
								
        print "\nargs[0] as array", np.asarray(args[0])[0]
        print "type args[0] as array", type(np.asarray(args[0])[0])
        ret = matlabarray(np.ones(np.asarray(args[0])[0], *args[1:],order="F",**kwargs))
        print "ret", ret				
        print "----"
    else:
        print "np.zeros(args)"					
        ret = matlabarray(np.ones(args, **kwargs))
    return ret
				
#------------------------------------------------------------------------------
#				Added Functions Start here.
#------------------------------------------------------------------------------
# -> convert to matlab arrays before returning
# -> remove additional arguments. *args **kwargs only where necessary makes debugging easier.

def eig_(A, nargout=1, *args,**kwargs):
	if nargout == 1:
		return np.linalg.eigvals(A)
	else:
		return np.linalg.eig(A)
	
def diag_(A, *args,**kwargs):
	return np.array(np.diag(A))
	
def isreal_(A, *args,**kwargs):
	return np.isreal(A)
	
def isnan_(A,*args,**kwargs):
	return np.isnan(A)
	
def isinf_(A, *args,**kwargs):
	return np.isinf(A)
	
def cond_(A, *args,**kwargs):
	return np.linalg.cond(A)
	
def svd_(A, full_matrices=1, *args,**kwargs):
	return np.linalg.svd(A, full_matrices)
	
def norm_(A, *args,**kwargs):
	return np.linalg.norm(A)
	
def pinv_(A):
	return np.linalg.pinv(A)

def fprintf_(*args,**kwargs):
	print args, kwargs	
	
def eye_(n):
	return matlabarray(np.eye(n))
	
def concatenate_(arrs, axis=0):
	for arr in arrs:
		if isempty_(arr):
			arrs.remove(arr)
	print "concatenate arrs", arrs			
	return matlabarray(np.concatenate(arrs, axis))
	
def sort_(A):
	return np.sort(A)
	
def isfield_(obj, name):
	return obj.__dict__.has_key(str(name))
	
def lower___(strng):
	print "Warning: Lower just returns the string as it is"
	return strng
	
def lower__(strng):
	return lower___(strng)
	
def regexprep___(string1, string2, string3):
	print "Warning: regexprep__ just returns the string(1) as it is"
	return string1
	
def regexprep__(string1, string2, string3):
	return regexprep___(string1, string2, string3)

def strtrim___(strng):
	print "Warning: strtrim___ just returns the string as it is"
	return strng

def strtrim__(strng):
	return strtrim___(strng)
	
def any_(A):
	return A.any()
	
def sqrt_(x):
	return np.sqrt(x)

def real_(x):
	ret = np.real(x)
	print "type np real ret", type(ret)
	return ret

def exp_(x):
	return np.exp(x)
	
def num2str_(num):
	return str(num)

def strcmp_(s1, s2):	
	#print "compare strings:"
	#print "s1", s1
	#print "s2", s2
	if s1 == s2:
		return 1
	else:
		return 0		

def null_(A, eps=1e-15):
	u, s, vh = scipy.linalg.svd(A)
	padding = max(0,np.shape(A)[1]-np.shape(s)[0])
	null_mask = np.concatenate(((s <= eps), np.ones((padding,),dtype=bool)),axis=0)
	null_space = scipy.compress(null_mask, vh, axis=0)
	return scipy.transpose(null_space)		
#def null_(A, eps=1e-15):
#    u, s, vh = scipy.linalg.svd(A)
#    null_mask = (s <= eps)
#    null_space = scipy.compress(null_mask, vh, axis=0)
#    return scipy.transpose(null_space)		
#def null_(A, eps=1e-3):
	#u,s,vh = np.linalg.svd(A,full_matrices=1,compute_uv=1)
	#print "u", u
	#print "s", s
	#print "vh", vh
	#null_space = np.compress(s <= eps, vh, axis=0)
	#return null_space.T

def int2str_(val):
	return str(val)
	
def full_(A):
	print "full_ just returns A"
	return A

if __name__ == "__main__":
    import doctest
    doctest.testmod()

def tf_mapper(x):
	#print "x", x
	if x:
		return 1
	else:
		return 0
				
def logical_or_(a,b):
	vtf_mapper = np.vectorize (tf_mapper)
	ret = np.logical_or(a,b)				
	return vtf_mapper(ret)
	
def strcat_(*args):
	ret = ""
	for arg in args:
		ret = ret + str(arg)
		
	print "strcat_:", ret
	return char(ret)
	
	

# vim:et:sw=4:si:tw=60