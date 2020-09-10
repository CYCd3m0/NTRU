import os
import sys
sys.path.append('./NTRU')
from Polynomial import *
import NTRUEncrypt

import time
import sympy as sym
from sympy import GF

cipher = NTRUEncrypt.generate_key(NTRUEncrypt.Highest_Security())
f = cipher._f._coeff
N = cipher._P.get_N()


""" almost inverse """
t1 = time.time()
ans1 = inverse_3(Polynomial(f, N), N)._coeff
t2 = time.time()

for i in range(len(ans1)):
    ans1[i] = ans1[i] % 3
print(ans1)
print('almost inverse time :', t2-t1)

print('--------------------------------------------------')

""" extgcd """
def gen_poly(coeffs, N):
    """Create a polynomial in x."""
    x = sym.Symbol('x')
    coeffs = list(coeffs)
    y = 0
    for i in range(N):
        y += (x**i)*coeffs[i]
    y = sym.poly(y)
    return y

f_poly = gen_poly(f, len(f))
x = sym.Symbol('x')

t1 = time.time()
fp = sym.polys.polytools.invert(f_poly, x**N-1, domain=GF(3, symmetric=False))
t2 = time.time()
ans2 = fp.all_coeffs()
ans2.reverse()
print(ans2)
print('exgcd time \t\t\t:', t2-t1)

print(f'\n{ans1 == ans2}')
