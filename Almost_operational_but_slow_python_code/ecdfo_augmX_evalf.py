# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 11:35:26 2014
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%  A new point y is added to the set of all points X. The objective function is 
%  evaluated at y and the function value is added to fX (or the model value
%  of the dummy point y is replaced by its real function value in fX).
%
%  INPUTS:
%
%  f           : function handle of the function to evaluate
%  y           : the point which is added to X
%  m           : index where to place y in X
%  X           : set of all points
%  fX          : function (or model) values associated to X
%  nfix        : number of fixed variables
%  xfix        : contains the values of the fixed variables
%  indfix      : fixed indices of x
%  indfree     : free indices of x
%  fxmax       : maximal allowed function value 
%                (to avoid infinity in the calculation)
%  neval       : actual number of function evaluations
%  maxeval     : maximal allowed number of function evaluations
%  verbose     : level of printing (from calling routine)
%  xstatus     : status vector if points contained in current interpolation set
%  xstatus_val : value, if new point y will be contained in interpolation set or not
%  sstatus     : status vector if points in lie in current subspace
%  dstatus     : status vector if points are dummy points
%  scaleX		: scaling of variables is applied
%  scalefacX	: scaling factors 
%
%  OUTPUTS:
%
%  X           : updated set of all points
%  fX          : updated set of function values associated with X
%  neval       : updated number of function evaluations
%  xstatus     : updated status vector if points contained in current interpolation set
%  sstatus     : updated status vector if points in lie in current subspace
%  dstatus     : updated status vector if points are dummy points
%
%  PROGRAMMING: A. Troeltzsch, August 2010. 
%
%  DEPENDENCIES: -
%
%  TEST:
%  X = [ 0 1 0 ; 0 0 1 ];
%  fX = [ 1 100 101 ];
%  y = [ 2; 4 ];
%
%  To put y on 4-th position in the set X call:
%  [X, fX, neval, xstatus, sstatus, dstatus] = ecdfo_augmX_evalf(@banana, ...
%     y, 4, X, fX, 0, [0;0], [], [1 2 3], 1e25, 3, 100, 1, ...
%     0, [1 1 1], 1, [1 1 1], [ 0 0 0], 0, [ 1, 1])
%  where
%     function fx = banana( x )
%     fx  = 100 * ( x(2) - x(1)^2 ) ^2 + (1-x(1))^2;
%
%  which gives
%  X =
%     0     1     0     2
%     0     0     1     4
%  fX =
%     1     100     101   1
%  neval =
%     4
%  xstatus =
%     1     1     1     1
%  sstatus =
%     1     1     1     1
%  dstatus =
%     0     0     0     0
%
%  CONDITIONS OF USE: Use at your own risk! No guarantee of any kind given.
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

