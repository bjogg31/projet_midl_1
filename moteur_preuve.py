"""
moteur_preuve.py
Fichier gérant l'application des règles et la recherche de preuve basiques, 4.3.1
"""

from datastructs import Form, Seq, Rule, ProofStateV0
from regles_calcul_tableaux import calculus


# ---------------------------------------------------------------------------
# Fonctions auxiliaires
# ---------------------------------------------------------------------------

def get_liste_fs(sequent: Seq) -> list[list[Form]]:
    """
    Renvoie la liste des fs utiles d'un séquent donné
    """
    liste_fs = [[]]
    for formule in sequent.hyps: liste_fs.append([formule])
    return liste_fs

def application_sur_ieme(proof_state: ProofStateV0, i: int, rule: Rule, fs: list[Form]) -> ProofStateV0:
    """
    Renvoie l'état de preuve après application de 'rule' sur le i-ème séquent de 'proof_state' aux formules 'fs'
    """
    sequent = proof_state[i]
    new_sequents = rule.action(fs, sequent)

    new_proof_state = proof_state.copy()
    new_proof_state.pop(i)

    return new_proof_state[:i] + new_sequents + new_proof_state[i:]


# ---------------------------------------------------------------------------
# Moteur de preuve
# ---------------------------------------------------------------------------

def next_proof_state(ps : ProofStateV0) -> list[ProofStateV0]:
    liste_proof_states = []

    for i in range(len(ps)):
        sequent = ps[i]

        for fs in get_liste_fs(sequent):
            for rule in calculus:

                if rule.appcond(fs, sequent):
                    liste_proof_states.append(application_sur_ieme(ps, i, rule, fs))

    return liste_proof_states
