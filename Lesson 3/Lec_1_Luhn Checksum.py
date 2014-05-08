# concise definition of the Luhn checksum:
#
# "For a card with an even number of digits, double every odd numbered
# digit and subtract 9 if the product is greater than 9. Add up all
# the even digits as well as the doubled-odd digits, and the result
# must be a multiple of 10 or it's not a valid card. If the card has
# an odd number of digits, perform the same addition doubling the even
# numbered digits instead."
#
# for more details see here:
# http://www.merriampark.com/anatomycc.htm
#
# also see the Wikipedia entry, but don't do that unless you really
# want the answer, since it contains working Python code!
# 
# Implement the Luhn Checksum algorithm as described above.

# is_luhn_valid takes a credit card number as input and verifies 
# whether it is valid or not. If it is valid, it returns True, 
# otherwise it returns False.

#from math import log,ceil

def is_luhn_valid(n):
    # Generate a list of the digits in reverse order
    # L = [n/10**i % 10 for i in range(int(ceil(log(n,10))))] ## First try, doesn't work when n is a power of 10
    L = [int(s) for s in str(n)[::-1]]
    chk = sum(L[0::2]) + sum(2*N % 9 if N!=9 else 9 for N in L[1::2])
    return chk % 10 == 0

    # The 2nd term could also be: sum(map(lambda N: 2*N % 9 if N!=9 else 9, L[1::2]))
    # This one-liner also works:
    # chk = sum(2*N % 9 if i % 2 and N!=9 else N for i, N in enumerate(L))
