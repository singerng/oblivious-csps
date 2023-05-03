"""
Clause bias patterns for Max-kAND

By Noah Singer <ngsinger@cs.cmu.edu>, May 2023
"""

import scipy as sp

class Pattern():
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
        for i in range(self.L):
            if self.c[i]:
                return False
        return True

    def __getitem__(self, key):
        sgn, idx = key
        assert sgn == +1 or sgn == -1
        assert -self.l <= idx <= self.l
        return self.c[idx+self.l+self.L*(sgn+1)//2]

    def prob(self, p):
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
    L = 2*l+1
    patterns = [Pattern(k, l, c) for c in partition_generator(k, 2*L)]
    assert len(patterns) == sp.special.binom(k+2*L-1,2*L-1)
    return patterns