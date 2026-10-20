"""
test_formules.py
Fichier contenant les fonctions sur les formules, 4.1
"""

from datastructs import FF, Var, Not, And, Or, Impl, Form, Seq

def nb_feuilles(f:Form) -> int:
    match f:
        case Var(_) | FF():
            return 1
        case Impl(a,b) | Or(a,b) | And(a,b):
            return nb_feuilles(a) + nb_feuilles(b)
        case Not(a):
            return nb_feuilles(a)

def liste_var(f:Form) -> list :
    match f:
        case Var(a):
            return [a]
        case FF():
            return []
        case Not(a):
            return liste_var(a)
        case Impl(a,b) | Or(a,b) | And(a,b):
            return liste_var(a) + liste_var(b)

def negative(f:Form) -> Form :
    match f:
        case Var(_) | FF():
            return f
        case Not(Not(a)):
            return negative(a)
        case Not(FF()):
            return Not(FF())
        case Not(Impl(a,b)):
            return And(negative(a), negative(Not(b)))
        case Not(And(a,b)):
            return Or(negative(Not(a)), negative(Not(b)))
        case Not(Or(a,b)):
            return And(negative(Not(a)), negative(Not(b)))
        case Impl(a,b):
            return Or(negative(Not(a)), negative(b))
        case And(a,b):
            return And(negative(a), negative(b))
        case Or(a,b):
            return Or(negative(a), negative(b))
        case Not(Var(_)):
            return f