"""
moteur_preuve.py
Fichier gérant l'application des règles et la recherche de preuve basiques, 4.3.1
"""

from datastructs import FF, Var, Not, Or, And, Impl, Form, Seq, Rule, Calculus

ProofStateV0 = list[Seq]
def next_proof_state(ps : ProofStateV0) -> list[ProofStateV0]:
    pass