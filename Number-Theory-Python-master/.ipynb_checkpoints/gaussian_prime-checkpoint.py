import math

def complex_eps(c): 
    return complex(round(c.real, 6), round(c.imag, 6))

def floor(c): 
    real = math.floor(round(c.real, 6))
    imag = math.floor(round(c.imag, 6))
    return complex(real, imag)

def complex_modulus(a, b): 
    return a - (b * floor(a / b))

def gaussian_gcd(a, b): 
    while b != 0+0j: 
        a, b = b, complex_modulus(a, b)
    return a

def modular_exponentiation(base, exponent, modulus):
    result = 1
    while exponent > 0:
        if (int(exponent) & 1) == 1: 
            result = (result * base) % modulus
        exponent=int(exponent)
        exponent >>= 1
        base = (base ** 2) % modulus
    return result

def root4(p): 
   # 4th root of 1 modulo p
   # Derived from http://bit.ly/p4ESdk by Robin Chapman
    base = 2
    pow = p/4
    while True:
        a = modular_exponentiation(base, pow, p)
        modulus = (a ** 2) % p
        if modulus == (p - 1): return a
        base += 1

def sq2(p): 
    a = root4(p) # 4th root of 1 modulo p
    return gaussian_gcd(complex(p, 0), complex(a, 1))

def first_quadrant_associate(c): 
    if c.real >= 0: 
        if c.imag >= 0: return c # 1st quadrant
        return c * 1j # 2nd quadrant
    elif c.imag < 0: return -c # 3rd quadrant
    return c * -1j # 4th quadrant

def factor(n): 
    if n < 2: return []

    if not (n & 1): # faster than n % 2
        res = factor(n // 2)
        return [2] + res

    for i in range(3, int(n ** .5) + 1, 2): 
        if not (n % i): 
            res = factor(n // i)
            return [i] + res
    return [n]

def norm(G): 
    return int(G.real ** 2) + int(G.imag ** 2)

def factor_gaussian(G): 
  # Algorithm from http://bit.ly/pCn9Hm by Jim Lewis
    N = norm(G)
    primes = factor(N)
    if primes == [1]: 
        return [G], 1

    factors = []
    while primes: 
        p = primes[0]

        if p == 2: 
            u = 1 + 1j
            if not complex_modulus(G, u): q = u
            else: q = 1 - 1j
            primes.remove(p)
        elif (p % 4) == 3: 
            q = p
            primes.remove(p)
            primes.remove(p)
        else: 
            u = sq2(p)
            u = first_quadrant_associate(u) # u[0] + (u[1] * 1j))
            if not complex_modulus(G, u): q = u
            else: q = u.conjugate()
            primes.remove(p)

        factors.append(q)
        G = complex_eps(G/q)
    return factors, G

def product(numbers): 
    result = 1
    for number in numbers: 
        result = result * number
    return result

def divisor_cardinality(factors): 
    powers = []
    unique_factors = set(factors)
    for unique_factor in unique_factors: 
        power = factors.count(unique_factor)
    powers.append(power)
    return product(power + 1 for power in powers)