import sys
import numpy as np


def em_matrix(em):
    """ Create fn to retrieve discrete emissions stored in matrix
    
    Args:
        em: matrix where rows are states and cols are emission probs of discrete states

    Returns:
        fnc which return emission probability given state and observation
    """
    def em_fn(state, k):
        return em[state][k]
    
    return em_fn

def path(X, Z, tr, em_fn, init_dist):
    """ log-likelihood of a particular path through an HMM

    Args:
        X:          sequence of observations
        Z:     sequence of hidden states
        tr:         transition matrix
        em_fn:      function to get LOG emissions given state and observation 
        init_dist:  iniitial distribution over states

    Returns:
        Y: most likely sequence of states
        V: Viterbi matrix
    """
    tr_log = [[np.log(p) for p in l] for l in tr]

    ll_X = [em_fn(zNEW, x)  + tr_log[zOLD][zNEW] for x, zOLD, zNEW in zip(X[1:], Z[:-1], Z[1:])]
    ll = em_fn(Z[0], X[0]) + np.log(init_dist[Z[0]]) + sum(ll_X)

    return ll

def viterbi(X, tr, em_fn, init_dist):
    """ Returns the Viterbi path for the observations X
        with given transition matrix and emission functions

    Args:
        X:          sequence of observations
        tr:         transition matrix
        em_fn:      function to get LOG emission given state and observation 
        init_dist:  iniitial distribution over states

    Returns:
        Y: most likely sequence of states
        V: Viterbi matrix
    """

    N = len(tr)
    L = len(X)

    V = [np.array([0]*N) for _ in range(L)]
    TB = [np.array([0]*N) for _ in range(L)]
    
    tr_log = [[np.log(p) for p in l] for l in tr]
    a_tr = np.array(tr_log).T  # NOTE: Transpose the matrix so cols match with cols of V

    Vprev = np.array([np.log(pk0) for pk0 in init_dist])

    for i in range(0,L):
        em = np.array([em_fn(k, X[i]) for k in range(N)])
        p_tr = a_tr + Vprev
        TB[i] = np.argmax(p_tr, axis=1)
        V[i] = np.max(p_tr, axis=1) + em

        # for k in range(N):
        #     ## k = new state
        #     ## j_hat = max old state
        #     j_hat = np.argmax([v + tr_log[j][k] for j, v in enumerate(Vprev)])
        #     V[i][k] = Vprev[j_hat] + tr_log[j_hat][k] + em_fn(k, X[i])
        #     TB[i][k] = j_hat

        Vprev = V[i]

    # perform traceback and return the predicted hidden state sequence
    Y = [0 for i in range(L)]
    _, yL = max([ (V[L-1][k], k) for k in range(N)])
    Y[L-1] = yL
    for i in range(L-2,-1,-1):
        Y[i] = TB[i+1][Y[i+1]]

    return Y, V

def forward(X, tr, em_fn, init_dist, method='loop'):
    """  Calculate total probability of observations given model using forward algorithm
    
    Uses probability scaling in order to ensure numerical stability
    Args:
        X:          sequence of observations
        tr:         transition matrix
        em_fn:      function to get emission given state and observation 
        init_dist:  iniitial distribution over states

    Kwargs:
        method:     How to perform the calculations (loop of vector)
                    loop uses for loops
                    vector uses a vectorized (matrix multiplication) approach

    Returns:
        C: list of P(X_i | X_i-1, ..., X_1)
        F: scaled forward probabilities giving P(Z_i | X_i, ..., X_1)

    Notes:
        * P(X_1, ..., X_n) = prod(C)
        * Above is liable to lead to underflow. Use log-likelihood instead:
            * ll(X_1, ..., X_n) = sum(log(C))
    """
    N = len(tr)
    L = len(X)

    # F = [np.array([0]*N) for _ in range(L)]
    F = [[0]*N for _ in range(L)]
    C = [0] * L
    # TB = [np.array([0]*N) for _ in range(L)]
    
    # tr_log = [[np.log(p) for p in l] for l in tr]
    a_tr = np.array(tr).T  # NOTE: Transpose the matrix to match orientation of F

    # Fprev = np.array([np.log(pk0) for pk0 in init_dist])
    # Calculate C[0], F[0]
    # ID = np.array(init_dist)
    # em = np.array([em_fn(k, X[0]) for k in range(N)])
    em = [em_fn(k, X[0]) for k in range(N)]
    pr = [e * p for e, p in zip(em, init_dist)]
    # pr = em * ID
    # F[0] = pr
    C[0] = sum(pr)
    F[0] = [p / C[0] for p in pr]
    # C[0] = np.sum(pr)
    # F[0] = pr / C[0]

    for i in range(1, L):
        # With loops
        if method == 'loop':
            l_delta = [0] * N
            for k in range(N):
                l_delta[k] = (em_fn(k, X[i]) * sum([F[i-1][j] * tr[j][k] for j in range(N)]))

            # F[i] = np.array(l_delta)
            C[i] = sum(l_delta)
            F[i] = [d / C[i] for d in l_delta]
            # F[i] = np.array([d / C[i] for d in l_delta])

        # Vectorized
        else:
            em = np.array([em_fn(k, X[i]) for k in range(N)])
            l_delta = np.dot(a_tr, F[i-1]) * em
            C[i] = np.sum(l_delta)
            F[i] = l_delta / C[i]

    # return F
    return C, F

def anno_accuracy(refanno,testanno):
    correct = 0
    assert len(refanno) == len(testanno)
    for i in range(1,len(refanno)):
        if refanno[i] == testanno[i]:
            correct += 1
    return float(correct)/len(refanno)

if __name__ == "__main__":
    main()


