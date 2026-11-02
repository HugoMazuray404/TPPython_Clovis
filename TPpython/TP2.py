from math import isqrt
from time import perf_counter


# Exercice 1.1
def diviseurs(n):
    if n <= 0:
        raise ValueError("n doit être strictement positif")
    return [d for d in range(1, n + 1) if n % d == 0]


print(diviseurs(28))
print(diviseurs(97))

# Exercice 2.1
def pgcd_naif(a, b):
    meilleur = 0
    for d in range(1, min(abs(a), abs(b)) + 1):
        if a % d == 0 and b % d == 0:
            meilleur = d
    return meilleur


def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


print(pgcd_naif(1071, 462), pgcd(1071, 462))

# Exercice 3.1
def est_premier_naif(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, n))


def est_premier(n):
    if n < 2:
        return False
    return all(n % d for d in range(2, isqrt(n) + 1))


def duree(fonction, n):
    debut = perf_counter()
    fonction(n)
    return perf_counter() - debut


for n in (10_007, 100_003, 1_000_003):
    t_naif = duree(est_premier_naif, n)
    t_racine = duree(est_premier, n)
    print(f"{n:>9} : naïf {t_naif:.5f} s | racine {t_racine:.6f} s")

# Exercice 4.1
def crible(limite):
    if limite < 0:
        raise ValueError("La limite doit être positive ou nulle")
    premiers = [True] * (limite + 1)
    if limite >= 0:
        premiers[0] = False
    if limite >= 1:
        premiers[1] = False

    for nombre in range(2, isqrt(limite) + 1):
        if premiers[nombre]:
            for multiple in range(nombre * nombre, limite + 1, nombre):
                premiers[multiple] = False
    return [nombre for nombre, est_premier in enumerate(premiers) if est_premier]


debut = perf_counter()
premiers = crible(100_000)
t_crible = perf_counter() - debut

debut = perf_counter()
combien = sum(est_premier(n) for n in range(100_001))
t_un_par_un = perf_counter() - debut

print(len(premiers), combien)
print(f"crible {t_crible:.4f} s | un par un {t_un_par_un:.4f} s")

# Exercice 5.1
def facteurs(n):
    if n < 1:
        raise ValueError("n doit être strictement positif")
    resultat = []
    diviseur = 2
    while diviseur * diviseur <= n:
        while n % diviseur == 0:
            resultat.append(diviseur)
            n //= diviseur
        diviseur += 1
    if n > 1:
        resultat.append(n)
    return resultat


decomposition = facteurs(360)
print(decomposition)
produit = 1
for facteur in decomposition:
    produit *= facteur
print(produit)
