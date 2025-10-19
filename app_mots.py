import streamlit as st
import random
import time

# --- CONFIGURATION DE BASE ---
MOTS = ["PYTHON", "PUZZLE", "JEU", "CODE", "ALGORITHME", "PROGRAMME", "CLAVIER", "SOURIS", "ORDINATEUR", "LOGICIEL"]
TEMPS_PAR_MANCHE = 10

# --- INITIALISATION DE LA SESSION ---
if "mot" not in st.session_state:
    st.session_state.score = 0
    st.session_state.manche = 0
    st.session_state.partie_terminee = False
    st.session_state.historique_scores = []
    st.session_state.mot = ""
    st.session_state.melange = ""
    st.session_state.debut = 0.0

# --- TITRE ---
st.title("🧩 Jeu de mots mélangés")
st.caption("Recomposez le mot avant la fin du temps ⏳")

# --- DÉMARRER UNE MANCHE ---
if st.button("▶️ Nouvelle manche"):
    st.session_state.mot = random.choice(MOTS)
    st.session_state.melange = ''.join(random.sample(st.session_state.mot, len(st.session_state.mot)))
    st.session_state.debut = time.time()
    st.session_state.manche += 1
    st.session_state.partie_terminee = False
    st.session_state.temps_restant = TEMPS_PAR_MANCHE

# --- SI UNE MANCHE EST EN COURS ---
if st.session_state.mot and not st.session_state.partie_terminee:
    elapsed = int(time.time() - st.session_state.debut)
    st.session_state.temps_restant = max(0, TEMPS_PAR_MANCHE - elapsed)

    st.subheader(f"Mot mélangé : **{st.session_state.melange}**")
    st.progress((TEMPS_PAR_MANCHE - st.session_state.temps_restant) / TEMPS_PAR_MANCHE)

    reponse = st.text_input("Votre réponse :", key="reponse").upper()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Valider"):
            if reponse == st.session_state.mot:
                st.success("Bravo 🎉 bonne réponse !")
                st.session_state.score += 1
                st.session_state.historique_scores.append(1)
            else:
                st.error(f"Faux ❌. Le mot correct était : **{st.session_state.mot}**")
                st.session_state.historique_scores.append(0)
            st.session_state.partie_terminee = True

    with col2:
        if st.session_state.temps_restant == 0:
            st.warning(f"⏰ Temps écoulé ! Le mot était : **{st.session_state.mot}**")
            st.session_state.historique_scores.append(0)
            st.session_state.partie_terminee = True

# --- AFFICHAGE DU SCORE ---
st.markdown("---")
st.metric(label="Score actuel", value=st.session_state.score)

# --- AFFICHAGE DE L'HISTORIQUE À LA FIN ---
if st.session_state.manche >= 1 and st.session_state.partie_terminee:
    st.markdown("### 🧾 Récapitulatif des manches précédentes :")
    total = len(st.session_state.historique_scores)
    bonnes = sum(st.session_state.historique_scores)
    st.write(f"**Manches jouées :** {total}")
    st.write(f"**Réussites :** {bonnes}")
    st.write(f"**Échecs :** {total - bonnes}")
    st.write(f"**Taux de réussite :** {bonnes/total*100:.1f}%")

# --- REJOUER UNE NOUVELLE PARTIE ---
if st.button("🔄 Rejouer depuis zéro"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
