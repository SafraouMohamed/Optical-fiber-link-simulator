import streamlit as st
import plotly.graph_objects as go

from optical_simulator.modules import bilan_liaison, analyse_modale
from optical_simulator.modules import emetteur


st.set_page_config(
    page_title="Simulateur Liaison Optique",
    page_icon="📡",
    layout="wide"
)


def generer_courbe_puissance(P_injectee, alpha, L_cable, A_ep, A_fixe, L_max, n_points=100):
    L_vals = [i * L_max / n_points for i in range(n_points + 1)]
    P_rx = []
    
    for L in L_vals:
        A_fibre = alpha * L
        n_ep = int(L // L_cable)
        A_ep_total = n_ep * A_ep
        A_total = A_fibre + A_ep_total + A_fixe
        P_rx.append(P_injectee - A_total)
    
    return L_vals, P_rx


def afficher_rapport(results, params):
    st.markdown("## 📊 Rapport de Faisabilité")
    
    etat = "✅ FONCTIONNELLE" if results['est_fonctionnelle'] else "❌ NON FONCTIONNELLE"
    st.markdown(f"**État:** {etat}")
    st.markdown("---")
    
    st.markdown("### ⚡ Bilan de Puissance")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Puissance émise (Pe)", f"{params.get('Pe_dBm', 0):.2f} dBm")
        st.metric("Puissance injectée", f"{results['P_injectee_dBm']:.2f} dBm")
    
    with col2:
        st.metric("Puissance reçue (P_rx)", f"{results['P_rx_dBm']:.2f} dBm")
        st.metric("Sensibilité récepteur", f"{params.get('P_min_dBm', -30):.2f} dBm")
    
    marge = results['marge_puissance_dB']
    marge_emoji = "✅" if marge >= 0 else "❌"
    st.metric("Marge de puissance", f"{marge:.2f} dB {marge_emoji}")
    
    detail = results['attenuation_detail']
    st.markdown("#### Détail des pertes")
    for key, val in detail.items():
        st.write(f"- {key}: {val:.2f} dB")
    
    st.markdown("---")
    st.markdown("### 📈 Analyse de Dispersion")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Δτ chromatique", f"{results['delta_tau_ch_ps']:.2f} ps")
    with col2:
        st.metric("Δτ intermodal", f"{results['delta_tau_im_ps']:.2f} ps")
    with col3:
        st.metric("Δτ total", f"{results['delta_tau_total_ps']:.2f} ps")
    
    db_max_gbps = results['Db_max_bps'] / 1e9
    st.metric("Débit binaire maximal", f"{db_max_gbps:.2f} Gbps")
    
    st.markdown("---")
    st.markdown("### 📏 Distances Maximales")
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Distance max (atténuation)", f"{results['L_max_att_km']:.2f} km")
    with col2:
        st.metric("Distance max (dispersion)", f"{results['L_max_disp_km']:.2f} km")
    
    st.metric("Distance max système", f"{results['L_max_systeme_km']:.2f} km")
    st.markdown(f"**Facteur limitant:** {results['facteur_limitant']}")
    
    st.markdown("---")
    st.markdown("### 🔍 Analyse Modale")
    st.metric("Nombre V", f"{results['nombre_V']:.2f}")
    st.metric("Mode", "Monomode" if results['est_mononode'] else "Multimode")


def afficher_graphique(params, results):
    st.markdown("## 📉 Courbe Puissance = f(Distance)")
    
    Pe = params.get('Pe_dBm', 0)
    alpha = params.get('alpha_dB_km', 0.2)
    L_cable = params.get('L_cable_km', 1.0)
    A_ep = params.get('A_ep_dB', 0.3)
    L_max = results['L_max_att_km']
    
    eta_c = params.get('eta_c_dB', -3)
    A_conn = params.get('A_conn_dB', 0.5) * 2
    A_fresnel = 0.6 if not params.get('adapt_index', False) else 0
    A_fixe = A_conn + A_fresnel + abs(eta_c)
    
    P_inj = emetteur.calculer_puissance_injectee(Pe, eta_c)
    L_vals, P_rx = generer_courbe_puissance(P_inj, alpha, L_cable, A_ep, A_fixe, L_max * 1.2)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=L_vals,
        y=P_rx,
        mode='lines',
        name='P_rx(L)',
        line=dict(color='blue', width=2.5)
    ))
    
    P_min = params.get('P_min_dBm', -30)
    fig.add_hline(y=P_min, line_dash="dash", line_color="red", annotation="Seuil P_min")
    
    if params.get('P_sat_dBm'):
        P_sat = params.get('P_sat_dBm')
        fig.add_hline(y=P_sat, line_dash="dash", line_color="orange", annotation="Saturation")
    
    fig.add_vline(x=L_max, line_dash="dash", line_color="green", annotation="L_max")
    
    fig.update_layout(
        xaxis_title="Distance (km)",
        yaxis_title="Puissance reçue (dBm)",
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def main():
    st.title("📡 Simulateur de Liaison Optique")
    st.markdown("**Projet:** BASED ON COURS - PROF. FAOUZI BAHLOUL, ENIT")
    
    st.sidebar.title("📝 Paramètres d'Entrée")
    
    with st.sidebar.expander("💡 Émetteur", expanded=True):
        Pe = st.number_input("Puissance émise (dBm)", value=0.0, step=0.1)
        lambda_nm = st.number_input("Longueur d'onde (nm)", value=1550.0, step=1.0)
        type_source = st.selectbox("Type de source", ["Laser", "LED"])
        
        choix_lambda = st.radio("Largeur spectrale", ["Δλ (nm)", "Δν (GHz)"])
        if choix_lambda == "Δλ (nm)":
            delta_lambda = st.number_input("Δλ (nm)", value=1.0, step=0.1)
            delta_nu = None
        else:
            delta_nu = st.number_input("Δν (GHz)", value=2.48, step=0.1)
            delta_lambda = emetteur.calculer_delta_lambda(delta_nu, lambda_nm) if delta_nu else 1.0
        
        eta_c = st.number_input("Perte couplage ηc (dB)", value=-3.0, step=0.5)
    
    with st.sidebar.expander("🌊 Fibre", expanded=True):
        type_fibre = st.selectbox("Type de fibre", ["SMF", "MMF"])
        profil = st.selectbox("Profil d'indice", ["Saut", "Gradient"])
        
        st.markdown("#### Indices (2 sur 3 requis)")
        choix_indices = st.selectbox(
            "Paramètres fournis", 
            ["n1 et n2", "n1 et Δ", "n1 et NA"]
        )
        
        if choix_indices == "n1 et n2":
            n1 = st.number_input("n1 (cœur)", value=1.485, step=0.001)
            n2 = st.number_input("n2 (gaine)", value=1.470, step=0.001)
        elif choix_indices == "n1 et Δ":
            n1 = st.number_input("n1 (cœur)", value=1.485, step=0.001)
            delta = st.number_input("Δ", value=0.01, step=0.001)
        else:
            n1 = st.number_input("n1 (cœur)", value=1.485, step=0.001)
            na = st.number_input("NA", value=0.21, step=0.01)
        
        a_um = st.number_input("Rayon cœur a (μm)", value=4.0, step=0.5)
        alpha = st.number_input("Atténuation α (dB/km)", value=0.2, step=0.01)
        Dc = st.number_input("Dispersion Dc (ps/nm·km)", value=18.0, step=0.5)
        L = st.number_input("Longueur liaison L (km)", value=50.0, step=1.0)
        
        st.markdown("#### Paramètres optionnels")
        L_cable = st.number_input("Longueur rouleau (km)", value=1.0, step=0.1)
        A_ep = st.number_input("Perte épissure (dB)", value=0.3, step=0.05)
    
    with st.sidebar.expander("📡 Récepteur"):
        P_min = st.number_input("Sensibilité Pmin (dBm)", value=-30.0, step=0.5)
        P_sat = st.number_input("Saturation Psat (dB)", value=None)
        A_conn = st.number_input("Perte connecteur (dB)", value=0.5, step=0.1)
    
    with st.sidebar.expander("⚙️ Système"):
        A_age = st.number_input("Marge vieillissement (dB)", value=0.0, step=0.5)
        A_margin = st.number_input("Marge système (dB)", value=0.0, step=0.5)
        alpha_cut = st.number_input("Marge coupure (dB/km)", value=0.0, step=0.01)
        codage = st.selectbox("Codage", ["NRZ", "RZ"])
        adapt_index = st.checkbox("Adaptation d'indice", value=False)
        
        debit_cible = st.number_input("Débit cible (Gbps)", value=10.0, step=1.0) * 1e9
    
    if st.sidebar.button("🚀 Analyser", type="primary"):
        try:
            indices_input = {}
            if choix_indices == "n1 et n2":
                indices_input = {'n1': n1, 'n2': n2}
            elif choix_indices == "n1 et Δ":
                indices_input = {'n1': n1, 'delta': delta}
            else:
                indices_input = {'n1': n1, 'na': na}
            
            params = {
                'Pe_dBm': Pe,
                'lambda_nm': lambda_nm,
                'type_source': type_source,
                'delta_lambda_nm': delta_lambda,
                'eta_c_dB': eta_c,
                'type_fibre': type_fibre,
                'profil': profil,
                'a_um': a_um,
                'alpha_dB_km': alpha,
                'Dc_ps_nm_km': Dc,
                'L_km': L,
                'P_min_dBm': P_min,
                'P_sat_dBm': P_sat,
                'L_cable_km': L_cable,
                'A_ep_dB': A_ep,
                'A_conn_dB': A_conn,
                'n_conn': 2,
                'A_age_dB': A_age,
                'A_margin_dB': A_margin,
                'alpha_cut_dB_km': alpha_cut,
                'codage': codage,
                'adapt_index': adapt_index,
                'debit_cible_bps': debit_cible,
                **indices_input
            }
            
            results = bilan_liaison.analyser_liaison_complete(params)
            
            coherence = analyse_modale.verifier_coherence_modale(
                type_fibre, results['nombre_V']
            )
            
            if coherence['niveau_alerte'] == 'error':
                st.error(coherence['message'])
            elif coherence['niveau_alerte'] == 'warning':
                st.warning(coherence['message'])
            
            tab1, tab2 = st.tabs(["📊 Rapport", "📉 Graphique"])
            
            with tab1:
                afficher_rapport(results, params)
            
            with tab2:
                afficher_graphique(params, results)
        
        except Exception as e:
            st.error(f"Erreur: {str(e)}")


if __name__ == "__main__":
    main()