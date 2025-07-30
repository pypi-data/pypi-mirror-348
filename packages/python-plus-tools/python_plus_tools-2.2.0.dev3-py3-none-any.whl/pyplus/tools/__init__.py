import decorators
from img_fit import latex2text as latex

from . import (
    colors,
    dec, 
    database_convert,
    formula,
    # password,
    permission,
    stack,
    tag,
    update,
    web,
    variables,
    pycppio,
)
from argparse import Namespace

# from . import () # deprecated moudle


def wait(operator: bool):
    """
    Please use it in subprocess.
    """
    while not operator:
        pass

def geohash(latitude, longitude, datedow):
    import hashlib

    """Compute geohash() using the Munroe algorithm.

    >>> geohash(37.421542, -122.085589, b'2005-05-26-10458.68')
    37.857713 -122.544543

    """
    # https://xkcd.com/426/
    h = hashlib.md5(datedow, usedforsecurity=False).hexdigest()
    p, q = [("%f" % float.fromhex("0." + x)) for x in (h[:16], h[16:32])]
    print("%d%s %d%s" % (latitude, p[1:], longitude, q[1:]))

class List(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def average(self):
        return sum(self) / len(self)
    
    def median(self):
        n = len(self)
        s = sorted(self)
        return (s[n//2] + s[~n//2]) / 2 if n % 2 else s[n//2]
    
    def mode(self):
        return max(set(self), key=self.count)
    
    def variance(self):
        n = len(self)
        mean = sum(self) / n
        return sum((x - mean) ** 2 for x in self) / n
    
    def std(self):
        return (self.variance()) ** 0.5
    
    def min(self):
        return min(self)
    
    def max(self):
        return max(self)
    
    def sum(self):
        return sum(self)
    
    def unique(self):
        return list(set(self))
