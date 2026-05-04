import math


def calculer_puissance_injectee(Pe_dBm: float, eta_c_dB: float) -> float:
    """
    Calcule la puissance injectée dans la fibre.
    
    Équation: P_injectée = Pe + ηc (Page 23, 36)
    
    Args:
        Pe_dBm: Puissance émise en dBm
        eta_c_dB: Perte de couplage en dB (négatif, ex: -17 pour LED, -3 pour Laser)
    
    Returns:
        Puissance injectée en dBm
    """
    return Pe_dBm + eta_c_dB


def dBm_to_mW(P_dBm: float) -> float:
    """Convertit dBm en mW."""
    return 10 ** (P_dBm / 10)


def mW_to_dBm(P_mW: float) -> float:
    """Convertit mW en dBm."""
    if P_mW <= 0:
        return float('-inf')
    return 10 * math.log10(P_mW)


def calculer_delta_lambda(delta_nu_GHz: float, lambda_nm: float) -> float:
    """
    Convertit largeur spectrale en fréquence vers largeur spectrale en longueur d'onde.
    
    Équation: Δλ = λ² × Δν / c
    
    Args:
        delta_nu_GHz: Largeur spectrale en fréquence (GHz)
        lambda_nm: Longueur d'onde centrale (nm)
    
    Returns:
        Largeur spectrale en longueur d'onde (nm)
    """
    lambda_m = lambda_nm * 1e-9
    delta_nu_Hz = delta_nu_GHz * 1e9
    c = 3e8
    delta_lambda = (lambda_m ** 2 * delta_nu_Hz) / c
    return delta_lambda * 1e9


def get_coupling_loss_default(source_type: str) -> float:
    """
    Retourne la perte de couplage par défaut selon le type de source.
    
    Args:
        source_type: 'LED' ou 'Laser'
    
    Returns:
        Perte de couplage en dB (négatif)
    """
    defaults = {
        'LED': -17.0,
        'Laser': -3.0
    }
    return defaults.get(source_type, -3.0)