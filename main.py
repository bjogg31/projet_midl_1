"""
main.py
Fichier de test et d'exécution des fonctions
"""

from datastructs import Var, FF, And, Not, Or, Impl, Seq
from test_formules import nb_feuilles, liste_var, negative
from regles_calcul_tableaux import calculus
from moteur_preuve import next_proof_state


def get_affichage_liste_sequents(liste_sequents: list[Seq]) -> str:
    """
    Renvoie l'affichage formaté d'une liste de sequents
    """
    affichage = "["

    for i in range(len(liste_sequents)):
        sequent = liste_sequents[i]

        affichage += str(sequent)
        if i < len(liste_sequents)-1:
            affichage += ",\n "

    affichage += "]"
    return affichage

def main():
    f = Impl(And(Var("a"), FF()), Not(Var("b")))

    print("___________________________________________")
    print("TEST MANIPULATION DE FORMULES")
    print("___________________________________________")
    print(f"Formule initiale    : {f}")
    print(f"Nombre de feuilles  : {nb_feuilles(f)}")
    print(f"Liste des variables : {liste_var(f)}")
    print(f"Forme Négative      : {negative(f)}")
    print()


    h = [Not(Var("a")), Or(Var("a"), Var("b"))]
    s = Seq(h, f)

    print("___________________________________________")
    print("TEST REGLES DE CALCUL DES TABLEAUX")
    print("___________________________________________")
    print(f"Séquent initial :    {s}")
    print(f"---- Liste des conditions d'applicabilité ----")
    for rule in calculus:
        print(f"  - {rule.rulename:^11} : {rule.appcond([], s)}")
    print(f"---- Liste des actions ----")
    for rule in calculus:
        print(f"  - {rule.rulename:^11} : {get_affichage_liste_sequents(rule.action([], s))}")
    print()


    p, q = Var("p"), Var("q")
    s1 = Seq([Or(Not(p), q), Not(And(p, q)), Not(Not(p)), Not(p)], FF())
    s2 = Seq([Or(Not(p), q), Not(And(p, q)), Not(Not(p)), q], FF())
    ps = [s1, s2]

    print("___________________________________________")
    print("TEST MOTEUR PREUVE")
    print("___________________________________________")
    print(f"Etat de preuve :\n{get_affichage_liste_sequents(ps)}")
    print()
    print(f"---- Liste des états de preuve suivants ----")
    for ps_i in next_proof_state(ps):
        print(get_affichage_liste_sequents(ps_i))
        print()


if __name__ == "__main__":
    main()
