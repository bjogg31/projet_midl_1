"""
main.py
Fichier de test et d'exécution des fonctions
"""

from datastructs import Var, FF, And, Not, Or, Impl
from test_formules import nb_feuilles, liste_var, negative
def main():
    f = Impl(And(Var("a"),FF()), Not(Var("b")))

    print("___________________________________________")
    print("TEST MANIPULATION DE FORMULES")
    print("___________________________________________")
    print(f"Formule initiale    : {f}")
    print(f"Nombre de feuilles  : {nb_feuilles(f)}")
    print(f"Liste des variables : {liste_var(f)}")
    print(f"Forme Négative      : {negative(f)}")

if __name__ == "__main__":
    main()
