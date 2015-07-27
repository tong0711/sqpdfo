# -*- coding: utf-8 -*-
"""
Created on Fri Nov 28 13:59:05 2014
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  Subroutine finds the smallest value in fY, which are the associated function
%  values of the set Y. There are only points inside the bounds considered
%  and those which are and no dummy points!
%  Exchanges the best point in the current interpolation set Y if a smaller
%  function value was found.
%
%  INPUT:
%
%  c           : contains a bunch of constants
%  QZ, RZ      : the QR factors of the (possibly shifted) matrix containing
%                the polynomial expansion of the interpolation points
%  Y           : interpolation set
%  fY          : function values associated to the current interpolation points
%  ind_Y       : indices of the points in Y out of X, the set of all points
%  i_xbest     : index of the best point
%  cur_degree  : number of interpolation points
%  indfree     : number of free variables
%  x           : best point
%  xl, xu      : lower/upper bounds on the variables
%  fx          : best function value
%  dstatus     : status vector of dummy points in X
%  whichmodel  : kind of model to build
%  scale       : model diagonal scaling
%  shift_Y     : 0 if no shift in interpolation points, 1 otherwise
%  Delta       : trust-region radius
%  normgx      : infinity norm of the projected gradient
%  kappa_ill   : threshold to declare a system matrix as ill-conditioned
%
%  OUTPUT:
%
%  (possibly) updated INPUT values
%
%  PROGRAMMING: A. Troeltzsch, August 2010 + March 2013.
%
%  DEPENDENCIES: bcdfo_swap_in_Y
%
%  CONDITIONS OF USE: Use at your own risk! No guarantee of any kind given.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%  Select indices of all points inside the bounds and which are not a dummy point


@author: jaco_da
"""

# Autogenerated with SMOP version 
# c:\Users\jaco_da\AppData\Local\Continuum\Anaconda\Scripts\smop-script.py ecdfo_find_smallf.m

from __future__ import division
#try:
from runtime import *
from copy import copy
#except ImportError:
#from smop.runtime import *
def ecdfo_find_smallf_(c=None,QZ_=None,RZ_=None,Y_=None,fY_=None,ciY_=None,ceY_=None,ind_Y_=None,i_xbest_=None,cur_degree=None,indfree=None,x_=None,xl=None,xu=None,fx=None,dstatus=None,whichmodel=None,scale_=None,shift_Y=None,Delta=None,normgx=None,kappa_ill=None,sigma=None,info_=None,*args,**kwargs):
#    varargin = cellarray(args)
#    nargin = 24-[c,QZ,RZ,Y,fY,ciY,ceY,ind_Y,i_xbest,cur_degree,indfree,x,xl,xu,fx,dstatus,whichmodel,scale,shift_Y,Delta,normgx,kappa_ill,sigma,info].count(None)+len(args)


    info=copy(info_)
    QZ=copy_(QZ_)
    RZ=copy_(RZ_)
    Y=copy_(Y_)
    fY=copy_(fY_)
    ciY=copy_(ciY_)
    ceY=copy_(ceY_)
    x=copy_(x_)
    scale=copy_(scale_)
    ind_Y=copy_(ind_Y_)
    i_xbest=copy_(i_xbest_)

    norm_ceY = zeros_(1,cur_degree)
    dummy_set=find_(dstatus == c.dummy)
    ind_insideBounds=matlabarray([])
    for i in arange_(1,cur_degree).reshape(-1):
        if((isempty_(find_(logical_or_(Y[:,i] < xl[indfree] , Y[:,i] > xu[indfree]),1))) and (isempty_(find_(dummy_set == ind_Y[i],1)))):
            ind_insideBounds[i]=i
        else:
            ind_insideBounds[i]=1
    if length_(ceY) > 0:
        for i in arange_(1,cur_degree).reshape(-1):
            norm_ceY[i]=norm_(ceY[:,i])
    else:
        norm_ceY=zeros_(1,cur_degree)
    meritY=fY + sigma *norm_ceY
    fmin,imin=min_(meritY[ind_insideBounds],nargout=2)
    if (imin != 1 and fmin < meritY[1]):
        QZ,RZ,Y,ind_Y,fY,ciY,ceY,x,scale=ecdfo_swap_in_Y_(1,imin,QZ,RZ,Y,ind_Y,fY,ciY,ceY,x,whichmodel,scale,shift_Y,Delta,normgx,kappa_ill,nargout=9)
        fx=fY[1]
        i_xbest=ind_Y[1]
        if (not shift_Y):
            x=Y[:,1]
    info.f=fY[1]
    if length_(ceY) > 0:
        info.ce=ceY[:,1]
    if length_(ciY) > 0:
        info.ci=ciY[:,1]
    return x,fx,QZ,RZ,Y,fY,ciY,ceY,ind_Y,i_xbest,scale,info
