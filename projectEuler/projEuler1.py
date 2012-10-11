#!/usr/bin/env python
'''
Project Euler Problem 1

Completed 08:30 20091104
'''
import sys

def main():
    '''Project Euler Problem 1
    
    find the sum of all multiples of 3 or 5 below 1000
    '''
    sum = 0
    counter = 0
    for i in range(1,1001):
        if i % 3 is 0:
            counter += i
        elif i % 5 is 0:
            counter += i

    print 'The sum of all the multiples of 3 or 5 below 1000 is: %s' % counter
    return 0

if __name__ == '__main__':
    try:
        sys.exit( main() )
    except KeyboardInterrupt:
        print 'Interrupted by User.'
        sys.exit( 1 )


