def mod_exp(base, exp, mod):
    result = 1
    while exp:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def brute_force(p, g, public_key):
    for priv in range(p):
        if mod_exp(g, priv, p) == public_key:
            return priv

def bsgs(g, h, p):
    import math
    m = int(math.sqrt(p)) + 1
    table = {mod_exp(g, j, p): j for j in range(m)}
    g_inv = pow(g, p-2, p)
    factor = mod_exp(g_inv, m, p)
    gamma = h
    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p

# Small key
p = 431
g = 2
a_priv = 123
b_priv = 321
A_pub = mod_exp(g, a_priv, p)
B_pub = mod_exp(g, b_priv, p)
print("Small A_pub =", A_pub)
print("Recovered a =", brute_force(p, g, A_pub))

# Large key
p_large = 10007
g_large = 5
a_large = 2345
A_large = mod_exp(g_large, a_large, p_large)
print("Recovered large a =", bsgs(g_large, A_large, p_large))
