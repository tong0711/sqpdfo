# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 13:25:23 2014

@author: jaco_da
"""

import unittest
from bcdfo_solve_TR_MS_bc import *
import numpy as np
#import helper

class Test_bcdfo_solve_TR_MS_bc(unittest.TestCase):

	def setUp(self):
		#self.options = helper.dummyOptions()
		#self.values = helper.dummyValues()

		pass

	def test_bcdfo_solve_TR_MS_bc(self):
		arg1 = np.array([[2,3]])
		print "arg1", arg1
		arg2 = np.array([[4, 6], [6, 5]])
		print "arg2", arg2
		arg3 = np.array([[-10, -10]])
		print "arg3", arg3
		arg4 = np.array([[10,10]])
		print "arg4", arg4
		
		print "Returns:\n", bcdfo_solve_TR_MS_bc( arg1, arg2, arg3, arg4, 1.0, 0.001, 1 )
#  should give
#    0.5153
#   -0.8575

if __name__ == '__main__':
	unittest.main()