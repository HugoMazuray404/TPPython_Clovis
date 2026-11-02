import math
import random


# Exercice 1.1
def vecteur(a, b):
    return b[0] - a[0], b[1] - a[1]


def produit_scalaire(u, v):
    return u[0] * v[0] + u[1] * v[1]


def norme(vecteur):
    return math.hypot(*vecteur)


def angle(u, v):
    produit_normes = norme(u) * norme(v)
    if produit_normes == 0:
        raise ValueError("L'angle d'un vecteur nul n'est pas défini")
    cosinus = produit_scalaire(u, v) / produit_normes
    cosinus = max(-1.0, min(1.0, cosinus))
    return math.degrees(math.acos(cosinus))


print(norme((3, 4)), produit_scalaire((1, 2), (3, 4)))
print(angle((1, 0), (1, 1)), angle((1, 0), (0, 1)))
print(angle((2, 0), (2, 0)))

# Exercice 1.2
def determinant(u, v):
    return u[0] * v[1] - u[1] * v[0]


def distance_point_droite(point, a, b):
    ab = vecteur(a, b)
    if norme(ab) == 0:
        raise ValueError("Les deux points doivent être distincts")
    return abs(determinant(ab, vecteur(a, point))) / norme(ab)


print(distance_point_droite((0, 0), (0, 1), (1, 0)), math.sqrt(2) / 2)
print(distance_point_droite((3, 4), (0, 0), (1, 0)))

# Exercice 2.1
def orientation(a, b, c):
    valeur = determinant(vecteur(a, b), vecteur(a, c))
    return (valeur > 0) - (valeur < 0)


print(orientation((0, 0), (1, 0), (1, 1)))
print(orientation((0, 0), (1, 0), (1, -1)))
print(orientation((0, 0), (1, 1), (2, 2)))

# Exercice 2.2
def aire(polygone):
    if len(polygone) < 3:
        return 0
    somme = sum(
        polygone[i][0] * polygone[(i + 1) % len(polygone)][1]
        - polygone[(i + 1) % len(polygone)][0] * polygone[i][1]
        for i in range(len(polygone))
    )
    return abs(somme) / 2


carre = [(0, 0), (1, 0), (1, 1), (0, 1)]
triangle = [(0, 0), (4, 0), (0, 3)]
maison = [(0, 0), (2, 0), (2, 1.5), (1, 2.5), (0, 1.5)]
print(aire(carre), aire(triangle), aire(maison))

# Exercice 3.1
def se_coupent(a, b, c, d):
    return (
        orientation(a, b, c) * orientation(a, b, d) < 0
        and orientation(c, d, a) * orientation(c, d, b) < 0
    )


print(se_coupent((0, 0), (1, 1), (0, 1), (1, 0)))
print(se_coupent((0, 0), (1, 0), (0, 1), (1, 1)))
print(se_coupent((0, 0), (1, 1), (2, 2), (3, 3)))

# Exercice 3.2
def intersection(a, b, c, d):
    ab = vecteur(a, b)
    cd = vecteur(c, d)
    denominateur = determinant(ab, cd)
    if denominateur == 0:
        return None

    ac = vecteur(a, c)
    t = determinant(ac, cd) / denominateur
    u = determinant(ac, ab) / denominateur
    if 0 <= t <= 1 and 0 <= u <= 1:
        return a[0] + t * ab[0], a[1] + t * ab[1]
    return None


print(intersection((0, 0), (2, 2), (0, 2), (2, 0)))
print(intersection((0, 0), (1, 0), (0, 1), (1, 1)))
print(intersection((0, 0), (1, 1), (2, 2), (3, 3)))

# Exercice 4.1
def _sur_segment(point, a, b):
    ab = vecteur(a, b)
    ap = vecteur(a, point)
    return (
        determinant(ab, ap) == 0
        and min(a[0], b[0]) <= point[0] <= max(a[0], b[0])
        and min(a[1], b[1]) <= point[1] <= max(a[1], b[1])
    )


def dedans(point, polygone):
    if len(polygone) < 3:
        return False
    x, y = point
    interieur = False

    for i, (x1, y1) in enumerate(polygone):
        x2, y2 = polygone[(i + 1) % len(polygone)]
        if _sur_segment(point, (x1, y1), (x2, y2)):
            return True
        if (y1 > y) != (y2 > y):
            x_croisement = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < x_croisement:
                interieur = not interieur
    return interieur


for point in ((1, 1), (1, 2.4), (3, 1), (0.2, 2.2)):
    print(point, dedans(point, maison))

# Exercice 4.2
random.seed(0)
tirages = 200_000
touches = 0
for _ in range(tirages):
    point = (random.uniform(0, 2), random.uniform(0, 2.5))
    if dedans(point, maison):
        touches += 1

print(2 * 2.5 * touches / tirages)

# Exercice 5.1
etoile = []
for k in range(10):
    rayon = 2 if k % 2 == 0 else 0.8
    angle = math.pi / 2 + k * math.pi / 5
    etoile.append((rayon * math.cos(angle), rayon * math.sin(angle)))

print(round(aire(etoile), 4))
print(dedans((0, 0), etoile), dedans((0, 1.5), etoile), dedans((1.2, 1.2), etoile))


def tracer_polygone(polygone, points=()):
    import matplotlib.pyplot as plt

    if polygone:
        sommets = polygone + [polygone[0]]
        xs, ys = zip(*sommets)
        plt.plot(xs, ys)
    if points:
        xs, ys = zip(*points)
        plt.scatter(xs, ys)
    plt.axis("equal")
    plt.show()


tracer_polygone(etoile, [(0, 0), (0, 1.5), (1.2, 1.2), (0, 1.9)])

# Exercice 6.1
def zone_de(point, zones):
    for indice, zone in enumerate(zones):
        if dedans(point, zone):
            return indice
    return None


zones = [maison, [(3, 0), (4, 0), (4, 1), (3, 1)]]
for point in ((1, 1), (3.5, 0.5), (2.5, 0.5)):
    print(point, zone_de(point, zones))
