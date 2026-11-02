from time import perf_counter


# Exercice 1
def evaluer_naif(polynome, x):
    return sum(coefficient * x**i for i, coefficient in enumerate(polynome))


print(evaluer_naif([2, 3, 0, 5], 2))

# Exercice 2
def evaluer(polynome, x):
    valeur = 0
    for coefficient in reversed(polynome):
        valeur = valeur * x + coefficient
    return valeur


polynome = [2, 3, 0, 5]
for x in (-2, 0, 1, 2, 10):
    print(x, evaluer_naif(polynome, x), evaluer(polynome, x))

# Exercice 2.2
for degre in (1000, 5000, 20000):
    polynome = [1] * (degre + 1)

    debut = perf_counter()
    valeur_naive = evaluer_naif(polynome, 1.0001)
    temps_naif = perf_counter() - debut

    debut = perf_counter()
    valeur_horner = evaluer(polynome, 1.0001)
    temps_horner = perf_counter() - debut

    rapport = temps_naif / temps_horner if temps_horner else float("inf")
    print(
        f"degré {degre:>6} : naïf {temps_naif:.5f} s | "
        f"Horner {temps_horner:.5f} s | rapport {rapport:.1f} | "
        f"écart {abs(valeur_naive - valeur_horner):.2e}"
    )

# Exercice 2.3
for degre in (200, 400, 800):
    polynome = [1] * (degre + 1)

    debut = perf_counter()
    valeur_naive = evaluer_naif(polynome, 3)
    temps_naif = perf_counter() - debut

    debut = perf_counter()
    valeur_horner = evaluer(polynome, 3)
    temps_horner = perf_counter() - debut

    rapport = temps_naif / temps_horner if temps_horner else float("inf")
    print(f"degré {degre:>4} : rapport {rapport:.1f} | résultats égaux : {valeur_naive == valeur_horner}")

# Exercice 3
def deriver(polynome):
    return [i * polynome[i] for i in range(1, len(polynome))]


print(deriver([2, 3, 0, 5]))
print(deriver([7]))

# Exercice 4
def dichotomie(fonction, a, b, tolerance=1e-12):
    if tolerance <= 0 or a > b:
        raise ValueError("Intervalle ou tolérance invalide")

    valeur_a = fonction(a)
    valeur_b = fonction(b)
    if valeur_a == 0:
        return a
    if valeur_b == 0:
        return b
    if valeur_a * valeur_b > 0:
        raise ValueError("Les valeurs aux bornes doivent être de signes opposés")

    while b - a > tolerance:
        milieu = (a + b) / 2
        valeur_milieu = fonction(milieu)
        if valeur_milieu == 0:
            return milieu
        if valeur_a * valeur_milieu < 0:
            b = milieu
        else:
            a, valeur_a = milieu, valeur_milieu
    return (a + b) / 2


def carre_moins_deux(x):
    return x * x - 2


racine = dichotomie(carre_moins_deux, 0, 2)
print(racine)
print(abs(racine - 2**0.5) < 1e-9)

# Exercice 4.2
def newton(polynome, depart, tolerance=1e-12, tours_max=100):
    derivee = deriver(polynome)
    x = float(depart)

    for tour in range(tours_max):
        valeur = evaluer(polynome, x)
        if abs(valeur) <= tolerance:
            return x, tour

        pente = evaluer(derivee, x)
        if pente == 0:
            raise ZeroDivisionError("La dérivée est nulle")

        suivant = x - valeur / pente
        if abs(suivant - x) <= tolerance * max(1.0, abs(suivant)):
            if abs(evaluer(polynome, suivant)) <= tolerance:
                return suivant, tour + 1
            raise RuntimeError("La méthode de Newton n'a pas convergé")
        x = suivant

    raise RuntimeError(f"Pas de convergence en {tours_max} itérations")


polynome = [-5, -2, 0, 1]
racine, tours = newton(polynome, 2)
print(racine, "en", tours, "itérations")
print(abs(evaluer(polynome, racine)) < 1e-10)

# Exercice 4.3
def newton_trace(polynome, depart, tours):
    derivee = deriver(polynome)
    x = float(depart)
    trajet = [x]

    for _ in range(tours):
        pente = evaluer(derivee, x)
        if pente == 0:
            break
        x -= evaluer(polynome, x) / pente
        trajet.append(x)
    return trajet


polynome = [2, -2, 0, 1]
print(newton_trace(polynome, 0, 8))

try:
    print(newton(polynome, 0))
except RuntimeError as erreur:
    print("Échec :", erreur)

