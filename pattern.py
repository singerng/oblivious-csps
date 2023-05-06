"""
Clause bias patterns for Max-kAND.

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

import scipy as sp

class Pattern():
    """
    Class to encode 'bias pattern'. This is an object which can be associated
    to any clause in a Max-kAND instance, and represents the behavior of oblivious
    algorithms on that clause.

    c is a vector of length 2*(2*l+1) and encodes (c^+, c^-). Entries of the
    patern can be accessed as pattern[sgn,i] where sgn in {-1,+1} and i in
    {-l,...,+l}.
    """
    def __init__(self, k, l, c):
        self.k = k
        self.l = l
        self.c = c
        self.L = 2*l+1
        assert len(c)==2*self.L

    def __hash__(self):
        return hash(self.c)

    def __repr__(self):
        return repr(self.c)

    def __str__(self):
        return str(self.c)

    def is_positive(self):
        """
        Is a clause with this pattern all positive literals?
        """
        for i in range(-self.l, self.l+1):
            if self[-1,i]:
                return False
        return True

    def __getitem__(self, key):
        """
        Access an entry of this pattern.
        """
        sgn, idx = key
        assert sgn == +1 or sgn == -1
        assert -self.l <= idx <= self.l
        return self.c[idx+self.l+self.L*(1-sgn)//2]

    def prob(self, p):
        """
        Calculate the probability a clause with this pattern is satisfied
        by an oblivious algorithm with rounding vector p.
        """
        result = (1/2)**(self[-1,0]+self[+1,0])
        for i in range(1,self.l+1):
            result *= p[i-1]**(self[+1,+i]+self[-1,-i])
            if self[-1,+i] or self[+1,-i]:
                result *= (1-p[i-1])**(self[-1,+i]+self[+1,-i])
        return result

# based loosely on https://stackoverflow.com/questions/10035752/elegant-python-code-for-integer-partitioning
def partition_generator(k, L):
    if L==1:
        yield (k,)
    else:
        for i in range(k+1):
            for c in partition_generator(k-i,L-1):
                yield (i,) + c

def enum_patterns(k, l):
    """
    Enumerate all patterns for oblivious algorithms for Max-kAND, with
    L=2*l+1 bias classes.
    """
    L = 2*l+1
    patterns = [Pattern(k, l, c) for c in partition_generator(k, 2*L)]
    assert len(patterns) == sp.special.binom(k+2*L-1,2*L-1)
    return patterns