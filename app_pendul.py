# pendu_avance.py
import streamlit as st
import random
import time

st.set_page_config(page_title="Pendu avancé", page_icon="🪓", layout="centered")
st.title("🪓 Pendu — version avancée (dessin, niveaux, score, minuteur)")

# -----------------------
# Configuration & mots
# -----------------------
WORD_BANK = {
    "Facile": ["CHAT", "MAISON", "SOLEIL", "VOITURE", "ARBRE", "MALE", "EAU", "LUNE"],
    "Moyen": ["PYTHON", "STREAMLIT", "ALGORITHME", "VARIABLE", "FUNCTION", "ORDINATEUR"],
    "Difficile": ["INTELLIGENCE", "CRYPTOGRAPHIE", "DETERMINATION", "SYNCHRONISATION", "PARALLELISME"]
}

HANGMAN_STAGES = [
    """
    
    
    
    
    
    _______
    """,
    """
    
     |
     |
     |
     |
    _|_____
    """,
    """
     ______
     |/
     |
     |
     |
    _|_____
    """,
    """
     ______
     |/   |
     |    O
     |
     |
    _|_____
    """,
    """
     ______
     |/   |
     |    O
     |    |
     |
    _|_____
    """,
    """
     ______
     |/   |
     |    O
     |   /|\\
     |
    _|_____
    """,
    """
     ______
     |/   |
     |    O
     |   /|\\
     |   / \\
    _|_____
    """
]

# -----------------------
# UI : options
# -----------------------
with st.sidebar:
    st.header("Paramètres du jeu")
    niveau = st.selectbox("Niveau", ["Facile", "Moyen", "Difficile"], index=1)
    # Timer per level (seconds)
    default_times = {"Facile": 120, "Moyen": 90, "Difficile": 60}
    timer_seconds = st.number_input(
        "Durée (secondes)", min_value=10, max_value=600, value=default_times[niveau], step=5
    )
    st.write("---")
    st.markdown("**Règles rapides :**")
    st.write("- Propose des lettres (1 lettre) ou devine directement le mot.")
    st.write("- Tu as 6 erreurs autorisées. Le dessin évolue à chaque erreur.")
    st.write("- Le minuteur se déclenche au début de la partie.")
    st.write("---")
    if st.button("Nouvelle partie (sidebar)"):
        st.session_state["force_new"] = True
        st.experimental_rerun()

# -----------------------
# Initialisation session_state
# -----------------------
def new_game(niveau_selected, timer_duration):
    st.session_state.mot_secret = random.choice(WORD_BANK[niveau_selected])
    st.session_state.trouve = ["_" for _ in st.session_state.mot_secret]
    st.session_state.lettres = []
    st.session_state.erreurs = 0
    st.session_state.max_erreurs = 6
    st.session_state.victoires = st.session_state.get("victoires", 0)
    st.session_state.defaites = st.session_state.get("defaites", 0)
    st.session_state.start_time = time.time()
    st.session_state.end_time = time.time() + timer_duration
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.last_action = None  # helpful for UX

if "mot_secret" not in st.session_state or st.session_state.get("force_new", False):
    # start a new game at load or if force_new set
    new_game(niveau, timer_seconds)
    st.session_state.force_new = False

# If user changed level or timer in sidebar we should start a new game
# (we can't detect change event easily, so compare stored level/time)
if st.session_state.get("current_level", None) != niveau or st.session_state.get("current_timer", None) != timer_seconds:
    new_game(niveau, timer_seconds)
    st.session_state.current_level = niveau
    st.session_state.current_timer = timer_seconds

# -----------------------
# Helper functions
# -----------------------
def display_hangman(errors):
    idx = min(errors, len(HANGMAN_STAGES)-1)
    st.code(HANGMAN_STAGES[idx], language=None)

def reveal_word():
    return " ".join(st.session_state.mot_secret)

def end_game(lost=False):
    st.session_state.game_over = True
    if lost:
        st.session_state.defaites = st.session_state.get("defaites", 0) + 1
        st.session_state.message = f"💀 Tu as perdu — le mot était : {st.session_state.mot_secret}"
    else:
        st.session_state.victoires = st.session_state.get("victoires", 0) + 1
        st.session_state.message = f"🎉 Bravo ! Tu as trouvé : {st.session_state.mot_secret}"

