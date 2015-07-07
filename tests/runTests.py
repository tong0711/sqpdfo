# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 14:31:47 2014

@author: jaco_da
"""
import unittest
import ecdfo_check_cond_test
import ecdfo_check_convex_test
import blls_test
import sqplab_badsimul_test
import sqplab_bfgs_test
import sqplab_checkoptions_test
import sqplab_options_test
import sqplab_tcg_test
import ecdfo_augmX_evalf_test
import ecdfo_finish_test
import ecdfo_func_test
import ecdfo_iter_printout_test
import ecdfo_init_prob_test
import evalfgh_test
import ecdfo_optimality_test
import sqplab_lsmult_test
import ecdfo_solve_TR_bc_test
import ecdfo_swap_in_Y_test
import ecdfo_find_smallf_test
import ecdfo_computeHessian_test
import ecdfo_prelim_test
import ecdfo_main_test

import bcdfo_evalL_test
import bcdfo_find_new_yj_test
import bcdfo_hessP_test
import bcdfo_include_in_Y_test
import bcdfo_repair_Y_test
import bcdfo_replace_in_Y_test
import bcdfo_solve_TR_MS_test
import bcdfo_build_QR_of_Y_test
import bcdfo_solve_TR_MS_bc_test
import bcdfo_evalZ_test
import bcdfo_poisedness_Y_test
import bcdfo_augment_Y_test
import bcdfo_gradP_test
import bcdfo_evalP_test
import bcdfo_computeP_test
import bcdfo_computeLj_test
import bcdfo_find_new_yj_test
import bcdfo_projgrad_test
import bcdfo_evalZ_test
#import bcdfo_build_QR_of_Y_test
#import bcdfo_solve_TR_MS_bc_test
#import bcdfo_evalZ_test
#import bcdfo_poisedness_Y_test
#import bcdfo_augment_Y_test
#import bcdfo_gradP_test
#import bcdfo_evalP_test

loader = unittest.TestLoader() 

suite = loader.loadTestsFromTestCase(ecdfo_check_convex_test.Test_ecdfo_check_convex)

#ECDFO Tests

suite.addTests(loader.loadTestsFromTestCase(ecdfo_main_test.Test_ecdfo_main))

suite.addTests(loader.loadTestsFromTestCase(ecdfo_check_cond_test.Test_ecdfo_check_cond))
suite.addTests(loader.loadTestsFromTestCase(blls_test.Test_blls))
suite.addTests(loader.loadTestsFromTestCase(sqplab_badsimul_test.Test_sqplab_badsimul))
suite.addTests(loader.loadTestsFromTestCase(sqplab_bfgs_test.Test_sqplab_bfgs))
suite.addTests(loader.loadTestsFromTestCase(sqplab_checkoptions_test.Test_sqplab_checkoptions))
suite.addTests(loader.loadTestsFromTestCase(sqplab_options_test.Test_sqplab_options))
suite.addTests(loader.loadTestsFromTestCase(sqplab_tcg_test.Test_sqplab_tcg))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_augmX_evalf_test.Test_ecdfo_augmX_evalf))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_finish_test.Test_ecdfo_finish))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_func_test.Test_ecdfo_func))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_iter_printout_test.Test_ecdfo_iter_printout))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_init_prob_test.Test_ecdfo_init_prob))
suite.addTests(loader.loadTestsFromTestCase(evalfgh_test.Test_evalfgh))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_optimality_test.Test_ecdfo_optimality))
suite.addTests(loader.loadTestsFromTestCase(sqplab_lsmult_test.Test_sqplab_lsmult))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_solve_TR_bc_test.Test_ecdfo_solve_TR_bc))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_swap_in_Y_test.Test_ecdfo_swap_in_Y))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_find_smallf_test.Test_ecdfo_find_smallf))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_computeHessian_test.Test_ecdfo_computeHessian))
suite.addTests(loader.loadTestsFromTestCase(ecdfo_prelim_test.Test_ecdfo_prelim))


#BCDFO Tests
suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalL_test.Test_bcdfo_evalL))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_find_new_yj_test.Test_bcdfo_find_new_yj))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_hessP_test.Test_bcdfo_hessP))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_include_in_Y_test.Test_bcdfo_include_in_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_repair_Y_test.Test_bcdfo_repair_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_replace_in_Y_test.Test_bcdfo_replace_in_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_solve_TR_MS_test.Test_bcdfo_solve_TR_MS))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_build_QR_of_Y_test.Test_bcdfo_build_QR_of_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_solve_TR_MS_bc_test.Test_bcdfo_solve_TR_MS_bc))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalZ_test.Test_bcdfo_evalZ))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_poisedness_Y_test.Test_bcdfo_poisedness_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_augment_Y_test.Test_bcdfo_augment_Y))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_gradP_test.Test_bcdfo_gradP))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalP_test.Test_bcdfo_evalP))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_computeP_test.Test_bcdfo_computeP))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_computeLj_test.Test_bcdfo_computeLj))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_find_new_yj_test.Test_bcdfo_find_new_yj))
suite.addTests(loader.loadTestsFromTestCase(bcdfo_projgrad_test.Test_bcdfo_projgrad))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalZ_test.Test_bcdfo_evalZ))

#suite.addTests(loader.loadTestsFromTestCase(bcdfo_build_QR_of_Y_test.Test_bcdfo_build_QR_of_Y))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_solve_TR_MS_bc_test.Test_bcdfo_solve_TR_MS_bc))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalZ_test.Test_bcdfo_evalZ))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_poisedness_Y_test.Test_bcdfo_poisedness_Y))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_augment_Y_test.Test_bcdfo_augment_Y))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_gradP_test.Test_bcdfo_gradP))
#suite.addTests(loader.loadTestsFromTestCase(bcdfo_evalP_test.Test_bcdfo_evalP))

unittest.TextTestRunner(verbosity=2).run(suite)