#def ecdfo_find_smallf_(c=None,QZ=None,RZ=None,Y=None,fY=None,ciY=None,ceY=None,ind_Y=None,i_xbest=None,cur_degree=None,indfree=None,x=None,xl=None,xu=None,fx=None,dstatus=None,whichmodel=None,scale=None,shift_Y=None,Delta=None,normgx=None,kappa_ill=None,sigma=None,info=None,*args,**kwargs):
#    #varargin = cellarray(args)
#    #nargin = 24-[c,QZ,RZ,Y,fY,ciY,ceY,ind_Y,i_xbest,cur_degree,indfree,x,xl,xu,fx,dstatus,whichmodel,scale,shift_Y,Delta,normgx,kappa_ill,sigma,info].count(None)+len(args)
#
#    norm_ceY = zeros_(1,cur_degree)
#				
#    dummy_set=find_(dstatus == c.dummy)
#    ind_insideBounds=matlabarray([])
#    for i in arange_(1,cur_degree).reshape(-1):
#        #print "Y[:,i]", Y[:,i]			
#        #print "xl[indfree]", xl[indfree]
#        #print "Y[:,i] < xl[indfree]", Y[:,i] < xl[indfree].T
#        #print "Y[:,i] > xu[indfree]", Y[:,i] > xu[indfree].T
#								
#        #print "np.logical_or(Y[:,i] < xl[indfree] , Y[:,i] > xu[indfree])", np.logical_or(Y[:,i] < xl[indfree].T , Y[:,i] > xu[indfree].T)
#        #print "the type:", type(logical_or_(Y[:,i] < xl[indfree] , Y[:,i] > xu[indfree]))								
#			
#        if ((isempty_(find_(logical_or_(Y[:,i] < xl[indfree].T , Y[:,i] > xu[indfree].T),1))) and (isempty_(find_(dummy_set == ind_Y[i],1)))):
#            ind_insideBounds[i]=i
#        else:
#            ind_insideBounds[i]=1
#    if length_(ceY) > 0:
#        for i in arange_(1,cur_degree).reshape(-1):
#            norm_ceY[i]=norm_(ceY[:,i])
#    else:
#        norm_ceY=zeros_(1,cur_degree)
#    meritY=fY + sigma * norm_ceY#sigma.dot(norm_ceY)
#    fmin,imin=min_(meritY[ind_insideBounds],nargout=2)
#    if (imin != 1 and fmin < meritY[1]):
#        QZ,RZ,Y,ind_Y,fY,ciY,ceY,x,scale=ecdfo_swap_in_Y_(1,imin,QZ,RZ,Y,ind_Y,fY,ciY,ceY,x,whichmodel,scale,shift_Y,Delta,normgx,kappa_ill,nargout=9)
#        fx=fY[1]
#        i_xbest=ind_Y[1]
#        if (not shift_Y):
#            x=Y[:,1]
#    info.f=fY[1]
#    if length_(ceY) > 0:
#        info.ce=ceY[:,1].T
#    if length_(ciY) > 0:
#        info.ci=ciY[:,1].T
#    return x,fx,QZ,RZ,Y,fY,ciY,ceY,ind_Y,i_xbest,scale,info
