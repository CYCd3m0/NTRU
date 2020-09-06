#!/usr/bin/env python3

from itertools import zip_longest

class Polynomial():

    def __init__(self, coeff, N):
        self._coeff = strip(coeff, 0)
        self._N = N
        
    def __add__(self, other):
        new_coeff = [sum(x) for x in zip_longest(self._coeff, other._coeff, fillvalue=0)]
        return Polynomial(new_coeff, self._N)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        """ Convolution product of truncated polynomial ring """
        if self.isZero() or other.isZero():
            return Polynomial([0], N)
        
        tmp_coeff = [0 for _ in range(self._N*2 - 1)]
        for power1, coeff1 in enumerate(self._coeff):
            for power2, coeff2 in enumerate(other._coeff):
                tmp_coeff[power1+power2] += coeff1 * coeff2

        new_coeff = [sum(x) for x in zip_longest(tmp_coeff[:self._N], tmp_coeff[self._N:], fillvalue=0)]
        return Polynomial(new_coeff, self._N)

    def __mod__(self, m):
        """ Reducing a polynomial's coeff mod m, also does center-lifting """
        new_coeff = list(map(lambda x: x%m if x%m <= m//2 else x%m - m, self._coeff))
        return Polynomial(new_coeff, self._N)

    def __str__(self):
        return ' '.join([str(c) for c in self._coeff])
    
    def __len__(self):
        return len(self._coeff)

    def __iter__(self):
        return iter(self._coeff)

    def __neg__(self):
        return Polynomial([-c for c in self._coeff], self._N)
    
    def __eq__(self, other):
        return self.deg() == other.deg() and all([x==y for (x,y) in zip(self._coeff, other._coeff)])

    def __ne__(self, other):
        return self.deg() != other.deg() or not(all([x==y for (x,y) in zip(self._coeff, other._coeff)]))

    def deg(self):
        return len(self) - 1
    
    def isZero(self):
        return self._coeff == [0]
    
    def scale(self, m):
        """ Scalar multiplication of polynomial by int m """
        new_coeff = [c*m for c in self._coeff]
        return Polynomial(new_coeff, self._N)
    
def strip(L, e=0):
    """ Strip all copies of e from end of list L """
    if len(L) == 0:
        return L

    last_index = len(L) - 1
    while last_index >= 0 and L[last_index] == e:
        last_index = last_index - 1
    return L[:last_index+1]



""" Functions for polynomial """

def inverse_2(a, N):
    """ Almost Inverse Algorithm mod 2 """
    k = 0
    f = a
    g = RingPoly(N)
    b = Polynomial([1], N)
    c = Polynomial([0], N)
    
    while True:
        while f._coeff[0] == 0:
            f = Polynomial(list(f)[1:], N)
            c = Polynomial([0] + list(c), N)
            k += 1
            
        if f._coeff == [1]:
            return b * Xnk(N, k)

        if f.deg() < g.deg():
            f,g = g,f
            b,c = c,b

        f = (f+g) % 2
        b = (b+c) % 2
        
def inverse_2_power(a, N, r):
    """ Almost Inverse Algorithm mod 2^r """
    b = inverse_2(a, N)
    q = 2
    while q < 2**r:
        q = q**2
        b = (b * (Polynomial([2], N) - (a*b))) % q
    return b

def inverse_3(a, N):
    """ Almost Inverse Algorithm mod 3 """
    k = 0
    f = a
    g = RingPoly(N)
    b = Polynomial([1], N)
    c = Polynomial([0], N)

    while True:
        while f._coeff[0] == 0:
            f = Polynomial(list(f)[1:], N)
            c = Polynomial([0] + list(c), N)
            k+=1
        
        if f._coeff == [1]:
            return b * Xnk(N,k)
        elif f._coeff == [-1]:
            return -b * Xnk(N,k)

        if f.deg() < g.deg():
            f,g = g,f
            b,c = c,b

        if f._coeff[0] == g._coeff[0]:
            f = (f-g) % 3
            b = (b-c) % 3
        else:
            f = (f+g) % 3
            b = (b+c) % 3

def Xnk(N, k):
    """ Generate X^(N-k) polynomial """
    xnk = [0 for _ in range(N+1)]
    xnk[N-k-1] = 1
    return Polynomial(xnk, N)

def RingPoly(N):
    """ Generate X^(N-1) polynomial """
    rp_coeff = [0 for _ in range(N+1)]
    rp_coeff[0] = -1
    rp_coeff[-1] = 1
    return Polynomial(rp_coeff, N)
