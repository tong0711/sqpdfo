# -*- coding: utf-8 -*-
"""
Created on Tue Dec 02 14:54:04 2014

@author: jaco_da
"""

import unittest
from bcdfo_evalL import bcdfo_evalL_
from bcdfo_build_QR_of_Y import bcdfo_build_QR_of_Y_
from runtime import matlabarray, compare_matlabarray
from random import random
#import helper

class Test_bcdfo_evalL(unittest.TestCase):
    """
    #Reminder :
    #This class is a test for evalL which computes the values of the lagrange polynomials l_j(x), such that the output vector values is :
    #[l_1(x), l_2(x), l_3(x),....l_p(x)] where p is the number of points of the interpolant set.
    """ 
    def setUp(self):
        #self.options = helper.dummyOptions()
        #self.values = helper.dummyValues()
           self.abs_tol=1e-15;
           self.rel_tol=1e-15;
           pass


    def test_bcdfo_evalL_1(self):
        """
     We verify here that for x being a point of the interpolant set, we have l_j(x) = 1 if the index j corresponds to the index of x in the interpolant set
    and 0 otherwise
        """
        Y = matlabarray([[ 0, 1, 0, 2, 1, 0],[0, 0, 1, 0, 0.01, 2 ]]) 
        QZ, RZ, xbase, scale = bcdfo_build_QR_of_Y_( Y, 0, 1, 1,1,1e15 )
        
        #Here we choose the first point of the interpolant set
        values = bcdfo_evalL_( QZ, RZ, Y, matlabarray(range(0,6)), matlabarray([[0],[0]]), xbase, 0, scale, 1 )
        correctvalues = matlabarray([ [1],   [0],    [0],    [0], [0],   [0] ])
        
        self.assertTrue(compare_matlabarray(values, correctvalues, self.abs_tol, self.rel_tol))
        

    def test_bcdfo_evalL_2(self):
        """
     We verify here that for x being a point of the interpolant set, we have l_j(x) = 1 if the index j corresponds to the index of x in the interpolant set
    and 0 otherwise
        """
        Y = matlabarray([[ 0, 1, 0, 2, 1, 0],[0, 0, 1, 0, 0.01, 2 ]]) 
        QZ, RZ, xbase, scale = bcdfo_build_QR_of_Y_( Y, 0, 1, 1,1,1e15 )
        
        #Here we choose the fifth point of the interpolant set
        values = bcdfo_evalL_( QZ, RZ, Y, matlabarray(range(1,6)), matlabarray([[1],[0.01]]), xbase, 0, scale, 1 )
        correctvalues = matlabarray([ [0.],   [0.],    [0.],    [0.], [1.],   [0.] ])
        
        self.assertTrue(compare_matlabarray(values, correctvalues, self.abs_tol, self.rel_tol))
        

    def test_bcdfo_evalL_3(self):
        """
     We verify here that for x being a point of the interpolant set, we have l_j(x) = 1 if the index j corresponds to the index of x in the interpolant set
    and 0 otherwise
        """
        Y = matlabarray([[ 0, 1, 0, 2, 1, 0],[0, 0, 1, 0, 0.01, 2 ]]) 
        QZ, RZ, xbase, scale = bcdfo_build_QR_of_Y_( Y, 0, 1, 1,1,1e15 )
        
        #Here we choose the fourth point of the interpolant set
        values = bcdfo_evalL_( QZ, RZ, Y, matlabarray([2, 3, 5]), matlabarray([[2],[0]]), xbase, 0, scale, 1 )
        correctvalues = matlabarray([ [0],   [0],    [0],  [1], [0],   [0] ])
        
        self.assertTrue(compare_matlabarray(values, correctvalues, self.abs_tol, self.rel_tol))
        self.assertTrue(compare_matlabarray(xbase, matlabarray([0,0]), self.abs_tol, self.rel_tol))
        self.assertTrue(compare_matlabarray(scale, matlabarray([1,0.5, 0.5, 0.25, 0.25, 0.25]), self.abs_tol, self.rel_tol))

    
    def test_bcdfo_evalL_4(self):
        """
        We verify here that for x random, the sum of the values is equal to 1 when we have a enough point to have a complete basis.
        """
        Y = matlabarray([[ 0, 1, 0, 2, 1, 0],[0, 0, 1, 0, 0.01, 2 ]]) 
        QZ, RZ, xbase, scale = bcdfo_build_QR_of_Y_( Y, 0, 1, 1,1,1e15 )
        
        #Here we choose a random point, and the complete interpolant set
        for i in range(0,50):
            values = bcdfo_evalL_( QZ, RZ, Y, matlabarray(range(0,6)), matlabarray([[(random()-0.5)*100],[(random()-0.5)*100]]), xbase, 0, scale, 1 )
            self.assertAlmostEqual(values.sum(), 1.0,places=9) #NB : random values force us to reduce the precision 

    def test_bcdfo_evalL_5(self):
        """
        More complicated test initally written in the matlab code
        """
        Y = matlabarray([[ 0, 1, 0, 2, 1, 0],[0, 0, 1, 0, 0.01, 2 ]]) 
        QZ, RZ, xbase, scale = bcdfo_build_QR_of_Y_( Y, 0, 1, 1,1,1e15 )
        values = bcdfo_evalL_( QZ, RZ, Y, matlabarray(range(1,6)), matlabarray([[-1],[1]]), xbase, 0, scale, 1 )
        #print "values", values
        correctvalues = matlabarray([ [0],   [97.0000],    [2.9900],    [1.0000], [-100.0000],   [-0.4950] ])
        self.assertTrue(compare_matlabarray(values, correctvalues, self.abs_tol, self.rel_tol))
        

if __name__ == '__main__':
    unittest.main()