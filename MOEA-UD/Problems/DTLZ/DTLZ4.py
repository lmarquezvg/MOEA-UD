"""
DTLZ4 test problem.

K. Deb, L. Thiele, M. Laumanns, and E. Zitzler, "Scalable Test Problems for 
Evolutionary Multiobjective Optimization," in Evolutionary Multiobjective 
Optimization. Theoretical Advances and Applications, pp. 105-145, 2005.

Y. Tian, R. Cheng, X. Zhang, and Y. Jin, "PlatEMO: A MATLAB platform for 
evolutionary multi-objective optimization," in IEEE Computational Intelligence 
Magazine, vol. 12, no. 4, pp. 73-87, 2017.
"""

import numpy as np

def parameters(m):
    """Returns number of decision variables, lower bounds, and upper bounds"""
    k = 10
    n = m-1+k
    lb = np.zeros(n)
    ub = np.ones(n)
    return n, lb, ub

def evaluate(P, m):
    """Evaluates a population for the DTLZ4 test problem"""
    N, n = np.shape(P)
    g = np.sum((P[:,m-1:]-0.5)**2, axis=1, keepdims=True)
    theta = P[:,:m-1]**100
    return np.tile(1+g, (1, m))*np.fliplr(np.cumprod(np.hstack((np.ones((N, 1)), np.cos(theta*np.pi/2))), axis=1))*np.hstack((np.ones((N, 1)), np.sin(theta[:,::-1]*np.pi/2)))
