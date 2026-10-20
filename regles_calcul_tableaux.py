"""
regles_calcul_tableaux.py
Fichier contenant le code des règles du calcul des Tableaux, 4.2
"""

#TODO: justifier le choix des conditions d'applicabilité dans le rapport
from datastructs import FF, Var, Not, Or, And, Impl, Form, Seq, Rule, Calculus


# ---------------------------------------------------------------------------
# Fonctions auxiliaires
# ---------------------------------------------------------------------------

def union_formules(liste_formules1: list[Form], liste_formules2: list[Form]) -> list[Form]:
    """
    Renvoie l'union de 2 listes de formules (liste de formule unique présente dans une liste ou dans l'autre).
    """
    union = []

    for formule in liste_formules1:
        if formule not in union: union.append(formule)

    for formule in liste_formules2:
        if formule not in union: union.append(formule)

    return union

def is_in(a: Form, liste_formules: list[Form]) -> bool:
    """
    Indique si la formule a est dans liste_formules, ou non
    """
    return a in liste_formules

def is_not_in(a: Form, liste_formules: list[Form]) -> bool:
    """
    Indique si la formule a est manquante de liste_formules, ou non
    """
    return not is_in(a, liste_formules)

def both_in(a: Form, b: Form, liste_formules: list[Form]) -> bool:
    """
    Indique si les deux formules (a ou b) sont dans liste_formules, ou non
    """
    return is_in(a, liste_formules) and is_in(b, liste_formules)

def not_both_in(a: Form, b: Form, liste_formules: list[Form]) -> bool:
    """
    Indique si au moins une formule (a ou b) est manquante de liste_formules, ou non
    """
    return not both_in(a, b, liste_formules)

def neither_in(a: Form, b: Form, liste_formules: list[Form]) -> bool:
    """
    Indique si les deux formules (a et b) sont manquantes de liste_formules, ou non
    """
    return is_not_in(a, liste_formules) and is_not_in(b, liste_formules)


# ---------------------------------------------------------------------------
# Conditions d'applicabilité
# ---------------------------------------------------------------------------

####################
#       Start      #
####################

# Start (S)
def s_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([], Seq(_, a)):
            return a != FF()

        case _: return False


####################
#      Axiomes     #
####################

# Axiome F (AxF)
def ax_f_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([], Seq(g, FF())):
            return is_in(FF(), g)

        case _: return False

# Axiome C (AxC)
def ax_c_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([a], Seq(g, FF())):
            return both_in(a, Not(a), g)

        case _: return False


####################
#     Négation     #
####################

# Négation (N)
def n_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return is_not_in(a, g)

        case _: return False


####################
#   Conjonctives   #
####################

# ET conjonctive (α∧)
def a_and_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return not_both_in(a, b, g)

        case _: return False

# OU conjonctive (α∨)
def a_or_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Not(Or(a, b))], Seq(g, FF())):
            return not_both_in(Not(a), Not(b), g)

        case _: return False

# IMPLICATION conjonctive (α→)
def a_impl_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Not(Impl(a, b))], Seq(g, FF())):
            return not_both_in(a, Not(b), g)

        case _: return False


####################
#   Disjonctives   #
####################

# ET disjonctive (β∧)
def b_and_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Not(And(a, b))], Seq(g, FF())):
            return neither_in(Not(a), Not(b), g)

        case _: return False

# OU disjonctive (β∨)
def b_or_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Or(a, b)], Seq(g, FF())):
            return neither_in(a, b, g)

        case _: return False

# IMPLICATION disjonctive (β→)
def b_impl_t_appcond(fs: list[Form], s: Seq) -> bool:
    match (fs, s):
        case ([Impl(a, b)], Seq(g, FF())):
            return neither_in(Not(a), b, g)

        case _: return False


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------

####################
#       Start      #
####################

# Start (S)
def s_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([], Seq(g, a)):
            return [
                Seq(union_formules(g, [Not(a)]), FF())
            ]

        case _: return []


