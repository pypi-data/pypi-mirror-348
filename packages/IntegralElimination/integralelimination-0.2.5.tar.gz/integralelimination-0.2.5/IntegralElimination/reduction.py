from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IntegralAlgebra import IntegralAlgebra

import sympy as sp 
from ordered_set import OrderedSet

from .IntegralMonomial import IM
from .IntegralPolynomial import IntegralPolynomial 
from .utils import (
    is_int, 
)

from .check_conditions_LM import (
    check_condition_LM_half_reduced_product,
)


def reduction_M_by_P_simple_case(A: IntegralAlgebra, 
                                 M: IM, 
                                 P: IntegralPolynomial) -> IntegralPolynomial:
    """
    Consider an integral monomial M
    and a nonzero integral polynomiaml P.
	
	If there exists an integral monomial 
    N such that lm{lm{P} · N}=M,
	then introduce
	R =  M-(1/l)P · N
	where l is the leading coefficient of P · N.
    """
    assert not P.is_zero() 

    LM_P,LC_P = A.LM_LC(P)
    assert LC_P == 1, "LC(P) should be normalized"

    N = A.monomial_division(M,LM_P)
    if N == None:
        return None  
    
    PN = A.polynomials_product(P,IntegralPolynomial(N))
    PN = A.normalize_LC_of_P(PN)[0]
    
    assert M == A.LM_LC(PN)[0]

    R = A.polynomials_subtraction(
            IntegralPolynomial(M),
            PN
        ) 
    if not R.is_zero():
        LM_R = A.LM_LC(R)[0]
        assert A.IMO_le(LM_R,M)
    return R
 

def reduction_M_by_P_reduced_power(A: IntegralAlgebra, 
                                   M: IM, 
                                   P: IntegralPolynomial
                                   ) -> IntegralPolynomial:
    """
    Consider an integral monomial M and an integral polynomial P
    with P_I != 0, P_N != 0, and lm{P} = lm{P_I}$.
    
    Assume there exists a positive integer n
    and an integral monomial N such that
    - lm{P_I}[1] lm{lm{P_N}[0]}^{n-1} = M[1],
    - lm{ (P_I[2+]) · (P_N[1+])^{n-1} · N } = M[2+],
    - N[0] = 1.

    If the condition
    of check_condition_LM_half_reduced_product
    (this function checks the condition)
    holds for P^{\reduced_power{n}} half-reduced-prod N,  
    then introduce
	R = M - (1/l) M[0](P^{reduced_power{n}} half-reduced-prod N )
	where
	l is the leading coefficient 
    of M[0](P^{reduced_power{n}} half-reduced-prod N ).
    """
    assert not P.is_zero() 
    LM_P,LC_P = A.LM_LC(P)
    assert LC_P == 1, "LC(P) should be normalized"
    if M.get_nb_int() == 0 : # |M| >= 1
        return None
    P_I = P.get_P_I()
    if P_I.is_zero(): return None 
    LM_P_I,LC_P_I = A.LM_LC(P_I)
    if LM_P_I != LM_P : # we want lm(P) = lm(P_I)
        return None
    P_N = P.get_P_N()
    if P_N.is_zero(): return None 
    LM_P_N,LC_P_N = A.LM_LC(P_N)
    M_1 = M.cut("1").get_content()[0]
    LM_P_N_0 = LM_P_N.cut("0").get_content()[0]
    LM_P_I_1 = LM_P_I.cut("1").get_content()[0]

    # we try to find n such that (lm(PI)[1]*lm(PN)[0]**(n-1))/M[1] = 1
    n = sp.Symbol("n_pow")
    pow_dict = ((LM_P_I_1*LM_P_N_0**(n-1))/M_1).as_powers_dict()
    if len(pow_dict) > 1: 
        #for example :
        # expr = ((x(t)*a(t))**n*y(t))/(x(t)**2*y(t))
        # expr.as_powers_dict()
        # {a(t)x(t):n, x(t): -2}
        return None 
    sp_solved = sp.solve(list(pow_dict.values())[0])
    if len(sp_solved)==0: return None
    solved_n = sp_solved[0] 
    if not(is_int(solved_n) and solved_n > 0):
        return None
    #we then have to verify the condition:
    #lm( (lm(P_I)[2+]) cdot (lm(P_N)[1+])**(n-1)) = M[2+]
    LM_P_I_i2plus = IntegralPolynomial(LM_P_I.cut("i2+"))
    LM_P_N_i1plus = IntegralPolynomial(LM_P_N.cut("i1+"))
    LM_P_N_i1plus_pow = A.polynomial_power(LM_P_N_i1plus,solved_n-1)
    pol = A.polynomials_product(LM_P_I_i2plus, LM_P_N_i1plus_pow)
    
    Mi2_plus = M.cut("i2+")
    B_P, c_B_P = A.LM_LC(pol)
    N = A.monomial_division(Mi2_plus, B_P)
    if N is None or N.get_content()[0] != 1:
        return None
    
    # we compute the reduced power
    P_reduced_pow_n = A.reduced_power(P,solved_n)
    # we verify the condition on N
    if not check_condition_LM_half_reduced_product(A, P_reduced_pow_n, N):
        return None
    # we can now compute R
    P_reduced_pow_n_red_prod_N = A.half_reduced_product(P_reduced_pow_n, N)
    
    M0 = IntegralPolynomial(M.cut("0"))
    M0_P_pow_n = A.polynomials_product(P_reduced_pow_n_red_prod_N, M0)
    l_P = LC_P_N
    temp = A.product_P_Coeff(M0_P_pow_n, -1/(solved_n*l_P**(solved_n-1)))
    assert M == A.LM_LC(temp)[0]
    R = A.polynomials_add(IntegralPolynomial(M), temp)
    if not R.is_zero():
        LM_R = A.LM_LC(R)[0]
        assert A.IMO_le(LM_R,M)
    return R 

