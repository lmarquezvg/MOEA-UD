"""
WFG3_MINUS test problem.

S. Huband, L. Barone, L. While, and P. Hingston, "A Scalable Multi-objective 
Test Problem Toolkit," in Evolutionary Multi-Criterion Optimization, 
pp. 280-295, 2005.

H. Ishibuchi, Y. Setoguchi, H. Masuda, and Y. Nojima, "Performance of 
Decomposition-Based Many-Objective Algorithms Strongly Depends on Pareto Front 
Shapes," in IEEE Transactions on Evolutionary Computation, vol. 21, no. 2, 
pp. 169-190, 2017.

Y. Tian, R. Cheng, X. Zhang, and Y. Jin, "PlatEMO: A MATLAB platform for 
evolutionary multi-objective optimization," in IEEE Computational Intelligence 
Magazine, vol. 12, no. 4, pp. 73-87, 2017.
"""

import numpy as np

def parameters(m):
    """Returns number of decision variables, lower bounds, and upper bounds"""
    k = m-1
    l = 24-(m-1)
    if not l % 2 == 0:
        l -= 1
    n = k+l
    lb = np.zeros(n)
    ub = np.arange(2.0, 2*n+1, 2)
    return n, lb, ub

def evaluate(P, m):
    """Evaluates a population for the WFG3_MINUS test problem"""
    N, n = np.shape(P)
    k = m-1
    D = 1
    A = np.hstack((np.ones(1), np.zeros(m-2)))
    S = np.arange(2.0, 2*m+1, 2)
    
    z01 = P/np.tile(np.arange(2.0, 2*n+1, 2), (N, 1))
    
    t1 = np.zeros((N, n))
    t1[:,:k] = z01[:,:k]
    t1[:,k:] = s_linear(z01[:,k:], 0.35)
    
    t2 = np.zeros((N, k+(n-k)//2))
    t2[:,:k] = t1[:,:k]
    # Same as:
    # for i in range(k, k+(n-k)//2):
    #     t2[:,i] = r_nonsep(t1[:,k+2*(i+1-k)-2:k+2*(i+1-k)], 2)
    t2[:,k:] = (t1[:,k::2]+t1[:,k+1::2]+2*np.abs(t1[:,k::2]-t1[:,k+1::2]))/3
    # --------
    
    t3 = np.zeros((N, m))
    for i in range(0, m-1):
        t3[:,i] = r_sum(t2[:,i*k//(m-1):(i+1)*k//(m-1)], np.ones(k//(m-1)))
    t3[:,m-1] = r_sum(t2[:,k:], np.ones((n-k)//2))
    
    x = np.zeros((N, m))
    for i in range(0, m-1):
        x[:,i] = np.maximum(t3[:,m-1], A[i])*(t3[:,i]-0.5)+0.5
    x[:,m-1] = t3[:,m-1]
    
    h = linear(x)
    
    return -(np.tile(D*x[:,m-1][:,np.newaxis], (1, m))+np.tile(S, (N, 1))*h)

def s_linear(y, A):
    """Transformation function. Shift: Linear"""
    out = np.abs(y-A)/np.abs(np.floor(A-y)+A)
    return out

def r_nonsep(y, A):
    """Transformation function. Reduction: Non-separable"""
    N, m = np.shape(y)
    sum1 = np.zeros(N)
    for j in range(0, m):
        sum2 = np.zeros(N)
        for k in range(0, A-1):
            sum2 += np.abs(y[:,j]-y[:,(1+j+k)%m])
        sum1 += y[:,j]+sum2
    out = sum1/(m/A)/np.ceil(A/2)/(1+2*A-2*np.ceil(A/2))
    return out

def r_sum(y, w):
    """Transformation function. Reduction: Weighted Sum"""
    out = np.sum(y*np.tile(w, (len(y), 1)), axis=1)/np.sum(w)
    return out

def linear(x):
    """Shape function. Linear"""
    N = len(x)
    out = np.fliplr(np.cumprod(np.hstack((np.ones((N, 1)), x[:,:-1])), axis=1))*np.hstack((np.ones((N, 1)), 1-x[:,-2::-1]))
    return out
