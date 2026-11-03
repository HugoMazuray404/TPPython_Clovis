"""
Estimer pi avec de la geometrie et du hasard.
On tire des points au hasard dans un carre de cote 2, centre en (0, 0).
La proportion de points dans le cercle de rayon 1 est environ pi / 4.
On peut donc estimer pi en multipliant cette proportion par 4.        """

import random


def estimer_pi(nombre_de_points):
    dedans = 0

    for _ in range(nombre_de_points):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        if x * x + y * y <= 1:
            dedans += 1

    return 4 * dedans / nombre_de_points


random.seed(42)  # Pour retrouver les memes resultats a chaque lancement.

for nombre in (100, 1_000, 10_000):
    estimation = estimer_pi(nombre)
    erreur = abs(estimation - 3.141592653589793)
    print(
        f"{nombre:>6} points : pi ~= {estimation:.5f} "
        f"(erreur : {erreur:.5f})"
    )

    """avec plus de points, l'estimation penche en general a se rapprocher de pi, mais le hasard peut faire varier l'erreur."""
