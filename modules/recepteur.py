def verifier_puissance_recue(P_rx_dBm: float, P_min_dBm: float, 
                              P_sat_dBm: float = None) -> dict:
    """
    Vérifie si la puissance reçue est suffisante.
    
    Logique (Page 21, 35-36):
    - Si P_rx < P_min → ÉCHEC (déficit)
    - Si P_rx > P_sat → ÉCHEC (excès)
    - Sinon → OK
    
    Args:
        P_rx_dBm: Puissance reçue (dBm)
        P_min_dBm: Sensibilité du récepteur (dBm)
        P_sat_dBm: Puissance de saturation (dBm, optionnel)
    
    Returns:
        Dict avec: ok (bool), message (str), marge_dB (float)
    """
    result = {
        'ok': False,
        'message': '',
        'marge_dB': 0.0
    }
    
    if P_sat_dBm is not None and P_rx_dBm > P_sat_dBm:
        deficit = P_rx_dBm - P_sat_dBm
        result['ok'] = False
        result['message'] = f"ÉCHEC: Puissance excède saturation de {deficit:.2f} dB"
        result['marge_dB'] = -deficit
    elif P_rx_dBm < P_min_dBm:
        deficit = P_min_dBm - P_rx_dBm
        result['ok'] = False
        result['message'] = f"ÉCHEC: Déficit de puissance de {deficit:.2f} dB"
        result['marge_dB'] = -deficit
    else:
        marge = P_rx_dBm - P_min_dBm
        result['ok'] = True
        result['message'] = f"OK: Marge de puissance de {marge:.2f} dB"
        result['marge_dB'] = marge
    
    return result


def get_detector_defaults() -> dict:
    """
    Retourne les paramètres par défaut selon le type de détecteur.
    
    Returns:
        Dict avec sensibilité par défaut (dBm)
    """
    return {
        'PIN': -30.0,
        'APD': -35.0
    }