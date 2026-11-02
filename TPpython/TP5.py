import unicodedata
from collections import Counter


# Exercice 1.1
def lettre_vers_nombre(lettre):
    return ord(lettre) - ord("A")


def nombre_vers_lettre(nombre):
    return chr(nombre % 26 + ord("A"))


print(lettre_vers_nombre("C"), nombre_vers_lettre(2))
print([nombre_vers_lettre(lettre_vers_nombre(c)) == c for c in "ABCXYZ"])

# Exercice 1.2
def nettoyer(texte):
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return "".join(c for c in texte.upper() if "A" <= c <= "Z")


print(nettoyer("Été, à Paris !"))

# Exercice 2.1
def chiffrer(texte, a, b):
    return "".join(
        nombre_vers_lettre(
            a * lettre_vers_nombre(lettre) + b
        )
        for lettre in nettoyer(texte)
    )


message = "ATTAQUEALAUBE"
print(chiffrer(message, 5, 8))
print(chiffrer(message, 1, 3))

# Exercice 3.1
def pgcd(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


valides = [a for a in range(1, 26) if pgcd(a, 26) == 1]
print(valides)
print(len(valides))

# Exercice 3.2
def inverse_modulaire(a, modulo):
    if modulo <= 1:
        raise ValueError("Le modulo doit être supérieur à 1")
    a %= modulo
    for candidat in range(1, modulo):
        if a * candidat % modulo == 1:
            return candidat
    raise ValueError(f"{a} n'est pas inversible modulo {modulo}")


print(inverse_modulaire(5, 26))
print(5 * 21 % 26)

try:
    inverse_modulaire(4, 26)
except ValueError as erreur:
    print(erreur)

# Exercice 4
def dechiffrer(texte, a, b):
    inverse = inverse_modulaire(a, 26)
    return "".join(
        nombre_vers_lettre(
            inverse * (lettre_vers_nombre(lettre) - b)
        )
        for lettre in nettoyer(texte)
    )


message = nettoyer("Attaque a l aube")
secret = chiffrer(message, 5, 8)
print(secret)
print(dechiffrer(secret, 5, 8))
print(dechiffrer(secret, 5, 8) == message)

try:
    dechiffrer(secret, 4, 7)
except ValueError as erreur:
    print(erreur)

# Exercice 5
def toutes_les_clefs(secret):
    return [
        (a, b, dechiffrer(secret, a, b))
        for a in valides
        for b in range(26)
    ]


essais = toutes_les_clefs(secret)
bons = [essai for essai in essais if essai[2] == message]
print(len(essais))
print(bons[0][0], bons[0][1])

# Exercice 6
texte_long = nettoyer(
    "Le chiffrement affine est un chiffrement par substitution monoalphabetique. "
    "Chaque lettre du message est remplacee par une autre lettre, toujours la meme, "
    "ce qui laisse intactes les frequences relatives des lettres et permet de casser "
    "le code sans essayer toutes les clefs possibles."
)
secret_long = chiffrer(texte_long, 7, 12)

comptes = Counter(secret_long)
lettre_frequente = comptes.most_common(1)[0][0]
print(lettre_frequente)

cible = lettre_vers_nombre(lettre_frequente)
candidats = []
for a in valides:
    b = (cible - 4 * a) % 26
    candidats.append((a, b, dechiffrer(secret_long, a, b)))

print(len(candidats))
for a, b, texte in candidats:
    if texte.startswith("LECHIFFREMENT"):
        print(a, b)
        print(texte[:60])
