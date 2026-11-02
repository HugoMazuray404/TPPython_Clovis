import math


# Exercice 1.1
n = 2026
d = 7
quotient, reste = divmod(n, d)
print(quotient, reste)
print(quotient * d + reste == n)

# Exercice 1.2
n = 123456789
print(n % 10)
print(n // 10)

# Exercice 2.1
total = sum(0.1 for _ in range(1000))
print(total)
print(total - 100)

# Exercice 2.2
def presque_egaux(a, b, tolerance=1e-9):
    return abs(a - b) <= tolerance


print(presque_egaux(0.1 + 0.2, 0.3))
print(presque_egaux(1.0, 1.5))

# Exercice 3.1
for i in range(1, 11):
    print(f"7 x {i} = {7 * i}")

# Exercice 3.2
n = 100
print(sum(range(1, n + 1)))
print(n * (n + 1) // 2)

# Exercice 4.1
def nombre_de_chiffres(n):
    return len(str(abs(n)))


print(nombre_de_chiffres(2026))
print(nombre_de_chiffres(7))
print(nombre_de_chiffres(10**60))
print(nombre_de_chiffres(-2026))

# Exercice 5.1
def heron(a, tolerance=1e-12):
    if a < 0:
        raise ValueError("La racine carrée d'un nombre négatif n'est pas réelle.")
    if a == 0:
        return 0.0

    x = float(a)
    while True:
        suivant = (x + a / x) / 2
        if abs(suivant - x) <= tolerance * abs(suivant):
            return suivant
        x = suivant


print(heron(2))
print(math.sqrt(2))
print(abs(heron(2) - math.sqrt(2)) < 1e-12)