####################
#      Axiomes     #
####################

# Axiome F (AxF)
def ax_f_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([], Seq(_, FF())):
            return [
            ]

        case _: return []

# Axiome C (AxC)
def ax_c_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([_], Seq(_, FF())):
            return [
            ]

        case _: return []


####################
#     Négation     #
####################

# Négation (N)
def n_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Not(Not(a))], Seq(g, FF())):
            return [
                Seq(union_formules(g, [a]), FF())
            ]

        case _: return []


####################
#   Conjonctives   #
####################

# ET conjonctive (α∧)
def a_and_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([And(a, b)], Seq(g, FF())):
            return [
                Seq(union_formules(g, [a, b]), FF())
            ]

        case _: return []

# OU conjonctive (α∨)
def a_or_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Not(Or(a, b))], Seq(g, FF())):
            return [
                Seq(union_formules(g, [Not(a), Not(b)]), FF())
            ]

        case _: return []

# IMPLICATION conjonctive (α→)
def a_impl_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Not(Impl(a, b))], Seq(g, FF())):
            return [
                Seq(union_formules(g, [a, Not(b)]), FF())
            ]

        case _: return []


####################
#   Disjonctives   #
####################

# ET disjonctive (β∧)
def b_and_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Not(And(a, b))], Seq(g, FF())):
            return [
                Seq(union_formules(g, [Not(a)]), FF()),
                Seq(union_formules(g, [Not(b)]), FF())
            ]

        case _: return []

# OU disjonctive (β∨)
def b_or_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Or(a, b)], Seq(g, FF())):
            return [
                Seq(union_formules(g, [a]), FF()),
                Seq(union_formules(g, [b]), FF())
            ]

        case _: return []

# IMPLICATION disjonctive (β→)
def b_impl_t_action(fs: list[Form], s: Seq) -> list[Seq]:
    match (fs, s):
        case ([Impl(a, b)], Seq(g, FF())):
            return [
                Seq(union_formules(g, [Not(a)]), FF()),
                Seq(union_formules(g, [b]), FF())
            ]

        case _: return []


# ---------------------------------------------------------------------------
# Regles
# ---------------------------------------------------------------------------

# Start (S)
s_t_rule = Rule("s_t", s_t_appcond, s_t_action)



# Axiome F (AxF)
ax_f_t_rule = Rule("ax_f_t", ax_f_t_appcond, ax_f_t_action)

# Axiome C (AxC)
ax_c_t_rule = Rule("ax_c_t", ax_c_t_appcond, ax_c_t_action)



# Négation (N)
n_t_rule = Rule("n_t", n_t_appcond, n_t_action)



# ET conjonctive (α∧)
a_and_t_rule = Rule("a_and_t", a_and_t_appcond, a_and_t_action)

# OU conjonctive (α∨)
a_or_t_rule = Rule("a_or_t", a_or_t_appcond, a_or_t_action)

# IMPLICATION conjonctive (α→)
a_impl_t_rule = Rule("a_impl_t", a_impl_t_appcond, a_impl_t_action)



# ET disjonctive (β∧)
b_and_t_rule = Rule("b_and_t", b_and_t_appcond, b_and_t_action)

# OU disjonctive (β∨)
b_or_t_rule = Rule("b_or_t", b_or_t_appcond, b_or_t_action)

# IMPLICATION disjonctive (β→)
b_impl_t_rule = Rule("b_impl_t", b_impl_t_appcond, b_impl_t_action)


# ---------------------------------------------------------------------------
# Calcul
# ---------------------------------------------------------------------------

calculus: Calculus = [
    s_t_rule,

    ax_f_t_rule,
    ax_c_t_rule,

    n_t_rule,

    a_and_t_rule,
    a_or_t_rule,
    a_impl_t_rule,

    b_and_t_rule,
    b_or_t_rule,
    b_impl_t_rule
]