def reduction_M_by_P(A: IntegralAlgebra, 
                     M: IM, 
                     P: IntegralPolynomial
                    ) -> IntegralPolynomial:
    """
    Lemma 14
    """
    assert not P.is_zero() 
    e = M.get_nb_int() 
    for i in reversed(range(e+1)): 
        prefix = M.get_prefix(i)
        suffix = M.get_suffix(i)   
        R = A.reduction_M_by_P_simple_case(suffix,P)  
        if R is not None:
            R = A.add_prefix_to_polynomial(prefix,R) 
            if not R.is_zero():
                LM_R = A.LM_LC(R)[0]
                assert A.IMO_le(LM_R,M)
            return R
        R = A.reduction_M_by_P_reduced_power(suffix,P) 
        if R is not None:
            R = A.add_prefix_to_polynomial(prefix,R)
            if not R.is_zero():
                LM_R = A.LM_LC(R)[0]
                assert A.IMO_le(LM_R,M)
            return R 

def reduce(IA:IntegralAlgebra, 
           Q:IntegralPolynomial, 
           T:OrderedSet[IntegralPolynomial],
           has_been_reduced=False) -> IntegralPolynomial:
    """
    reduce Q by the set of integral polynomials T
    """ 
    if Q.is_zero(): 
        return IntegralPolynomial(0), False
    A = Q 

    LM_A,LC_A = IA.LM_LC(A)
    #test if LM can be reduced by some P of T
    if IA.storage["P_red_to_zero"].get(A):
        return IntegralPolynomial(0), True
    for P in T: 
        P_norm, _ = IA.normalize_LC_of_P(P)  
        R = reduction_M_by_P(IA, LM_A, P_norm)  
        if R is not None:  
            #A=lm(A)+B, i.e B is the tail, so we can just delete the leading 
            # monomial of A to obtain B
            B = A.get_content_as_dict()
            del B[LM_A]

            alphaR = IA.product_P_Coeff(R, LC_A, return_dict=True)
            A = IA.polynomials_add(B, alphaR, return_dict=False)   
            if A.is_zero():
                return A, True 
            return reduce(IA, A, T, has_been_reduced=True) 
    if A.is_zero():
        IA.storage["P_red_to_zero"][A] = IntegralPolynomial(0)
    return A, has_been_reduced

def __auto_reduce(IA:IntegralAlgebra, 
                T:OrderedSet[IntegralPolynomial]) -> tuple:
    T_reduced =  OrderedSet([])
    T_done = OrderedSet([]) 
    one_P_has_been_reduced = False
    for P in T:
        T_done.add(P) 
        T_copy = T - T_done | T_reduced 
        P_reduced, has_been_reduced = IA.reduce(P,T_copy)
        one_P_has_been_reduced = one_P_has_been_reduced or has_been_reduced 
        if not P_reduced.is_zero(): 
            T_reduced.add(P_reduced) 
        
    return T_reduced, one_P_has_been_reduced

def auto_reduce(IA:IntegralAlgebra, 
                T:OrderedSet[IntegralPolynomial]
            ) -> OrderedSet[IntegralPolynomial]:
    T_reduced = T
    has_been_reduced = True 
    while has_been_reduced:  
        T_temp, has_been_reduced = __auto_reduce(IA,T_reduced) 
        T_reduced = T_temp  
    return T_reduced