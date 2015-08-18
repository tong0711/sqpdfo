# -*- coding: utf-8 -*-
"""
Created on Thu Nov 06 11:24:27 2014
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% checks whether matrix A is convex.
% if A is not convex, matrix is convexified by perturbing small
% eigenvalues.
%
% the bigger the value EPS, the more different the matrix gets.
%
% programming: A. Troeltzsch, 2014
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
@author: jaco_da
"""
# Autogenerated with SMOP version 
# c:\Users\jaco_da\AppData\Local\Continuum\Anaconda\Scripts\smop-script.py ecdfo_check_convex.m

from __future__ import division
#try:
from runtime import *
#print "type eig", type(eig_)
#except ImportError:
#    from smop.runtime import *
from numpy import diag, array,isreal,real
from copy import copy
import numpy

def ecdfo_check_convex_(A_=None,options=None,*args,**kwargs):
#    varargin = cellarray(args)
#    nargin = 2-[A,options].count(None)+len(args)

    A=copy(A_)

    ev=numpy.linalg.eigvals(A)
    evneg=ev[ev < 0]
    if not isempty_(evneg):
        ZERO=array([1e-10])
        EPS=array([1e-09])
        d,v=numpy.linalg.eig(A)
        d[d < ZERO]=EPS
        d=diag(d)
        A=v.dot( d .dot( v.T ))
        if not isempty_(find_(~ isreal(A),1)):
            if options.verbose >= 3:
                #This is a little bit weird since we did not test if it was symmetric. Maybe an copy/paste with ecdfo_check_cond ?
                disp_('### ecdfo_check_convex: matrix is non symmetric. Resetting A.')
            A=0.5*(A+A.conj().T)

    #On account of the test asking if there is a non real in A, I suppose that we only want the real parts (also having imaginary parts raise errors on problem 5 in ecdfo_func),
    #hence the real conversion
    return real(A)

#def ecdfo_check_convex_(A=None,options=None,*args,**kwargs):
#    #varargin = cellarray(args)
#    #nargin = 2-[A,options].count(None)+len(args)
#
#    ev=eig_(A)
#    evneg=ev[ev < 0]
#    if not isempty_(evneg):
#        ZERO=1e-10
#        EPS=1e-09
#        d,v=eig_(A,nargout=2)
#        d[d < ZERO]=EPS
#        d=diag_(d)
#        A=v * d * v.T
#        #print "not is real:", ~isreal_(A)
#        if True in np.iscomplex(A):#not isempty_(find_(~isreal_(A),True)):
#            if options.verbose >= 3:
#                disp_(char('### ecdfo_check_convex: matrix is non symmetric. Resetting A.'))
#            A=(A + A.T) * 0.5
#    return A