@author: jaco_da
"""

# Autogenerated with SMOP version 
# c:\Users\jaco_da\AppData\Local\Continuum\Anaconda\Scripts\smop-script.py ecdfo_augmX_evalf.m

from __future__ import division
#try:
from runtime import *
#except ImportError:
    #from smop.runtime import *
from copy import copy

def ecdfo_augmX_evalf_(f=None,y=None,m=None,X_=None,fX_=None,ciX_=None,ceX_=None,nfix=None,xfix=None,indfix=None,indfree=None,fxmax=None,neval_=None,xstatus_=None,xstatus_val=None,sstatus_=None,dstatus_=None,scaleX=None,scalefacX=None,info_=None,options=None,values=None,*args,**kwargs):
#    varargin = cellarray(args)
#    nargin = 22-[f,y,m,X,fX,ciX,ceX,nfix,xfix,indfix,indfree,fxmax,neval,xstatus,xstatus_val,sstatus,dstatus,scaleX,scalefacX,info,options,values].count(None)+len(args)

    X=copy_(X_)
    fX=copy_(fX_)
    ciX=copy_(ciX_)
    ceX=copy_(ceX_)
    neval=copy(neval_)
    xstatus=copy_(xstatus_)
    xstatus=copy_(xstatus_)
    sstatus=copy_(sstatus_)
    dstatus=copy_(dstatus_)
    info=copy(info_)
    
    

    full_n=length_(xfix)
    I=eye_(full_n)
    xstatus[m]=xstatus_val
    sstatus[m]=1
    dstatus[m]=0
    if (nfix > 0):
        yfull=I[:,indfix] * xfix[indfix] + I[:,indfree] * y
        X[:,m]=yfull
        if (scaleX):
            yfull=yfull / scalefacX
        info.nsimul[2]=info.nsimul(2) + 1
        outdic,fvalue,info.ci,info.ce=f(2,yfull)
        info.f=fvalue
    else:
        if isempty_(X):
            X=copy_(y)
        else:
            X[:,m]=y
        info.nsimul[2]=info.nsimul[2] + 1
        outdic,fvalue,info.ci,info.ce=f(2,y)
        info.f=fvalue
    if outdic == 1:
        if options.verbose:
            fprintf_(options.fout,'### ecdfo_augmX_evalf: initial point x is out of domain\n\n')
        info.flag=values.fail_on_simul
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    if isnan_(fvalue):
        if options.verbose:
            fprintf_(options.fout,'### ecdfo_augmX_evalf: f is NaN at the point x\n\n')
            x=copy_(y)
        info.flag=values.fail_on_simul
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    if isinf_(fvalue):
        if options.verbose:
            fprintf_(options.fout,'### ecdfo_augmX_evalf: f is Inf at the point x\n\n')
            x=copy_(y)
        info.flag=values.fail_on_simul
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    if outdic:
        info=sqplab_badsimul_(outdic,info,options,values)
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    if not isempty_(info.ci) and size_(info.ci,2) != 1:
        if options.verbose:
            fprintf_(options.fout,'### ecdfo_augmX_evalf: the computed ci must be a column vector\n\n')
        info.flag=values.fail_on_simul
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    if not isempty_(info.ce) and size_(info.ce,2) != 1:
        if options.verbose:
            fprintf_(options.fout,'### ecdfo_augmX_evalf: the computed ce must be a column vector\n\n')
        info.flag=values.fail_on_simul
        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
    fX[m]=min_(fxmax,real_(fvalue))
    if not isempty_(info.ci):
        if isempty_(ciX):
            ciX=real_(info.ci)							
        else:
            ciX[:,m]=real_(info.ci)
#        ciX[:,m]=real_(info.ci.T)
    if not isempty_(info.ce):
#        ceX[:,m]=real_(info.ce.T)
        if isempty_(ceX):
            ceX=real_(info.ce)						
        else:
            ceX[:,m]=real_(info.ce)

    neval=neval + 1
    return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic

#def ecdfo_augmX_evalf_(f=None,y=None,m=None,X=None,fX=None,ciX=None,ceX=None,nfix=None,xfix=None,indfix=None,indfree=None,fxmax=None,neval=None,xstatus=None,xstatus_val=None,sstatus=None,dstatus=None,scaleX=None,scalefacX=None,info=None,options=None,values=None,*args,**kwargs):
#    #varargin = cellarray(args)
#    #nargin = 22-[f,y,m,X,fX,ciX,ceX,nfix,xfix,indfix,indfree,fxmax,neval,xstatus,xstatus_val,sstatus,dstatus,scaleX,scalefacX,info,options,values].count(None)+len(args)
#
#    full_n=length_(xfix)
#    I=eye_(full_n)
#    xstatus[m]=xstatus_val
#    sstatus[m]=1
#    dstatus[m]=0
#    if (nfix > 0):
#        yfull=I[:,indfix] * xfix[indfix] + I[:,indfree] * y
#        X[:,m]=yfull
#        if (scaleX):
#            yfull=yfull / scalefacX
#        info.nsimul[2]=info.nsimul[2]+ 1
#        #print "f(2,yfull)", 								
#        outdic,fvalue,info.ci,info.ce=f(2,yfull)
#        info.f=fvalue
#    else:
#        #print "X", X#[:,m]
#        #print "X.shape", X.shape
#        #print "m", m								
#        #print "y", y
#        #print "type y", type(y)
#        if X.shape[1] <= m:								
#            X = concatenate_([X, y], axis=1)								
#            #print "concatenate"												
#        else:
#            X[:,m]=y												
#            #print "assignment"												
#										
#        #print "X", X#[:,m]								
#        								
#        #X[:,m]=y
#        if (scaleX):
#            y=y / scalefacX
#        info.nsimul[2]=info.nsimul[2] + 1
#        outdic,fvalue,info.ci,info.ce=f(2,y)
#        info.f=fvalue
#    if outdic == 1:
#        if options.verbose:
#            fprintf_(options.fout,char('### ecdfo_augmX_evalf: initial point x is out of domain\\n\\n'))
#        info.flag=values.fail_on_simul
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    #print "fvalue", fvalue
#    #print "isnan fvalue", isnan_(fvalue)								
#    if isnan_(fvalue):
#        if options.verbose:
#            fprintf_(options.fout,char('### ecdfo_augmX_evalf: f is NaN at the point x\\n\\n'))
#            x=copy_(y)
#        info.flag=values.fail_on_simul
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    if isinf_(fvalue):
#        if options.verbose:
#            fprintf_(options.fout,char('### ecdfo_augmX_evalf: f is Inf at the point x\\n\\n'))
#            x=copy_(y)
#        info.flag=values.fail_on_simul
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    if outdic:
#        info=sqplab_badsimul_(outdic,info,options,values)
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    if not isempty_(info.ci) and size_(info.ci,2) != 1:
#        if options.verbose:
#            fprintf_(options.fout,char('### ecdfo_augmX_evalf: the computed ci must be a row vector\\n\\n'))
#        info.flag=values.fail_on_simul
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    if not isempty_(info.ce) and size_(info.ce,2) != 1:
#        if options.verbose:
#            fprintf_(options.fout,char('### ecdfo_augmX_evalf: the computed ce must be a row vector\\n\\n'))
#        info.flag=values.fail_on_simul
#        return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic
#    fX[m]=min_(fxmax,real_(fvalue))
#    if not isempty_(info.ci):
#        ciX[:,m]=real_(info.ci.T)
#    if not isempty_(info.ce):
#        #ceX[:,m]=real_(info.ce.T)
#        #print "ceX", ceX
#        #print "real_(info.ce.T)", real_(info.ce.T)
#        #print "type real_(info.ce.T)", type(real_(info.ce.T))	
#        #print "info.ce", info.ce								
#        if X.shape[1] <= m: #<= m:								
#            if info.ce.shape == (1,1):
#                
#                info.ce = info.ce * ones_(ceX.shape[0])#.T
#                #print "infoce", info.ce.T																
#            #print "ceX", ceX
#        #print "real_(info.ce.T)", real_(info.ce.T)
#        #print "type real_(info.ce.T)", type(real_(info.ce.T))	
#            #print "ceX", ceX												
#            #print "info.ce.T", info.ce.T								
#        																
#            #ceX = matlabarray(np.concatenate([ceX, real_(info.ce.T)], 1))
#            ceX = concatenate_([ceX, real_(info.ce)], axis=1)								
#            #print "concatenate"												
#        else:
#            ceX[:,m]=real_(info.ce.T)												
#            #print "assignment"								
#    neval=neval + 1
#    return X,fX,ciX,ceX,neval,xstatus,sstatus,dstatus,info,outdic