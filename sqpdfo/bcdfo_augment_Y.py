# -*- coding: utf-8 -*-

from sqpdfo.runtime import *
from sqpdfo.bcdfo_build_QR_of_Y import bcdfo_build_QR_of_Y_

def bcdfo_augment_Y_(Ynew=None,Y=None,whichmodel=None,shift_Y=None,Delta=None,normgx=None,kappa_ill=None,*args,**kwargs):
    """
#
#  Augment the interpolation set by adding new vector(s).  This assumes that,
#  on entry, the polynomial is not yet fully quadratic. If this is the case,
#  the current interpolation set (and the associated polynomial degree) are
#  increased by the number of columns in Ynew and a new factorization of the
#  (possibly shifted) matrix is computed.
#
#  INPUT:
#
#  Ynew        : the new vectors to add to the interpolation set
#  Y           : a matrix whose columns contain the current interpolation points
#  whichmodel  : kind of model to build
#  shift_Y     : 0 if no shift in interpolation points, 1 otherwise
#  Delta       : trust-region radius
#  normgx      : infinity norm of the projected gradient
#  kappa_ill   : threshold to declare a system matrix as ill-conditioned
#
#  OUTPUT:
#
#  p1          : the updated number of points in set Y
#  QZ, RZ      : the QR factors of the (possibly shifted) matrix containing
#                the polynomial expansion of the updated interpolation points,
#  Y           : a matrix whose columns contain the updated interpolation points
#  xbase       : the updated base point,
#  scale       : the updated model diagonal scaling.
#
#  PROGRAMMING: Ph. Toint and A. Troeltzsch, April 2009.
#               (This version 12 IX 2010)
#
#  DEPENDENCIES: bcdfo_build_QR_of_Y
#
#  TEST:
#  Y = [ 0 1 0 2 0 ; 0 0 1 0 2 ];
#  [ QZ, RZ, xbase, scale ] = bcdfo_build_QR_of_Y(  Y, 0, 0, 1, 1, 1e15 );
#  [ p1, QZ, RZ, Y, xbase, scale ] = bcdfo_augment_Y( [1;0.01], Y, 0, 0, 1, ...
#       1, 1e15 )
#  gives
#  p1 =
#
#     6
#
#  QZ =
#
#    1.0000         0         0         0         0         0
#         0   -0.8944         0   -0.4472         0         0
#         0         0   -0.8944         0   -0.4472         0
#         0   -0.4472         0    0.8944         0         0
#         0         0   -0.4472         0    0.8944         0
#         0         0         0         0         0    1.0000
#
#  RZ =
#
#    1.0000    1.0000    1.0000    1.0000    1.0000    1.0000
#         0   -1.1180         0   -2.6833         0   -1.1180
#         0         0   -1.1180         0   -2.6833   -0.0090
#         0         0         0    0.8944         0         0
#         0         0         0         0    0.8944   -0.0044
#         0         0         0         0         0    0.0100
#
#  Y =
#
#         0    1.0000         0    2.0000         0    1.0000
#         0         0    1.0000         0    2.0000    0.0100
#
#  xbase =
#
#     0
#     0
#
#  scale =
#
#     1
#     1
#     1
#     1
#     1
#     1
#
#  In the scaled case:
#  Y = [ 0 1 0 2 0 ; 0 0 1 0 2 ];
#  [ QZ, RZ, xbase, scale ] = bcdfo_build_QR_of_Y(  Y, 0, 1, 1, 1, 1e15 );
#  [ p1, QZ, RZ, Y, xbase, scale ] = bcdfo_augment_Y( [1;0.01], Y, 0, 1, 1, ...
#      1, 1e15 )
#  gives
#  p1 =
#
#     6
#
#  QZ =
#
#    1.0000         0         0         0         0         0
#         0   -0.9701         0   -0.2425         0         0
#         0         0   -0.9701         0   -0.2425         0
#         0   -0.2425         0    0.9701         0         0
#         0         0   -0.2425         0    0.9701         0
#         0         0         0         0         0    1.0000
#
#  RZ =
#
#    1.0000    1.0000    1.0000    1.0000    1.0000    1.0000
#         0   -0.5154         0   -1.0914         0   -0.5154
#         0         0   -0.5154         0   -1.0914   -0.0049
#         0         0         0    0.2425         0         0
#         0         0         0         0    0.2425   -0.0012
#         0         0         0         0         0    0.0025
#
#  Y =
#
#         0    1.0000         0    2.0000         0    1.0000
#         0         0    1.0000         0    2.0000    0.0100
#
#  xbase =
#
#     0
#     0
#
#  scale =
#
#    1.0000
#    0.5000
#    0.5000
#    0.2500
#    0.2500
#    0.2500
#
#  CONDITIONS OF USE: Use at your own risk! No guarantee of any kind given.
#
    """   
    
#    varargin = cellarray(args)
#    nargin = 7-[Ynew,Y,whichmodel,shift_Y,Delta,normgx,kappa_ill].count(None)+len(args)

    n,p1=size_(Y,nargout=2)
    if ((p1 >= ((n + 1) * (n + 2)) / 2) and (whichmodel != 3)):
        disp_(' === augment_Y: warning!!! The interpolation is already fully quadratic!')
        disp_('     Ignoring augmentation...')
        QZ,RZ,xbase,scale=bcdfo_build_QR_of_Y_(Y,whichmodel,shift_Y,Delta,normgx,kappa_ill,nargout=4)
    else:
        Y=concatenate_([Y, Ynew], axis=1)
        p1=p1 + size_(Ynew,2)
        QZ,RZ,xbase,scale=bcdfo_build_QR_of_Y_(Y,whichmodel,shift_Y,Delta,normgx,kappa_ill,nargout=4)
    return p1,QZ,RZ,Y,xbase,scale