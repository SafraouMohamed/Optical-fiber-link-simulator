import math
from . import emetteur, fibre, recepteur


def calculer_attenuation_totale(
    A_fibre_dB: float,
    A_epissures_dB: float,
    A_connecteurs_dB: float,
    A_fresnel_dB: float,
    A_couplage_dB: float = 0.0,
    A_age_dB: float = 0.0,
    alpha_cut_dB_km: float = 0.0,
    L_km: float = 0.0,
    A_margin_dB: float = 0.0
) -> dict:
    """
    Calcule l'atténuation totale de la liaison.
    
    Équation (Page 21, 38):
    A_totale = A_fibre + A_épissures + A_connecteurs + A_Fresnel + A_couplage + A_age + α_cut × L + A_margin
    
    Returns:
        Dict avec attenuation_totale_dB et détail par type
    """
    A_cut = alpha_cut_dB_km * L_km
    
    total = (A_fibre_dB + A_epissures_dB + A_connecteurs_dB + A_fresnel_dB + 
            A_couplage_dB + A_age_dB + A_cut + A_margin_dB)
    
    return {
        'attenuation_totale_dB': total,
        'detail': {
            'fibre': A_fibre_dB,
            'epissures': A_epissures_dB,
            'connecteurs': A_connecteurs_dB,
            'fresnel': A_fresnel_dB,
            'couplage': A_couplage_dB,
            'vieillissement': A_age_dB,
            'coupure': A_cut,
            'marge': A_margin_dB
        }
    }


def calculer_puissance_recue(P_injectee_dBm: float, A_totale_dB: float) -> float:
    """
    Calcule la puissance reçue à une distance donnée.
    
    Équation: P_rx(L) = P_injectée - A_totale(L) (Page 21)
    
    Args:
        P_injectee_dBm: Puissance injectée (dBm)
        A_totale_dB: Atténuation totale (dB)
    
    Returns:
        Puissance reçue (dBm)
    """
    return P_injectee_dBm - A_totale_dB


def calculer_budget_optique(Pe_dBm: float, P_min_dBm: float) -> float:
    """
    Calcule le budget optique.
    
    Équation: Budget = Pe - P_min (Page 21)
    
    Args:
        Pe_dBm: Puissance émise (dBm)
        P_min_dBm: Sensibilité (dBm)
    
    Returns:
        Budget optique (dB)
    """
    return Pe_dBm - P_min_dBm


