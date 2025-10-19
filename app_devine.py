import streamlit as st
import random

# Configuration de la page
st.set_page_config(page_title="Jeu : Devine le nombre", page_icon="🎯")

st.title("🎯 Jeu : Devine le nombre")

# Génération d'un nombre secret (1 à 100)
if "nombre_secret" not in st.session_state:
    st.session_state.nombre_secret = random.randint(1, 100)
    st.session_state.essais = 0

# Entrée utilisateur
proposition = st.number_input("Entre un nombre entre 1 et 100 :", min_value=1, max_value=100, step=1)

# Bouton pour valider
if st.button("Deviner"):
    st.session_state.essais += 1
    if proposition < st.session_state.nombre_secret:
        st.info("🔽 Trop petit ! Essaie encore.")
    elif proposition > st.session_state.nombre_secret:
        st.warning("🔼 Trop grand ! Essaie encore.")
    else:
        st.success(f"🎉 Bravo ! Tu as trouvé le nombre {st.session_state.nombre_secret} en {st.session_state.essais} essais.")
        if st.button("Rejouer"):
            st.session_state.nombre_secret = random.randint(1, 100)
            st.session_state.essais = 0
            st.experimental_rerun()

# Indice facultatif
if st.checkbox("Afficher un indice"):
    if st.session_state.nombre_secret % 2 == 0:
        st.write("💡 Le nombre est pair.")
    else:
        st.write("💡 Le nombre est impair.")
