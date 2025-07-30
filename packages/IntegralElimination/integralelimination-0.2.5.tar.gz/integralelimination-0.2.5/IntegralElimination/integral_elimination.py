from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .IntegralAlgebra import IntegralAlgebra

from ordered_set import OrderedSet

from .IntegralPolynomial import IntegralPolynomial 


def integral_elimination(IA: IntegralAlgebra,
                        F: OrderedSet[IntegralPolynomial],
                        disable_exp: bool = False,
                        disable_log: bool = True,
                        disable_critical_pairs: bool = False,
                        nb_iter = None) -> tuple:

    T = OrderedSet([elem for elem in F])
    E = OrderedSet()
    L = OrderedSet()
    X_prime = IA.order
    finished = False 
    
    i = 1
    while not finished:
        T_prime = IA.auto_reduce(T)
        E_prime = E
        L_prime = L
        T_E = OrderedSet([])
        T_L = OrderedSet([])
        if not disable_exp:
            T_E, E_prime = IA.update_exp(T_prime, E)
        if not disable_log:
            T_L, L_prime = IA.update_log(T_prime, L)
        X_prime = IA.extend_X_with_exp_and_log(E_prime, L_prime)
        IA.update_IMO(X_prime)
        T_prime = T_prime | T_E | T_L # T_prime union T_E union T_L

        if not disable_critical_pairs:
            C = IA.critical_pairs(T_prime)
            for Q in C:
                # _ is a boolean = has_been_reduced
                Q_red, _ = IA.reduce(Q,T_prime) 
                if not Q_red.is_zero():
                    T_prime.add(Q_red)

        E_prime_red = OrderedSet([])
        for ui, vi, Qi in E_prime:
            # _ is a boolean = has_been_reduced
            Qi_red, _ = IA.reduce(Qi, T_prime) 
            E_prime_red.add((ui, vi ,Qi_red))

        L_prime_red = OrderedSet([])
        for li, Qi in L_prime:
            # _ is a boolean = has_been_reduced
            Qi_red, _ = IA.reduce(Qi, T_prime) 
            L_prime_red.add((li ,Qi_red))

        X_prime = IA.extend_X_with_exp_and_log(E_prime_red, L_prime_red)

        IA.update_IMO(X_prime)
        E = E_prime_red 
        L = L_prime_red 
        
        T_equal_T_prime = check_T_equal_T_prime(T, T_prime)
        T = T_prime

        if (i == nb_iter) or T_equal_T_prime:
            finished = True

        i += 1
    return (E, L, T, X_prime)


def check_T_equal_T_prime(T: OrderedSet[IntegralPolynomial],
                          T_prime: OrderedSet[IntegralPolynomial]) -> bool:
    T_sp = OrderedSet([eq.get_sympy_repr() for eq in T])
    T_prime_sp = OrderedSet([eq.get_sympy_repr() for eq in T_prime]) 
    return T_sp == T_prime_sp