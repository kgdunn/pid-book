# Randomized distribution 
# Box, Hunter and Hunter, Chapter 4, p 97:

import numpy as np
import matplotlib.pyplot as plt

def xuniqueCombinations(items, n):
    """ Code from: http://code.activestate.com/recipes/190465/ """
    if n==0: yield []
    else:
        for i in xrange(len(items)-n+1):
            for cc in xuniqueCombinations(items[i+1:],n-1):
                yield [items[i]]+cc

if __name__ == '__main__':
    number = 11
    subset_A = 5
    subset_B = number - subset_A
    outcomes = np.array([29.9, 11.4, 26.6, 23.7, 25.3, 28.5, 14.2, 17.9, 
                         16.5, 21.1, 24.3])

    choose_some = list(xuniqueCombinations(range(number), subset_A))
    print "Unique ways to split " + str(number) + ' experiments into 2 groups,',
    print "with " + str(subset_A) + ' (A) entries and ' + str(subset_B) + '',
    print '(B) entries:',
    print len(choose_some)
    
    handled = dict()
    diffs = []
    for subset in choose_some:
        y_A = 0.0
        y_B = sum(outcomes)
        entry = ['B']*number
    
        for item in subset:
            entry[item] = 'A'
            y_A += outcomes[item]
            y_B -= outcomes[item]
        
        key = ''
        for item in entry:
            key += item
        handled[key] = y_B/(subset_B+0.0) - y_A/(subset_A+0.0)        
        diffs.append(handled[key])
    
    diffs = np.array(diffs)   
    print diffs
    print sum(diffs>1.69)

    plt.hist(diffs,  bins=50)
    plt.show()
