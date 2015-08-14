# -*- coding: utf-8 -*-
"""
Created on Thu Nov 13 14:55:53 2014
INPUT VALUES
x =

  -1.717000000000000   1.595700000000000   1.827200000000000  -0.763600000000000  -0.763600000000000

OUTPUT VALUES
>> [msg,f,ci,ce] = ecdfo_func(x)
powells func

msg =

     0


f =

   0.053985698962084


ci =

     []


ce =

  -0.000822750000001
   0.000238240000000
   0.001195859492999
@author: jaco_da
"""
import sys
sys.path.append("../")
import unittest
from ecdfo_func import *
#import numpy as np
#import helper
from ecdfo_global_variables import set_prob


class Test_ecdfo_func(unittest.TestCase):
    """
          Reminder :
          This class is a test for ecdfo_func which computes f, ci and ce according to a given problem
    """
    def setUp(self):
        self.x =  matlabarray([ -1.717000000000000,   1.595700000000000,   1.827200000000000,  -0.763600000000000,  -0.763600000000000])
        #self.options = helper.dummyOptions()
        #self.values = helper.dummyValues()
        self.abs_tol=1e-11
        self.rel_tol=1e-11
        pass

    
    def test_ecdfo_func(self):
        """
          Test with problem 5, results compared with matlab
        """
        set_prob(5)
        
        msg,f,ci,ce = ecdfo_func_(self.x)
        
        correctmsg = 0
        correctf =0.053985698962084
        correctci = matlabarray([])
        correctce = matlabarray([  -0.000822750000001, 0.000238240000000, 0.001195859492999]).T
        
        self.assertEqual(correctmsg, msg)
        self.assertAlmostEqual(correctf, f, 7)
        self.assertAlmostEqual(correctci, ci, 7)
        #print "abs", (abs(correctce - ce) < 1e-7).all()
        #print "ce", ce
        #print "correctce", correctce
        self.assertTrue(compare_matlabarray(correctce, ce, self.abs_tol, self.rel_tol))

if __name__ == '__main__':
    unittest.main()