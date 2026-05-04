import math


def calculer_delta(n1: float, n2: float) -> float:
    """
    Calcule la différence relative d'indice.
    
    Équation: Δ = (n1 - n2) / n1 (Page 4)
    
    Args:
        n1: Indice du cœur
        n2: Indice de la gaine
    
    Returns:
        Différence relative Δ
    """
    return (n1 - n2) / n1


def calculer_na(n1: float, n2: float) -> float:
    """
    Calcule l'ouverture numérique.
    
    Équation: NA = n1√(2Δ) = √(n1² - n2²) (Page 4)
    
    Args:
        n1: Indice du cœur
        n2: Indice de la gaine
    
    Returns:
        Ouverture numérique NA
    """
    return math.sqrt(n1**2 - n2**2)


def calculer_na_from_delta(n1: float, delta: float) -> float:
    """
    Calcule NA depuis Δ.
    
    Équation: NA = n1√(2Δ)
    """
    return n1 * math.sqrt(2 * delta)


def calculer_n2(n1: float, delta: float) -> float:
    """
    Calcule n2 depuis n1 et Δ.
    
    Équation: n2 = n1(1 - Δ)
    """
    return n1 * (1 - delta)


def calculer_delta_from_na(n1: float, na: float) -> float:
    """
    Calcule Δ depuis NA.
    
    Équation: Δ = (NA / n1)² / 2
    """
    return (na / n1) ** 2 / 2


def calculer_n2_from_na(n1: float, na: float) -> float:
    """
    Calcule n2 depuis n1 et NA.
    
    Équation: n2 = √(n1² - NA²)
    """
    return math.sqrt(n1**2 - na**2)


def deriver_parametres_indices(n1: float = None, n2: float = None, 
                              delta: float = None, na: float = None) -> dict:
    """
    Dérive les paramètres d'indice manquants.
    
    L'utilisateur doit fournir 2 parmi 4: (n1, n2, Δ, NA)
    
    Returns:
        Dict avec n1, n2, delta, NA
    """
    provided = sum(x is not None for x in [n1, n2, delta, na])
    
    if provided < 2:
        raise ValueError("Paramètres insuffisants: fournir au moins 2 parmi n1, n2, δ, NA")
    
    if n1 is not None and n2 is not None:
        delta = delta or calculer_delta(n1, n2)
        na = na or calculer_na(n1, n2)
    elif n1 is not None and delta is not None:
        n2 = n2 or calculer_n2(n1, delta)
        na = na or calculer_na_from_delta(n1, delta)
    elif n1 is not None and na is not None:
        delta = delta or calculer_delta_from_na(n1, na)
        n2 = n2 or calculer_n2_from_na(n1, na)
    elif n2 is not None and delta is not None:
        n1 = n1 or n2 / (1 - delta)
        na = na or calculer_na_from_delta(n1, delta)
    elif n2 is not None and na is not None:
        # n1² = n2² + NA² → pas assez d'info
        raise ValueError("Impossible de dériver n1 sans δ")
    elif delta is not None and na is not None:
        # n1 = NA / √(2δ)
        n1 = n1 or na / math.sqrt(2 * delta)
        n2 = n2 or calculer_n2(n1, delta)
    
    return {'n1': n1, 'n2': n2, 'delta': delta, 'na': na}


def calculer_perte_fibre(alpha_dB_km: float, L_km: float) -> float:
    """
    Calcule l'atténuation de la fibre.
    
    Équation: A_fibre = α × L (Page 11)
    
    Args:
        alpha_dB_km: Atténuation linéique (dB/km)
        L_km: Longueur de la liaison (km)
    
    Returns:
        Atténuation en dB
    """
    return alpha_dB_km * L_km


