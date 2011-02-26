# Randomized distribution 
# Box, Hunter and Hunter, Chapter 4, p 97:

import numpy as np
import matplotlib.pyplot as plt
import time as time

def xuniqueCombinations(items, n):
    """ Code from: http://code.activestate.com/recipes/190465/ """
    if n==0: yield []
    else:
        for i in xrange(len(items)-n+1):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

if __name__ == '__main__':
    case_A = np.array([254, 440, 501, 368, 697, 476, 188, 525])
    case_B = np.array([338,470,558,426,733,539,240,628,517])
    
    #case_A = np.array([254,440,501,368,697,476,188,525,451,517,370,396,279,450,422,406,425,544,376,335])
    #case_B = np.array([338,470,558,426,733,539,240,628,517,564,435,306,558,358,429,291,520,491,489,479,591,428,424])
    
    # Box, Hunter and Hunter tomato case
    #case_A = np.array([29.9, 11.4, 25.3, 16.5, 21.1])
    #case_B = np.array([26.6, 23.7, 28.5, 14.2, 17.9, 24.3])
    
    n_A = case_A.shape[0]
    n_B = case_B.shape[0]
    number = n_A + n_B
    import scipy.misc as misc
    fact = misc.factorial
    print "Runs required = " + str(fact(number)/fact(n_A)/fact(n_B))
    outcomes = np.concatenate((case_A, case_B))

    choose_some = xuniqueCombinations(range(number), n_A)
    print "Unique ways to split " + str(number) + ' experiments into 2 groups,',
    print "with " + str(n_A) + ' (A) entries and ' + str(n_B) + '',
    print '(B) entries:',
    
    n=0
    handled = dict()
    diffs = []
    
    t = time.time()
    for subset in choose_some:
        n+=1
        y_A = 0.0
        y_B = sum(outcomes)
        entry = ['B']*number
            
        for item in subset:
            entry[item] = 'A'
            y_A += outcomes[item]
            y_B -= outcomes[item]
        
        print entry
        key = ''
        for item in entry:
           key += item
        handled[key] = y_B/(n_B+0.0) - y_A/(n_A+0.0)        
        diffs.append(handled[key])
        
        if not(n%10000):
            print str(n)
        if n==1E6:
            break

        
    print len(diffs)            
    print time.time() - t
    
    actual_diff = np.mean(case_B) - np.mean(case_A)
    print "Actual difference = " + str(actual_diff)
    print "Number greater than this: ",
    print sum(np.array(diffs)>actual_diff)
    print "Fraction = ", 
    print sum(np.array(diffs)>actual_diff) / (len(diffs)+0.0)
    
    from matplotlib.figure import Figure
    fig = Figure(figsize=(5, 2.5))
    rect = [0.2, 0.20, 0.80, 0.80]  # Left, bottom, width, height
    ax = fig.add_subplot(111, frame_on=False)
    ax.hist(diffs,  bins=50, facecolor='none')
    ax.axvline(actual_diff, c="red")
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    canvas=FigureCanvasAgg(fig)
    fig.savefig('single-experiment-randomization-some.png', dpi=300, facecolor='w', edgecolor='w', 
                orientation='portrait', papertype=None, format=None, transparent=True)
    
