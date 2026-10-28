"""
main.py
Fichier de test et d'exécution des fonctions
"""

from datastructs import Var, FF, And, Not, Or, Impl, Form, Seq, OpenGoal, ProofState
from test_formules import nb_feuilles, liste_var, negative
from regles_calcul_tableaux import calculus
from moteur_preuve import next_proof_state_v0, next_proof_state
from recherche_preuve import prove_seq_v0, prove_seq


# ---------------------------------------------------------------------------
# Fonctions auxiliaires
# ---------------------------------------------------------------------------

def get_affichage_liste_formules(liste_formules: list[Form]) -> str:
    """
    Renvoie l'affichage formaté d'une liste de formules
    """
    affichage = "["
    for i in range(len(liste_formules)):
        formule = liste_formules[i]

        affichage += str(formule)
        if i < len(liste_formules) - 1:
            affichage += " ,"

    affichage += "]"
    return affichage

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

def get_affichage_proof_state(proof_state: ProofState) -> str:
    """
    Renvoie l'affichage formaté d'un état de preuves
    """
    affichage = ""
    open_goals, closed_goals = proof_state

    affichage += "Liste des buts fermés :\n"
    for i in range(len(closed_goals)):
        closed_goal = closed_goals[i]

        affichage += f"But fermé {i} -\n"
        affichage += f"    historique   : {closed_goal.history}\n"
        affichage += f"    séquent      : {closed_goal.seq}\n"
        affichage += f"    nom de règle : {closed_goal.rulename}\n"
        affichage += f"    formules     : {get_affichage_liste_formules(closed_goal.forms)}\n"
        affichage += "\n"
    affichage += "\n"

    affichage += "Liste des buts ouverts :\n"
    for i in range(len(open_goals)):
        open_goal = open_goals[i]

        affichage += f"But ouvert {i} -\n"
        affichage += f"    historique   : {open_goal.history}\n"
        affichage += f"    séquent      : {open_goal.seq}\n"
        affichage += "\n"

    return affichage

def get_affichage_liste_proof_states(liste_proof_states: list[ProofState]) -> str:
    """
    Renvoie l'affichage formaté d'une liste d'états de preuves
    """
    affichage = ""

    for i in range(len(liste_proof_states)):
        proof_state = liste_proof_states[i]

        affichage += f"-- état de preuve {i} --\n"
        affichage += get_affichage_proof_state(proof_state)
        affichage += "\n"

    return affichage


# ---------------------------------------------------------------------------
# Fonction 'main' de tests
# ---------------------------------------------------------------------------

def main():
    f = Impl(And(Var("a"), FF()), Not(Var("b")))

    print("###########################################")
    print("TEST MANIPULATION DE FORMULES")
    print("###########################################")
    print(f"Formule initiale    : {f}")
    print(f"Nombre de feuilles  : {nb_feuilles(f)}")
    print(f"Liste des variables : {liste_var(f)}")
    print(f"Forme Négative      : {negative(f)}")
    print()
    print(f"Formule initiale    : {f}")
    print()


    h = [Not(Var("a")), Or(Var("a"), Var("b"))]
    s = Seq(h, f)

    print("###########################################")
    print("TEST REGLES DE CALCUL DES TABLEAUX")
    print("###########################################")
    print(f"Séquent initial :    {s}")
    print(f"---- Liste des conditions d'applicabilité ----")
    for rule in calculus:
        print(f"  - {rule.rulename:^11} : {rule.appcond([], s)}")
    print(f"----------------------------------------------")
    print(f"---- Liste des actions ----")
    for rule in calculus:
        print(f"  - {rule.rulename:^11} : {get_affichage_liste_sequents(rule.action([], s))}")
    print(f"---------------------------")
    print()
    print(f"Séquent initial :    {s}")
    print()


    p, q = Var("p"), Var("q")
    s1 = Seq([Or(Not(p), q), Not(And(p, q)), Not(Not(p)), Not(p)], FF())
    s2 = Seq([Or(Not(p), q), Not(And(p, q)), Not(Not(p)), q], FF())
    ps_v0 = [s1, s2]

    print("###########################################")
    print("TEST MOTEUR DE PREUVE — version basique (V0)")
    print("###########################################")
    print(f"Etat de preuve :\n{get_affichage_liste_sequents(ps_v0)}")
    print()
    print(f"---- Liste des états de preuve suivants ----")
    for ps_i in next_proof_state_v0(ps_v0):
        print(get_affichage_liste_sequents(ps_i))
        print()
    print(f"--------------------------------------------")
    print()
    print(f"Etat de preuve :\n{get_affichage_liste_sequents(ps_v0)}")
    print()


    print("###########################################")
    print("TEST RECHERCHE DE PREUVE — version basique (V0)")
    print("###########################################")
    print(f"Séquent à prouver     :    {s}")
    print(f"Résultat de la preuve :    {prove_seq_v0(s)}")
    print()
    print(f"Séquent à prouver     :    {s}")
    print()


    open_goal_1 = OpenGoal([1], s1)
    open_goal_2 = OpenGoal([2], s2)
    open_goals = [open_goal_1, open_goal_2]
    closed_goals = []
    ps = open_goals, closed_goals

    print("###########################################")
    print("TEST MOTEUR DE PREUVE — version raffinée")
    print("###########################################")
    print(f"-- etat de preuve --")
    print(get_affichage_proof_state(ps))
    print()
    print(f"---- Liste des états de preuve suivants ----")
    liste_next_proof_states = next_proof_state(ps)
    print(get_affichage_liste_proof_states(liste_next_proof_states))
    print(f"--------------------------------------------")
    print()
    print(f"-- etat de preuve --")
    print(get_affichage_proof_state(ps))
    print()


    print("###########################################")
    print("TEST RECHERCHE DE PREUVE — version raffinée")
    print("###########################################")
    print(f"Séquent à prouver     :    {s}")
    print(f"---- Résultat de la preuve ----")
    resultat = prove_seq(s)
    print(get_affichage_liste_proof_states(resultat))
    print(f"-------------------------------")
    print()
    print(f"Séquent à prouver     :    {s}")
    print()


if __name__ == "__main__":
    main()
