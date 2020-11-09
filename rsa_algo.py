import random


# Find GCD and Bezout coefficients
def saunderson(bigger, smaller):
    # out: (GCD, Bezout bigger, Bezout smaller)
    if smaller > bigger:
        print("saunderson: invalid arguments.")
        return 0, 0, 0
    # first iteration
    saund = [
        (bigger, 0, 1, 0),
        (smaller, bigger // smaller, 0, 1)
    ]
    currIndx = 2
    prevRemainder = 1
    bezoutB = 1
    bezoutS = 1
    nextRemainder = saund[currIndx - 2][0] % saund[currIndx - 1][0]
    while nextRemainder != 0:
        quotient = saund[currIndx - 1][0] // nextRemainder
        bezoutB = saund[currIndx - 2][2] - (saund[currIndx - 1][1] * saund[currIndx - 1][2])
        bezoutS = saund[currIndx - 2][3] - (saund[currIndx - 1][1] * saund[currIndx - 1][3])
        newLine = (nextRemainder, quotient, bezoutB, bezoutS)
        saund += [newLine]
        currIndx += 1
        prevRemainder = nextRemainder
        nextRemainder = saund[currIndx - 2][0] % saund[currIndx - 1][0]
    return prevRemainder, bezoutB, bezoutS


def generateKeys():
    # Generate private and public keys
    f = open("trial1.txt")
    goodPrimes = f.readlines()
    f.close()
    f = open("trial.txt")
    primes = f.readlines()
    f.close()
    p, q, N = 0, 0, 0
    while q == p or str(N)[0] != "9":
        p, q = int(random.choice(goodPrimes)[:-1]), int(random.choice(goodPrimes)[:-1])
        N = p * q
    d = (p - 1) * (q - 1)
    e = d
    mdc = 0
    while not (e < d and mdc == 1):
        e = int(random.choice(primes)[:-1])
        if e < d:
            saund = saunderson(d, e)
            mdc = saund[0]
            revE = saund[2] % d
    privateKey = revE
    mypublicKey = e
    return privateKey, mypublicKey
