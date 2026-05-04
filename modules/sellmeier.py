import math


SELLMEIER_CONSTANTS = {
    'A0': 0.6961663,
    'A1': 0.4079426,
    'A2': 0.8974794,
    'lambda0': 6.84043e-8,  # m
    'lambda1': 1.162414e-7,  # m
    'lambda2': 9.896161e-6   # m
}


def calculer_indice_sellmeier(lambda_um: float) -> float:
    """
    Calcule l'indice de réfraction via Sellmeier.
    
    Équation (Page 14):
    n²(λ) = 1 + A₀λ²/(λ²-λ₀²) + A₁λ²/(λ²-λ₁²) + A₂λ²/(λ²-λ₂²)
    
    Args:
        lambda_um: Longueur d'onde (μm)
    
    Returns:
        Indice de réfraction n(λ)
    """
    lambda_m = lambda_um * 1e-6
    lambda2 = lambda_m ** 2
    
    A0 = SELLMEIER_CONSTANTS['A0']
    A1 = SELLMEIER_CONSTANTS['A1']
    A2 = SELLMEIER_CONSTANTS['A2']
    lambda0 = SELLMEIER_CONSTANTS['lambda0']
    lambda1 = SELLMEIER_CONSTANTS['lambda1']
    lambda2 = SELLMEIER_CONSTANTS['lambda2']
    
    term0 = A0 * lambda2 / (lambda2 - lambda0**2)
    term1 = A1 * lambda2 / (lambda2 - lambda1**2)
    term2 = A2 * lambda2 / (lambda2 - lambda2**2)
    
    n2 = 1 + term0 + term1 + term2
    
    return math.sqrt(n2)


def calculer_dispersion_sellmeier(lambda_um_1: float, lambda_um_2: float, L_km: float = 1.0) -> float:
    """
    Calcule la dispersion chromatique via Sellmeier.
    
    Utilise n(λ) à deux longueurs d'onde pour estimer Dc.
    
    Args:
        lambda_um_1: Première longueur d'onde (μm)
        lambda_um_2: Deuxième longueur d'onde (μm)
        L_km: Longueur (km)
    
    Returns:
        Dispersion chromatique (ps/nm·km) approximée
    """
    n1 = calculer_indice_sellmeier(lambda_um_1)
    n2 = calculer_indice_sellmeier(lambda_um_2)
    
    delta_lambda = abs(lambda_um_2 - lambda_um_1) * 1000  # nm
    c = 3e5  # km/s
    
    dn = abs(n2 - n1)
    D = (dn / delta_lambda) * 1e12 / c
    
    return D * 1000  # ps/nm·km approximé