def calculer_perte_epissures(L_km: float, L_cable_km: float = 1.0, A_ep_dB: float = 0.3) -> float:
    """
    Calcule les pertes dûes aux épissures.
    
    Équation: N_ép = ⌊L / L_câble⌋, A_épissures = N_ép × A_ép (Page 21, 40)
    
    Args:
        L_km: Longueur totale (km)
        L_cable_km: Longueur par rouleau (km, défaut 1)
        A_ep_dB: Perte par épissure (dB, défaut 0.3)
    
    Returns:
        Atténuation due aux épissures (dB)
    """
    n_ep = int(L_km // L_cable_km)
    return n_ep * A_ep_dB


def calculer_nombre_epissures(L_km: float, L_cable_km: float = 1.0) -> int:
    """Calcule le nombre d'épissures."""
    return int(L_km // L_cable_km)


def calculer_perte_connecteurs(n_conn: int = 2, A_conn_dB: float = 0.5) -> float:
    """
    Calcule les pertes des connecteurs.
    
    Équation: A_connecteurs = N_conn × 0.5 (Page 21)
    
    Args:
        n_conn: Nombre de connecteurs (défaut 2: entrée + sortie)
        A_conn_dB: Perte par connecteur (dB, défaut 0.5)
    
    Returns:
        Attribution due aux connecteurs (dB)
    """
    return n_conn * A_conn_dB


def calculer_perte_fresnel(adapt_index: bool = False) -> float:
    """
    Calcule la perte Fresnel aux jonctions.
    
    Équation: A_Fresnel = 0.6 dB (sans adaptation), ≈ 0 (avec adaptation) (Page 19)
    
    Args:
        adapt_index: Si True, adaptation d'indice effectuée
    
    Returns:
        Perte Fresnel (dB)
    """
    return 0.0 if adapt_index else 0.6


def calculer_dispersion_chromatique(Dc_ps_nm_km: float, delta_lambda_nm: float, L_km: float) -> float:
    """
    Calcule l'élargissement chromatique.
    
    Équation: Δτ_ch = Dc × Δλ × L (Page 14)
    
    Args:
        Dc_ps_nm_km: Dispersion chromatique (ps/nm·km)
        delta_lambda_nm: Largeur spectrale (nm)
        L_km: Longueur (km)
    
    Returns:
        Élargissement en picosecondes
    """
    return Dc_ps_nm_km * delta_lambda_nm * L_km


def calculer_dispersion_intermodale(type_fibre: str, profil: str, 
                                     n1: float, delta: float, L_km: float) -> float:
    """
    Calcule l'élargissement intermodal.
    
    Équations (Page 17):
    - Saut d'indice: Δτ_im = (n1 / c) × Δ × L
    - Gradient d'indice: Δτ_im = (n1 / 8c) × Δ² × L
    - Monomode: Δτ_im = 0
    
    Args:
        type_fibre: 'SMF' ou 'MMF'
        profil: 'Saut' ou 'Gradient'
        n1: Indice du cœur
        delta: Différence relative Δ
        L_km: Longueur (km)
    
    Returns:
        Élargissement intermodal en picosecondes
    """
    if type_fibre.upper() == 'SMF':
        return 0.0
    
    c = 3e5  # km/s → 3e5 km/s
    L_m = L_km * 1000  # convertir en mètres
    
    if profil.capitalize() == 'Saut':
        delta_tau = (n1 / c) * delta * L_m
    else:  # Gradient
        delta_tau = (n1 / (8 * c)) * (delta ** 2) * L_m
    
    return delta_tau * 1e12  # convertir en ps


def calculer_dispersion_totale(delta_tau_ch_ps: float, delta_tau_im_ps: float) -> float:
    """
    Calcule la dispersion totale (quadratique).
    
    Équation: Δτ_total = √(Δτ_ch² + Δτ_im²) (Page 17)
    
    Args:
        delta_tau_ch_ps: Élargissement chromatique (ps)
        delta_tau_im_ps: Élargissement intermodal (ps)
    
    Returns:
        Dispersion totale (ps)
    """
    return math.sqrt(delta_tau_ch_ps**2 + delta_tau_im_ps**2)


def calculer_debit_maximal(delta_tau_total_ps: float, codage: str = 'NRZ') -> float:
    """
    Calcule le débit binaire maximal.
    
    Équation: Db_max = 0.7 / Δτ_total (Page 17, NRZ)
    
    Args:
        delta_tau_total_ps: Dispersion totale (ps)
        codage: 'NRZ' ou 'RZ'
    
    Returns:
        Débit maximal en bps
    """
    if delta_tau_total_ps <= 0:
        return float('inf')
    
    coef = 0.7 if codage.upper() == 'NRZ' else 0.35
    return coef / (delta_tau_total_ps * 1e-12)


def calculer_nombre_V(a_um: float, lambda_um: float, na: float) -> float:
    """
    Calcule le nombre V (fréquence normalisée).
    
    Équation: V = (2πa / λ) × NA (Page 34)
    
    Args:
        a_um: Rayon du cœur (μm)
        lambda_um: Longueur d'onde (μm)
        na: Ouverture numérique
    
    Returns:
        Nombre V (sans unité)
    """
    return (2 * math.pi * a_um / lambda_um) * na


def verifier_mononode(V: float) -> bool:
    """
    Vérifie si la fibre est monomode.
    
    Condition: V < 2.405 (Page 34)
    
    Args:
        V: Nombre V
    
    Returns:
        True si monomode, False sinon
    """
    return V < 2.405