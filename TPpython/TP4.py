import random
import time

import numpy as np


# Exercice 1
matrice = [
    [1, 2, 2],
    [1, 3, -2],
    [3, 5, 8],
]

print(matrice[0])
print(matrice[0][2])
print(len(matrice), len(matrice[0]))

# Exercice 1.1
def transposee(matrice):
    if not matrice:
        return []
    return [list(colonne) for colonne in zip(*matrice)]


matrice = [[1, 2, 3], [4, 5, 6]]
print(transposee(matrice))

# Exercice 2.1
def produit(matrice_a, matrice_b):
    if not matrice_a:
        return []
    if any(len(ligne) != len(matrice_a[0]) for ligne in matrice_a):
        raise ValueError("La première matrice doit être rectangulaire")
    if not matrice_b or len(matrice_b) != len(matrice_a[0]):
        raise ValueError("Dimensions incompatibles")
    if any(len(ligne) != len(matrice_b[0]) for ligne in matrice_b):
        raise ValueError("La deuxième matrice doit être rectangulaire")

    lignes, colonnes = len(matrice_a), len(matrice_b[0])
    resultat = [[0] * colonnes for _ in range(lignes)]
    for i in range(lignes):
        for j in range(colonnes):
            resultat[i][j] = sum(
                matrice_a[i][k] * matrice_b[k][j]
                for k in range(len(matrice_b))
            )
    return resultat


identite = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
matrice = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
print(produit(matrice, identite) == matrice)
print(produit([[1, 2], [3, 4]], [[0, 1], [1, 0]]))

# Exercice 2.2
def matrice_aleatoire(n):
    return [[random.random() for _ in range(n)] for _ in range(n)]


random.seed(42)
for taille in (40, 80, 120):
    matrice_a = matrice_aleatoire(taille)
    matrice_b = matrice_aleatoire(taille)
    debut = time.perf_counter()
    produit(matrice_a, matrice_b)
    print(f"n = {taille:>3} : {time.perf_counter() - debut:.4f} s")

# Exercice 3.1
taille = 120
matrice_a = matrice_aleatoire(taille)
matrice_b = matrice_aleatoire(taille)

debut = time.perf_counter()
produit(matrice_a, matrice_b)
temps_python = time.perf_counter() - debut

matrice_a_numpy = np.array(matrice_a)
matrice_b_numpy = np.array(matrice_b)
debut = time.perf_counter()
matrice_a_numpy @ matrice_b_numpy
temps_numpy = time.perf_counter() - debut

print(f"Python pur {temps_python:.4f} s")
print(f"NumPy      {temps_numpy:.6f} s")
print("Rapport :", round(temps_python / max(temps_numpy, 1e-9)))

# Exercice 4.1
def resoudre(matrice, second_membre, tolerance=1e-14):
    n = len(matrice)
    if n == 0 or len(second_membre) != n:
        raise ValueError("Dimensions incompatibles")
    if any(len(ligne) != n for ligne in matrice):
        raise ValueError("La matrice doit être carrée")
    if tolerance <= 0:
        raise ValueError("La tolérance doit être positive")

    travail = [list(matrice[i]) + [second_membre[i]] for i in range(n)]

    for k in range(n):
        pivot = max(range(k, n), key=lambda i: abs(travail[i][k]))
        if abs(travail[pivot][k]) <= tolerance:
            raise ValueError("Système singulier ou mal posé")
        travail[k], travail[pivot] = travail[pivot], travail[k]

        for i in range(k + 1, n):
            facteur = travail[i][k] / travail[k][k]
            for j in range(k, n + 1):
                travail[i][j] -= facteur * travail[k][j]

    solution = [0.0] * n
    for i in range(n - 1, -1, -1):
        reste = travail[i][n] - sum(
            travail[i][j] * solution[j] for j in range(i + 1, n)
        )
        solution[i] = reste / travail[i][i]
    return solution


matrice = [[1, 2, 2], [1, 3, -2], [3, 5, 8]]
second_membre = [2, -1, 8]
solution = resoudre(matrice, second_membre)
print([round(valeur, 10) for valeur in solution])
verification = [
    sum(matrice[i][j] * solution[j] for j in range(3))
    for i in range(3)
]
print([round(valeur, 10) for valeur in verification])

# Exercice 5
random.seed(7)
taille = 50
matrice = matrice_aleatoire(taille)
second_membre = [random.random() for _ in range(taille)]

solution_python = resoudre(matrice, second_membre)
solution_numpy = np.linalg.solve(np.array(matrice), np.array(second_membre))
ecart = max(
    abs(solution_python[i] - solution_numpy[i])
    for i in range(taille)
)
print("Écart maximal :", ecart)
print(ecart < 1e-9)

# Exercice 6
def rotation(angle):
    cosinus, sinus = np.cos(angle), np.sin(angle)
    return np.array([[cosinus, -sinus], [sinus, cosinus]])


gauche = rotation(np.pi / 3) @ rotation(np.pi / 6)
droite = rotation(np.pi / 2)
print(np.allclose(gauche, droite))
print(np.round(droite, 10))