def calculer_distance_max_att(
    P_injectee_dBm: float,
    alpha_dB_km: float,
    L_cable_km: float,
    A_ep_dB: float,
    A_fixe_dB: float,
    P_min_dBm: float,
    tolerance: float = 0.01
) -> float:
    """
    Calcule la distance maximale basée sur l'atténuation.
    
    Résolution de: P_injectée - αL - N_ép(L) × A_ép - A_fixe = P_min
    
    Méthode: Itérative (car N_ép dépend de L)
    
    Returns:
        Distance maximale (km)
    """
    # Estimation linéaire simple
    if alpha_dB_km <= 0:
        return float('inf')
    
    budget = P_injectee_dBm - A_fixe_dB - P_min_dBm
    
    if budget <= 0:
        return 0.0
    
    # Itération simple
    L_max = budget / alpha_dB_km
    for _ in range(100):
        n_ep = int(L_max // L_cable_km)
        A_ep_calc = n_ep * A_ep_dB
        A_total = alpha_dB_km * L_max + A_ep_calc
        P_rx = P_injectee_dBm - A_total
        
        if P_rx < P_min_dBm + tolerance:
            # Réduire la distance
            L_max *= 0.99
        else:
            break
    
    return max(0, L_max)


def calculer_distance_max_disp(
    debit_bps: float,
    Dc_ps_nm_km: float,
    delta_lambda_nm: float,
    type_fibre: str,
    profil: str,
    n1: float,
    delta: float,
    codage: str = 'NRZ'
) -> float:
    """
    Calcule la distance maximale basée sur la dispersion.
    
    Équations (Page 17):
    - SMF: L_max_disp = 0.7 / (Db × Dc × Δλ)
    - MMF: Résolution numérique
    
    Returns:
        Distance maximale (km)
    """
    coef = 0.7 if codage.upper() == 'NRZ' else 0.35
    
    if type_fibre.upper() == 'SMF':
        # Dispersion chromatique seulement
        if Dc_ps_nm_km * delta_lambda_nm <= 0:
            return float('inf')
        L_max = coef / (debit_bps * Dc_ps_nm_km * delta_lambda_nm * 1e-12)
        return L_max
    else:
        # MMF: itération nécessaire pour dispersion intermodale
        L_max = 1000  # max supposé
        for _ in range(100):
            delta_tau_ch = Dc_ps_nm_km * delta_lambda_nm * L_max
            delta_tau_im = fibre.calculer_dispersion_intermodale(
                type_fibre, profil, n1, delta, L_max
            )
            delta_tau_total = fibre.calculer_dispersion_totale(delta_tau_ch, delta_tau_im)
            Db_max = fibre.calculer_debit_maximal(delta_tau_total, codage)
            
            if Db_max >= debit_bps:
                break
            L_max *= 0.9
        
        return L_max


def analyser_liaison_complete(params: dict) -> dict:
    """
    Analyse complète de la liaison - fonction principale d'orchestration.
    
    Args:
        params: Dict containing all input parameters:
            - emetteur: Pe_dBm, lambda_nm, type_source, delta_lambda_nm, eta_c_dB
            - fibre: type_fibre, profil, n1, n2, a_um, alpha_dB_km, Dc_ps_nm_km, L_km
            - recepteur: P_min_dBm, P_sat_dBm (optional)
            - system: A_age_dB, A_margin_dB, alpha_cut_dB_km, codage, adapt_index
    
    Returns:
        Complete analysis results
    """
    # Extraire les paramètres
    Pe = params.get('Pe_dBm', 0)
    lambda_nm = params.get('lambda_nm', 1550)
    type_source = params.get('type_source', 'Laser')
    delta_lambda_nm = params.get('delta_lambda_nm', 1.0)
    eta_c_dB = params.get('eta_c_dB', -3.0)
    
    type_fibre = params.get('type_fibre', 'SMF')
    profil = params.get('profil', 'Saut')
    n1 = params.get('n1', 1.485)
    n2 = params.get('n2', 1.470)
    a_um = params.get('a_um', 4.0)
    alpha_dB_km = params.get('alpha_dB_km', 0.2)
    Dc_ps_nm_km = params.get('Dc_ps_nm_km', 18.0)
    L_km = params.get('L_km', 50.0)
    
    P_min_dBm = params.get('P_min_dBm', -30.0)
    P_sat_dBm = params.get('P_sat_dBm', None)
    
    # Paramètres optionnels
    L_cable_km = params.get('L_cable_km', 1.0)
    A_ep_dB = params.get('A_ep_dB', 0.3)
    A_conn_dB = params.get('A_conn_dB', 0.5)
    n_conn = params.get('n_conn', 2)
    A_age_dB = params.get('A_age_dB', 0.0)
    A_margin_dB = params.get('A_margin_dB', 0.0)
    alpha_cut_dB_km = params.get('alpha_cut_dB_km', 0.0)
    codage = params.get('codage', 'NRZ')
    adapt_index = params.get('adapt_index', False)
    
    # Dérivations des indices
    indices = fibre.deriver_parametres_indices(n1=n1, n2=n2)
    n1 = indices['n1']
    n2 = indices['n2']
    delta = indices['delta']
    na = indices['na']
    
    # Calculs émetteur
    P_injectee = emetteur.calculer_puissance_injectee(Pe, eta_c_dB)
    
    # Calculs fibre
    A_fibre = fibre.calculer_perte_fibre(alpha_dB_km, L_km)
    A_epissures = fibre.calculer_perte_epissures(L_km, L_cable_km, A_ep_dB)
    A_connecteurs = fibre.calculer_perte_connecteurs(n_conn, A_conn_dB)
    A_fresnel = fibre.calculer_perte_fresnel(adapt_index)
    
    # Dispersion
    delta_tau_ch = fibre.calculer_dispersion_chromatique(Dc_ps_nm_km, delta_lambda_nm, L_km)
    delta_tau_im = fibre.calculer_dispersion_intermodale(type_fibre, profil, n1, delta, L_km)
    delta_tau_total = fibre.calculer_dispersion_totale(delta_tau_ch, delta_tau_im)
    
    # Nombre V
    lambda_um = lambda_nm / 1000
    V = fibre.calculer_nombre_V(a_um, lambda_um, na)
    est_mononode = fibre.verifier_mononode(V)
    
    # Débit max
    Db_max = fibre.calculer_debit_maximal(delta_tau_total, codage)
    
    # Atténuation totale
    att = calculer_attenuation_totale(
        A_fibre, A_epissures, A_connecteurs, A_fresnel,
        abs(eta_c_dB), A_age_dB, alpha_cut_dB_km, L_km, A_margin_dB
    )
    A_totale = att['attenuation_totale_dB']
    
    # Puissance reçue
    P_rx = calculer_puissance_recue(P_injectee, A_totale)
    
    # Vérification récepteur
    verif_rx = recepteur.verifier_puissance_recue(P_rx, P_min_dBm, P_sat_dBm)
    
    # Distances max
    A_fixe = A_connecteurs + A_fresnel + A_epissures
    L_max_att = calculer_distance_max_att(
        P_injectee, alpha_dB_km, L_cable_km, A_ep_dB, A_fixe, P_min_dBm
    )
    
    debit_cible = params.get('debit_cible_bps', 10e9)
    L_max_disp = calculer_distance_max_disp(
        debit_cible, Dc_ps_nm_km, delta_lambda_nm, type_fibre, profil, n1, delta, codage
    )
    
    # Facteur limitant
    L_max = min(L_max_att, L_max_disp)
    facteur = 'ATTENUATION' if L_max_att <= L_max_disp else 'DISPERSION'
    
    # Marge dispersion
    marge_disp_pct = 0.0
    if Db_max > 0 and debit_cible > 0:
        marge_disp_pct = (Db_max / debit_cible - 1) * 100
    
    return {
        'est_fonctionnelle': verif_rx['ok'],
        'statut_puissance': verif_rx,
        'P_rx_dBm': P_rx,
        'marge_puissance_dB': verif_rx['marge_dB'],
        'L_max_att_km': L_max_att,
        'L_max_disp_km': L_max_disp,
        'L_max_systeme_km': L_max,
        'facteur_limitant': facteur,
        'Db_max_bps': Db_max,
        'delta_tau_total_ps': delta_tau_total,
        'delta_tau_ch_ps': delta_tau_ch,
        'delta_tau_im_ps': delta_tau_im,
        'nombre_V': V,
        'est_mononode': est_mononode,
        'attenuation_detail': att['detail'],
        'P_injectee_dBm': P_injectee,
        'marge_dispersion_pourcent': marge_disp_pct,
        'indices_derives': indices
    }