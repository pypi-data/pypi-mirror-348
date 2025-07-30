import sympy as sp
import unittest
from IntegralElimination import *

class TestIntegralElimination(unittest.TestCase):
    def test_15(self):
        x = sp.Function('x')
        y = sp.Function('y')
        t = sp.Symbol("t")
        theta = sp.Symbol("theta") 

        A = IntegralAlgebra(order=[x(t),y(t)],
                            parameters=[theta])
        
        #is lm(P) is a monomial (not integral)
        P = IntegralPolynomial(IM(x(t))-IM(y(t)))
        M = IM(x(t)**2, y(t),x(t)*y(t))
        R = A.reduction_M_by_P_reduced_power(M,P) 
        expected = None
        verify = expected == R
        self.assertTrue(verify) 

        # other test
        P = IntegralPolynomial(IM(1,x(t)*y(t))-IM(y(t)))   
        M = IM(x(t)**2, x(t)*y(t)**2)
        R = A.reduction_M_by_P_reduced_power(M,P).get_sympy_repr()
        expected = IM(x(t)**2*y(t)**2)/2
        verify = sp.simplify(expected - R) == 0 
        self.assertTrue(verify)

        # other test
        P = IntegralPolynomial(IM(1,x(t)*y(t),y(t))-IM(y(t)))   
        M = IM(x(t)**2, x(t)*y(t)**2)
        R = A.reduction_M_by_P_reduced_power(M,P) 
        expected = None
        verify = expected == R
        self.assertTrue(verify)

if __name__ == '__main__':
    unittest.main()