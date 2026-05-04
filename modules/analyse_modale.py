import math
from . import fibre


def verifier_coherence_modale(type_fibre: str, V: float) -> dict:
    """
    Vérifie la cohérence entre le type de fibre déclaré et le nombre V.
    
    Logique (Page 34):
    - Si SMF et V ≥ 2.405 → ALERTE
    - Si MMF et V < 2.405 → INFO (régime monomode)
    
    Args:
        type_fibre: 'SMF' ou 'MMF'
        V: Nombre V calculé
    
    Returns:
        Dict avec: coherent (bool), message (str), niveau_alerte (str)
    """
    est_mononode = fibre.verifier_mononode(V)
    type_fibre = type_fibre.upper()
    
    result = {
        'coherent': True,
        'message': '',
        'niveau_alerte': 'info'  # 'info', 'warning', 'error'
    }
    
    if type_fibre == 'SMF' and V >= 2.405:
        result['coherent'] = False
        result['message'] = f"ALERTE: Fibre déclarée monomode mais V = {V:.2f} ≥ 2.405"
        result['niveau_alerte'] = 'error'
    elif type_fibre == 'MMF' and est_mononode:
        result['coherent'] = True
        result['message'] = f"INFO: Fibre multimode mais V = {V:.2f} < 2.405 (régime monomode)"
        result['niveau_alerte'] = 'info'
    
    return result