# Exercice 4.4
polynome = [-5, -2, 0, 1]
for depart in (2, 1, 0):
    racine, tours = newton(polynome, depart)
    print(f"départ {depart:>2} : {tours:>2} itérations, racine {racine:.9f}")

# Exercice 5
import matplotlib.pyplot as plt

polynome = [-5, -2, 0, 1]
xs = [i / 100 for i in range(-300, 301)]
ys = [evaluer(polynome, x) for x in xs]

plt.plot(xs, ys, label="x³ - 2x - 5")
plt.axhline(0, linewidth=0.8)
plt.axvline(0, linewidth=0.8)
plt.ylim(-20, 20)
plt.xlabel("x")
plt.ylabel("P(x)")
plt.legend()
plt.title("Polynôme et racine réelle")
plt.show()

# Exercice 6
def somme(polynome_a, polynome_b):
    longueur = max(len(polynome_a), len(polynome_b))
    a = polynome_a + [0] * (longueur - len(polynome_a))
    b = polynome_b + [0] * (longueur - len(polynome_b))
    return [a[i] + b[i] for i in range(longueur)]


def produit_poly(polynome_a, polynome_b):
    if not polynome_a or not polynome_b:
        return []
    resultat = [0] * (len(polynome_a) + len(polynome_b) - 1)
    for i, coefficient_a in enumerate(polynome_a):
        for j, coefficient_b in enumerate(polynome_b):
            resultat[i + j] += coefficient_a * coefficient_b
    return resultat


print(somme([1, 2], [0, 0, 3]))
print(produit_poly([1, 1], [1, 1]))
print(produit_poly([-1, 1], [1, 1]))

binome = [1]
for _ in range(10):
    binome = produit_poly(binome, [1, 1])
print(binome)
print(sum(binome), 2**10)

# Exercice 7
import math


def derivee_avant(fonction, x, h):
    if h == 0:
        raise ValueError("h doit être non nul")
    return (fonction(x + h) - fonction(x)) / h


def derivee_centree(fonction, x, h):
    if h == 0:
        raise ValueError("h doit être non nul")
    return (fonction(x + h) - fonction(x - h)) / (2 * h)


exacte = math.cos(1.0)
for h in (1e-1, 1e-2, 1e-4, 1e-6, 1e-8, 1e-10, 1e-12):
    erreur_avant = abs(derivee_avant(math.sin, 1.0, h) - exacte)
    erreur_centree = abs(derivee_centree(math.sin, 1.0, h) - exacte)
    print(f"h = {h:.0e} : avant {erreur_avant:.1e} | centrée {erreur_centree:.1e}")

# Exercice 8
def rectangles(fonction, a, b, n):
    if n <= 0:
        raise ValueError("n doit être strictement positif")
    h = (b - a) / n
    return h * sum(fonction(a + i * h) for i in range(n))


def trapezes(fonction, a, b, n):
    if n <= 0:
        raise ValueError("n doit être strictement positif")
    h = (b - a) / n
    interieur = sum(fonction(a + i * h) for i in range(1, n))
    return h * ((fonction(a) + fonction(b)) / 2 + interieur)


def simpson(fonction, a, b, n):
    if n <= 0:
        raise ValueError("n doit être strictement positif")
    if n % 2:
        n += 1
    h = (b - a) / n
    impairs = sum(fonction(a + i * h) for i in range(1, n, 2))
    pairs = sum(fonction(a + i * h) for i in range(2, n, 2))
    return h / 3 * (fonction(a) + fonction(b) + 4 * impairs + 2 * pairs)


def carre(x):
    return x * x


for n in (10, 100, 1000):
    erreur_rectangles = abs(rectangles(carre, 0, 1, n) - 1 / 3)
    erreur_trapezes = abs(trapezes(carre, 0, 1, n) - 1 / 3)
    erreur_simpson = abs(simpson(carre, 0, 1, n) - 1 / 3)
    print(
        f"n = {n:>4} : rectangles {erreur_rectangles:.1e} | "
        f"trapèzes {erreur_trapezes:.1e} | Simpson {erreur_simpson:.1e}"
    )

# Exercice 8.2
def arctangente_derivee(x):
    return 4 / (1 + x * x)


approx_trapezes = trapezes(arctangente_derivee, 0, 1, 1000)
approx_simpson = simpson(arctangente_derivee, 0, 1, 1000)
print(approx_trapezes, abs(approx_trapezes - math.pi))
print(approx_simpson, abs(approx_simpson - math.pi))
