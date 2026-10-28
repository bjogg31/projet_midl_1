"""
recherche_preuve.py
Fichier gérant la recherche de preuve de manière récursive sur un état de preuve donné, 4.4
"""

from typing import Callable, TypeVar
from datastructs import Seq, ProofStateV0, ProofState, OpenGoal
from moteur_preuve import next_proof_state_v0, next_proof_state


# ---------------------------------------------------------------------------
# Algorithme 'Depth First Search (DPS)'
# ---------------------------------------------------------------------------

PS = TypeVar("PS")

def dfs (get_next_states_function: Callable[[PS], list[PS]],
         is_state_solution: Callable[[PS], bool],
         liste_states: list[PS]) -> list[PS]:

    if len(liste_states) == 0:
        return []

    else:
        if is_state_solution(liste_states[0]):
            return [liste_states[0]]
            # si vous souhaitez continuer la recherche, décommentez :
            # return [liste_states[0]] + dfs (get_next_states_function,
            #                                 is_state_solution,
            #                                 get_next_states_function(liste_states[0]) + liste_states[1:])

        else:
            return dfs (get_next_states_function,
                        is_state_solution,
                        get_next_states_function(liste_states[0]) + liste_states[1:])


# ---------------------------------------------------------------------------
# Recherche de preuve — version basique (V0)
# ---------------------------------------------------------------------------

def sol_proof_state_v0(proof_state: ProofStateV0) -> bool:
    """
    Indique si un état de preuve (V0) est résolu
    """
    return len(proof_state) == 0

def init_state_v0(sequent: Seq) -> list[ProofStateV0]:
    """
    Renvoie la liste d'états de preuve (V0) de départ pour un séquent donné
    """
    return [[sequent]]

def prove_seq_v0(sq: Seq) -> list[ProofStateV0]:
    return dfs(next_proof_state_v0,
               sol_proof_state_v0,
               init_state_v0(sq))


# ---------------------------------------------------------------------------
# Recherche de preuve — version raffinée
# ---------------------------------------------------------------------------

def sol_proof_state(proof_state: ProofState) -> bool:
    """
    Indique si un état de preuve est résolu
    """
    open_goals, _ = proof_state
    return len(open_goals) == 0

def init_state(sequent: Seq) -> list[ProofState]:
    """
    Renvoie la liste d'états de preuve de départ pour un séquent donné
    """
    open_goals = [OpenGoal([], sequent)]
    closed_goals = []

    proof_state = open_goals, closed_goals
    return [proof_state]

def prove_seq(sq: Seq) -> list[ProofState]:
    return dfs(next_proof_state,
               sol_proof_state,
               init_state(sq))

