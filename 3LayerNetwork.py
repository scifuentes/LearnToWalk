import numpy as np

def nonlin(x,deriv=False):
    if(deriv):
        return x*(1-x)

    return 1/(1+np.exp(-x))
    
X = np.array([[3,1,-1,-3,1],
              [1,-1,-3,3,1],
              [-1,-3,3,1,1],
              [-3,3,1,-1,1],

              [3,1,-3,-1,1],
              [1,-1,3,-3,1],
              [-1,-3,1,3,1],
              [-3,3,-1,1,1],

              [3,-3,1,-1,1],
              [1,3,-1,-3,1],
              [-1,1,-3,3,1],
              [-3,-1,3,1,1],

              [3,-3,-1,1,1],
              [1,3,-3,-1,1],
              [-1,1,3,-3,1],
              [-3,-1,1,3,1],

              [3,-1,1,-3,1],
              [1,-3,-1,3,1],
              [-1,3,-3,1,1],
              [-3,1,3,-1,1],

              [3,-1,-3,1,1],
              [1,-3,3,-1,1],
              [-1,3,1,-3,1],
              [-3,1,-1,3,1]
              ])
                
y = np.array([[1,-1,-3,3],
              [-1,-3,3,1],
              [-3,3,1,-1],
              [3,1,-1,-3],
              
              [1,-1,3,-3],
              [-1,-3,1,3],
              [-3,3,-1,1],
              [3,1,-3,-1],

              [1,3,-1,-3],
              [-1,1,-3,3],
              [-3,-1,3,1],
              [3,-3,1,-1],

              [1,3,-3,-1],
              [-1,1,3,-3],
              [-3,-1,1,3],
              [3,-3,-1,1],

              [1,-3,-1,3],
              [-1,3,-3,1],
              [-3,1,3,-1],
              [3,-1,1,-3],

              [1,-3,3,-1],
              [-1,3,1,-3],
              [-3,1,-1,3],
              [3,-1,-3,1]
              ])

np.random.seed(1)

# randomly initialize our weights with mean 0
syn0 = 2*np.random.random((len(X[0]),8)) - 1
syn1 = 2*np.random.random((8,len(y[0]))) - 1

for j in xrange(10000000):

    #pick one of the training samples
    s = np.random.randint(0,len(X))
    
    # Feed forward through layers 0, 1, and 2
    l0 = X[s]/10.
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))

    # how much did we miss the target value?
    l2_error = y[s]/10. - l2
    
    if (j% 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error)))
        
    # in what direction is the target value?
    # were we really sure? if so, don't change too much.
    l2_delta = l2_error*nonlin(l2,deriv=True)

    # how much did each l1 value contribute to the l2 error (according to the weights)?
    l1_error = l2_delta.dot(syn1.T)
    
    # in what direction is the target l1?
    # were we really sure? if so, don't change too much.
    l1_delta = l1_error * nonlin(l1,deriv=True)

    syn1 += np.outer(l1,l2_delta)
    syn0 += np.outer(l0,l1_delta)
