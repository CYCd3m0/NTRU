#!/usr/bin/env python3

from os import urandom
from random import SystemRandom
from Polynomial import Polynomial
r = SystemRandom(urandom(256))

class Parameters():

    def __init__(self, N, p, q, df, dg, dr):
        """Security parameters for NTRU"""
        self._N = N
        self._p = p
        self._q = q
        self._df = df
        self._dg = dg
        self._dr = dr

    def generate_poly_f(self):
        """ Generate private key f """
        f_poly = [0] * self._N
        ones = r.sample(range(0, self._N), k = 2*self._df - 1)

        for i in ones[:self._df]:
            f_poly[i] = 1

        for i in ones[self._df:]:
            f_poly[i] = -1

        return Polynomial(f_poly, self._N)

    def generate_poly_g(self):
        """ Generate private key g """
        g_poly = [0] * self._N
        ones = r.sample(range(0, self._N), k = 2*self._dg)

        for i in ones[:self._dg]:
            g_poly[i] = 1

        for i in ones[self._dg:]:
            g_poly[i] = -1

        return Polynomial(g_poly, self._N)

    def generate_poly_r(self):
        """ Generate a random r for security parameters """
        r_poly = [0] * self._N
        ones = r.sample(range(0, self._N), k = 2*self._dr)

        for i in ones[:self._dr]:
            r_poly[i] = 1

        for i in ones[self._dr:]:
            r_poly[i] = -1
        
        return Polynomial(r_poly, self._N)
    
    def get_N(self):
        return self._N

    def get_p(self):
        return self._p

    def get_q(self):
        return self._q

    def get_df(self):
        return self._df + 1, self._df

    def get_dg(self):
        return self._dg, self._dg

    def get_dr(self):
        return self._dr, self._dr

    def __str__(self):
        return str(self._N) + "," + str(self._p) + "," + str(self._q) + "," + str(self._df) + "," + str(self._dg) + "," + str(self._dr)
        