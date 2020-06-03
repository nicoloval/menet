import sys
sys.path.append('../')
import Directed_graph_Class as sample
import numpy as np
import unittest  # test tool


class MyTest(unittest.TestCase):


    def setUp(self):
        pass


    def test_loglikelihood_dcm(self):
        """
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        """
        n, seed = (3, 42)
        a = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'quasinewton')
        x0 = np.concatenate((g.r_x, g.r_y))

	# call loglikelihood function 
        f_sample = -g.stop_fun(x0)
        f_correct = 8*np.log(1/2) - 6*np.log(5/4)
        # debug
        # print(x0)
        # print(f_sample)
        # print(f_correct)

        # test result
        self.assertTrue(round(f_sample, 3) == round(f_correct, 3))


    def test_loglikelihood_dcm_notrd(self):
        n, seed = (3, 42)
        a = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        args = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_sample = sample.loglikelihood_dcm_notrd(x, args )
        f_correct = 8*np.log(1/2) - 6*np.log(5/4)
        # debug
        # print(args)
        # print(f_sample)
        # print(f_correct)

        self.assertTrue(round(f_sample, 3) == round(f_correct, 3))


    def test_loglikelihood_prime_dcm(self):
        """
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        """
        n, seed = (3, 42)
        a = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        # rd
        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'quasinewton')
        x0 = np.concatenate((g.r_x, g.r_y))

        f_sample = -g.fun(x0)
        g._set_solved_problem(f_sample)
        f_full = np.concatenate((g.x, g.y))
        # f_correct = np.array([3.2, 1.2, 3.2, 1.2])

        # not rd
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        args_notrd = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_notrd = sample.loglikelihood_prime_dcm_notrd(x, args_notrd)
 
        # debug
        # print(a)
        # print(x0, x)
        # print('f_sample, f_correct', f_full, f_notrd)

        # test result
        self.assertTrue(np.allclose(f_full, f_notrd))


    def test_loglikelihood_prime_dcm_notrd(self):
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        args = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_sample = sample.loglikelihood_prime_dcm_notrd(x, args)
        f_correct = np.array([-4/5+4,4-4/5, 2-4/5, -4/5+2, -4/5+4, -4/5+4])  
        # debug
        # print(par)
        # print(f_sample)
        # print(f_correct)

        # test result
        self.assertTrue(np.allclose(f_sample, f_correct))


    def test_loglikelihood_prime_dcm_0(self):
        """
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        """
        n, seed = (3, 42)
        a = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        # rd
        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'quasinewton')
        x0 = np.concatenate((g.r_x, g.r_y))

        f_sample = -g.fun_jac(x0)
        g._set_solved_problem(f_sample)
        f_full = np.concatenate((g.x, g.y))
        # f_correct = np.array([3.2, 1.2, 3.2, 1.2])

        # not rd
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        args_notrd = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_notrd = sample.loglikelihood_hessian_diag_dcm_notrd(x, args_notrd)
 
        # debug
        # print(a)
        # print(x0, x)
        # print('f_sample, f_correct', f_full, f_notrd)

        # test result
        self.assertTrue(np.allclose(f_full, f_notrd))



    def test_loglikelihood_hessian_diag_dcm(self):
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        c = np.array([1,1,1])
        args = (k_out, k_in, nz_ind_out, nz_ind_in, c)
        args_notrd = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_sample = sample.loglikelihood_hessian_diag_dcm(x, args)
        f_correct = sample.loglikelihood_hessian_diag_dcm_notrd(x, args_notrd)
        # debug
        # print(par)
        # print(f_sample)
        # print(f_correct)

        # test result
        self.assertTrue(np.allclose(f_sample, f_correct))


    def test_loglikelihood_hessian_diag_dcm_notrd(self):
        a = np.array([[0, 0, 1],
                      [1, 0, 1],
                      [0, 1, 0]])

        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        args = (k_out, k_in, nz_ind_out, nz_ind_in)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_sample = sample.loglikelihood_hessian_diag_dcm_notrd(x, args)
        f_correct = np.array([8/25-4, 8/25-8, 8/25-4,8/25-4, 8/25-4, 8/25-8])  
        # debug
        # print(par)
        # print(f_sample)
        # print(f_correct)

        # test result
        self.assertTrue(np.allclose(f_sample, f_correct))


    def test_iterative_dcm(self):
        """
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        """
        n, seed = (3, 42)
        a = sample.random_binary_matrix_generator_nozeros(n, sym=False, seed=seed)

        # rd
        g = sample.DirectedGraph(a)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'fixed-point')
        x0 = 0.5*np.ones(4) 

        f_sample = -g.fun(x0)
        g._set_solved_problem(f_sample)
        f_full = np.concatenate((g.x, g.y))
        f_correct = np.array([2.5, 1.25, 1.25, 2.5, 1.25, 1.25])

        # debug
        # print(a)
        # print(x0, x)

        # test result
        self.assertTrue(np.allclose(f_full, f_correct))


    def test_iterative_dcm_1(self):
        degseq = np.array([0, 1, 2, 1, 2, 2, 2, 0, 2, 0])

        # rd
        g = sample.DirectedGraph(degree_sequence = degseq)
        g.degree_reduction()
        g.initial_guess='uniform'
        g._initialize_problem('dcm', 'fixed-point')
        x0 = np.ones(6) 
        # x0[x0 == 0] = 0

        f_sample = -g.fun(x0)
        # g._set_solved_problem(f_sample)
        # f_full = np.concatenate((g.x, g.y))
        f_correct = np.array([0, 0.5, 1, 1, 1, 0])

        # debug
        # print(g.args)
        # print(f_sample)
        # print(f_correct)

        # test result
        self.assertTrue(np.allclose(f_sample, f_correct))


    def test_loglikelihood_hessian_dcm_vs_diag(self):
        a = np.array([[0, 1, 1],
                      [1, 0, 1],
                      [0, 1, 0]])
        k_out = np.sum(a > 0, 1) 
        k_in = np.sum(a > 0, 0)
        nz_ind_out = np.nonzero(k_out)[0]
        nz_ind_in = np.nonzero(k_in)[0]
        c = np.array([1,1,1])
        args = (k_out, k_in, nz_ind_out, nz_ind_in, c)
        x = 0.5*np.ones(len(k_out)+len(k_in))
	# call loglikelihood function 
        f_diag = sample.loglikelihood_hessian_diag_dcm(x, args)
        f_full = sample.loglikelihood_hessian_dcm(x, args)
        f_df = np.diag(f_full)
        # debug
        # print(f_diag, f_full, f_df)
        

        # test result
        self.assertTrue(np.allclose(f_diag, f_df))


if __name__ == '__main__':
    unittest.main()