# -----------------------
# Main layout
# -----------------------
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mot à deviner")
    st.markdown(" ".join(st.session_state.trouve))

    st.write("")
    # Letters already tried
    st.write("Lettres proposées :", ", ".join(st.session_state.lettres) if st.session_state.lettres else "Aucune")

    # Input pour une lettre
    with st.form(key="letter_form"):
        lettre = st.text_input("Propose une lettre (A-Z) :", max_chars=1, key="letter_input").upper().strip()
        submitted_letter = st.form_submit_button("Valider la lettre")
    if submitted_letter and not st.session_state.game_over:
        st.session_state.last_action = "letter"
        if not lettre or not lettre.isalpha() or len(lettre) != 1:
            st.warning("⚠️ Entre une seule lettre (A-Z).")
        elif lettre in st.session_state.lettres:
            st.info("Tu as déjà essayé cette lettre.")
        else:
            st.session_state.lettres.append(lettre)
            if lettre in st.session_state.mot_secret:
                for i, ch in enumerate(st.session_state.mot_secret):
                    if ch == lettre:
                        st.session_state.trouve[i] = lettre
                st.success("✅ Bonne lettre !")
            else:
                st.session_state.erreurs += 1
                st.error("❌ Mauvaise lettre.")
        st.experimental_rerun()

    # Formulaire pour deviner le mot entier
    with st.form(key="word_form"):
        guess = st.text_input("Ou deviner le mot entier :", key="word_input").upper().strip()
        submitted_word = st.form_submit_button("Deviner le mot")
    if submitted_word and not st.session_state.game_over:
        st.session_state.last_action = "word"
        if not guess.isalpha():
            st.warning("⚠️ Le mot doit contenir uniquement des lettres.")
        else:
            if guess == st.session_state.mot_secret:
                st.session_state.trouve = list(st.session_state.mot_secret)
                end_game(lost=False)
                st.balloons()
            else:
                st.session_state.erreurs += 1
                st.error("❌ Ce n'est pas le bon mot.")
        st.experimental_rerun()

    # Vérifications victoire / défaite
    if not st.session_state.game_over:
        # Timer check
        remaining = int(st.session_state.end_time - time.time())
        if remaining <= 0:
            end_game(lost=True)
        elif "_" not in st.session_state.trouve:
            end_game(lost=False)

    # Afficher message final si partie terminée
    if st.session_state.game_over:
        if st.session_state.message:
            if "Bravo" in st.session_state.message:
                st.success(st.session_state.message)
            else:
                st.error(st.session_state.message)
        st.write("Mot :", reveal_word())
        if st.button("Rejouer", key="replay_main"):
            new_game(niveau, timer_seconds)
            st.experimental_rerun()

with col2:
    st.subheader("État du jeu / Dessin")
    display_hangman(st.session_state.erreurs)
    st.write(f"Erreurs : **{st.session_state.erreurs}** / {st.session_state.max_erreurs}")

    # Timer affichage
    remaining = int(st.session_state.end_time - time.time())
    if remaining > 0 and not st.session_state.game_over:
        minutes = remaining // 60
        seconds = remaining % 60
        st.info(f"⏱️ Temps restant : {minutes:02d}:{seconds:02d}")
    elif st.session_state.game_over:
        st.info("⏱️ Partie terminée.")
    else:
        st.warning("⏱️ Temps écoulé !")

    # Score
    st.write("---")
    st.subheader("Score")
    st.write(f"🏆 Victoires : **{st.session_state.get('victoires', 0)}**")
    st.write(f"💀 Défaites : **{st.session_state.get('defaites', 0)}**")

    # Boutons rapides
    if st.button("Nouvelle partie", key="replay_side"):
        new_game(niveau, timer_seconds)
        st.experimental_rerun()

# -----------------------
# Check loss by errors
# -----------------------
if st.session_state.erreurs >= st.session_state.max_erreurs and not st.session_state.game_over:
    end_game(lost=True)
    st.experimental_rerun()

# -----------------------
# Small UX hints
# -----------------------
if st.session_state.last_action == "letter":
    st.caption("Tip: tu peux aussi deviner le mot entier si tu penses le connaître.")
elif st.session_state.last_action == "word":
    st.caption("Astuce: proposer lettres fréquentes (E, A, I, O, R, S, T) aide souvent.")

# Footer
st.markdown("---")
st.markdown("Développé avec ❤️ — copie ce fichier et lance `streamlit run pendu_avance.py`.")
