"""
test_formules.py
Fichier contenant les fonctions sur les formules, 4.1
"""

from datastructs import FF, Var, Not, And, Or, Impl, Form


def nb_feuilles(f:Form) -> int:
    match f:
        case Not(a):
            return nb_feuilles(a)
        case Or(a,b) | And(a,b) | Impl(a,b):
            return nb_feuilles(a) + nb_feuilles(b)

        case _: return 1

def liste_var(f:Form) -> list :
    match f:
        case Var(a):
            return [a]
        case Not(a):
            return liste_var(a)
        case Or(a,b) | And(a,b) | Impl(a,b):
            return liste_var(a) + liste_var(b)

        case _: return []

def negative(f:Form) -> Form:
    match f:
        case Not(Not(a)):
            return negative(a)
        case Not(Or(a, b)):
            return And(negative(Not(a)), negative(Not(b)))
        case Not(And(a, b)):
            return Or(negative(Not(a)), negative(Not(b)))
        case Not(Impl(a, b)):
            return And(negative(a), negative(Not(b)))

        case Or(a, b):
            return Or(negative(a), negative(b))
        case And(a, b):
            return And(negative(a), negative(b))
        case Impl(a, b):
            return Or(negative(Not(a)), negative(b))

        case _: return f
