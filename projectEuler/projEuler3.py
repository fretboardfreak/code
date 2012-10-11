#!/usr/bin/env python
'''
Find the largest palindrome made from the product of two 3-digit numbers.

A palindromic number reads the same both ways. The largest palindrome made from the product of two 2-digit
numbers is 9009 = 91 x 99.
'''
import sys

def getList( string ):
    '''
    return a list with 1 char per item.
    '''
    retVal = []
    for char in string:
        retVal.append( char )
    return retVal

def isPalindrome( integer ):
    '''
    True if integer is a palindrome.
    '''
    string = integer.__str__()
    forward = getList( string )
    reverse = forward[:]
    reverse.reverse()
    if forward == reverse:
        return True
    return False

def main():
    palindromes = []
    a = 999
    b = 999
    while True:
        test = a * b
        result = isPalindrome( test )
        if result:
            palindromes.append( test )
        if a == 100:
            b -= 1
            a = 999
        if b == 100:
            break
        a -= 1

    palindromes.sort()
    print palindromes
    print 'And the winner is: %s' % palindromes[-1]
    return palindromes[-1]


# ------------------------------------------------------------

if __name__ == '__main__':
    try:
        sys.exit( main() )
    except KeyboardInterrupt:
        print 'Interrupted by User.'
        sys.exit( 1 )


