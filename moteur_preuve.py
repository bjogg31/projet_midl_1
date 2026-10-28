"""
moteur_preuve.py
Fichier gérant l'application des règles et la recherche de preuve basiques, 4.3.1
"""

from datastructs import Form, Seq, Rule, ProofStateV0, OpenGoal, ClosedGoal, ProofState
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

def application_sur_ieme(proof_state: ProofStateV0,
                         rule: Rule,
                         i: int,
                         fs: list[Form]) -> ProofStateV0:
    """
    Renvoie l'état de preuve (V0) après application de 'rule' sur le i-ème séquent de 'proof_state' aux formules 'fs'
    """
    sequent = proof_state[i]
    new_sequents = rule.action(fs, sequent)

    return proof_state[:i] + new_sequents + proof_state[i+1:]


def get_proof_state_from_rule(proof_state: ProofState,
                              rule: Rule,
                              open_goal_index: int,
                              fs: list[Form]) -> ProofState:
    """
    Renvoie l'état de preuve après application de 'rule' sur le séquent, d'indice 'open_goal_index',
    de 'proof_state' aux formules 'fs'
    """
    open_goals, closed_goals = proof_state

    current_open_goal = open_goals[open_goal_index]

    current_history = current_open_goal.history
    current_sequent = current_open_goal.seq

    new_sequents = rule.action(fs, current_sequent)

    open_goals_to_add = [OpenGoal(current_history + [k],
                                  new_sequents[k])
                         for k in range(len(new_sequents))]
    closed_goal_to_add = ClosedGoal(current_history,
                                    current_sequent,
                                    rule.rulename,
                                    fs)

    new_open_goals = open_goals[:open_goal_index] + open_goals_to_add + open_goals[open_goal_index+1:]
    new_closed_goals = closed_goals + [closed_goal_to_add]

    new_proof_state = new_open_goals, new_closed_goals
    return new_proof_state


# ---------------------------------------------------------------------------
# Moteurs de preuve
# ---------------------------------------------------------------------------

def next_proof_state_v0(ps: ProofStateV0) -> list[ProofStateV0]:
    liste_proof_states = []

    for i in range(len(ps)):
        sequent = ps[i]

        for fs in get_liste_fs(sequent):
            for rule in calculus:

                if rule.appcond(fs, sequent):
                    liste_proof_states.append(application_sur_ieme(ps, rule, i, fs))

    return liste_proof_states


def next_proof_state(ps: ProofState) -> list[ProofState]:
    open_goals, _ = ps
    liste_proof_states = []

    for open_goal_index in range(len(open_goals)):
        sequent = open_goals[open_goal_index].seq

        for fs in get_liste_fs(sequent):
            for rule in calculus:

                if rule.appcond(fs, sequent):

                    new_state = get_proof_state_from_rule(ps, rule, open_goal_index, fs)
                    liste_proof_states.append(new_state)

    return liste_proof_states
