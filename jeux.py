# multi_jeux_streamlit.py
import streamlit as st
import random
import time
import pandas as pd

st.set_page_config(page_title="🎮 Centre de mini-jeux", page_icon="🎯", layout="centered")

# -----------------------
# Styles (couleurs + animation)
# -----------------------
st.markdown(
    """
    <style>
    /* Animated gradient background */
    @keyframes gradientBG {
      0% {background-position: 0% 50%;}
      50% {background-position: 100% 50%;}
      100% {background-position: 0% 50%;}
    }
    .stApp {
      background: linear-gradient(120deg, #FFD6E0, #FFF6BF, #D6FFEF, #D3E0FF);
      background-size: 400% 400%;
      animation: gradientBG 12s ease infinite;
      font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }
    .title {
      font-weight: 700;
      color: #222;
    }
    .big-btn .stButton>button {
      background: linear-gradient(90deg,#ff8a00,#e52e71);
      color: white;
      border-radius: 10px;
      padding: 10px 18px;
      font-size: 16px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    }
    .big-btn .stButton>button:hover {
      filter: brightness(0.95);
    }
    .card {
      background: rgba(255,255,255,0.85);
      border-radius: 12px;
      padding: 12px;
      box-shadow: 0 6px 18px rgba(0,0,0,0.08);
    }
    .small {
      font-size: 13px;
      color: #333;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------
# Utilities & Data
# -----------------------
PUZZLE_WORDS = [
    "PYTHON", "PUZZLE", "JEU", "CODE", "ALGO",
    "ORDINATEUR", "PROGRAMME", "CONSOLE", "VARIABLE", "FONCTION",
    "ALGORITHME", "INFORMATIQUE", "DEVELOPPEMENT"
]

QUIZ_QS = {
    "Quelle est la capitale du Maroc ?": "RABAT",
    "Combien font 7 + 6 ?": "13",
    "Langage utilisé pour Streamlit ?": "PYTHON",
    "La planète rouge ?": "MARS",
    "Combien font 9 × 9 ?": "81"
}

# Init session state
if "page" not in st.session_state:
    st.session_state.page = "Accueil"
if "scores" not in st.session_state:
    # store per-game session scores and history of rounds
    st.session_state.scores = {"puzzle": 0, "multiplication": 0, "quiz": 0}
    st.session_state.history = {"puzzle": [], "multiplication": [], "quiz": []}
if "puzzle" not in st.session_state:
    st.session_state.puzzle = {}
if "mult" not in st.session_state:
    st.session_state.mult = {}
if "quiz" not in st.session_state:
    st.session_state.quiz = {}

# -----------------------
# Page UI (sidebar menu)
# -----------------------
st.title("🎮 Centre de mini-jeux")
st.markdown("**Choisis un jeu et amuse-toi — scores stockés pour la session seulement.**")

with st.sidebar:
    st.markdown("## 🕹️ Menu")
    st.session_state.page = st.radio(
        "Sélectionner",
        ("Accueil", "🧩 Puzzle de mots", "✖️ Multiplication", "🧠 Quiz"),
        index=("Accueil", "🧩 Puzzle de mots", "✖️ Multiplication", "🧠 Quiz").index(st.session_state.page)
    )
    st.markdown("---")
    st.markdown("**Scores session**")
    st.write(f"Puzzle: {st.session_state.scores['puzzle']}  |  Mult: {st.session_state.scores['multiplication']}  |  Quiz: {st.session_state.scores['quiz']}")
    st.markdown("---")
    if st.button("🔄 Réinitialiser scores (session)"):
        st.session_state.scores = {"puzzle": 0, "multiplication": 0, "quiz": 0}
        st.session_state.history = {"puzzle": [], "multiplication": [], "quiz": []}
        st.experimental_rerun()

# -----------------------
# Game implementations
# -----------------------
def jeu_puzzle():
    st.header("🧩 Puzzle de mots")
    st.markdown("Recompose le mot mélangé avant la fin du temps (optionnel).")
    if "word" not in st.session_state.puzzle or st.button("🔀 Nouveau mot", key="puzz_new"):
        w = random.choice(PUZZLE_WORDS)
        st.session_state.puzzle["word"] = w
        st.session_state.puzzle["shuffled"] = " ".join(random.sample(list(w), len(w)))
        st.session_state.puzzle["start"] = time.time()
        st.session_state.puzzle["time_limit"] = 15
        st.session_state.puzzle["answered"] = False

    word = st.session_state.puzzle["word"]
    shuffled = st.session_state.puzzle["shuffled"]
    limit = st.session_state.puzzle["time_limit"]
    elapsed = int(time.time() - st.session_state.puzzle.get("start", time.time()))
    remaining = max(0, limit - elapsed)
    progress = (limit - remaining) / limit

    st.markdown(f"<div class='card'><b>Mot mélangé :</b> <span style='font-size:20px'>{shuffled}</span></div>", unsafe_allow_html=True)
    st.progress(progress)
    st.caption(f"Temps restant estimé : {remaining} s")

    guess = st.text_input("Ta réponse :", key="puzz_input").upper()

    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("✅ Valider", key="puzz_val"):
            if remaining == 0:
                st.warning("⏰ Temps écoulé — tu ne peux plus valider. Nouveau mot généré.")
                st.session_state.history["puzzle"].append({"word": word, "result": "timeout"})
            else:
                if guess == word:
                    st.success("Bravo 🎉 bonne réponse !")
                    st.session_state.scores["puzzle"] += 1
                    st.session_state.history["puzzle"].append({"word": word, "result": "win"})
                else:
                    st.error(f"Faux ❌. Le mot était : {word}")
                    st.session_state.history["puzzle"].append({"word": word, "result": "lose"})
            st.session_state.puzzle["answered"] = True
            st.button("🔀 Nouveau mot", key="puzz_trigger")  # small hack for new word UI
            st.experimental_rerun()
    with col2:
        if st.button("💡 Indice (révèle 1 lettre)", key="puzz_hint"):
            # reveal one correct letter in place (simple)
            idx = random.randrange(len(word))
            hint = "".join(
                word[i] if i == idx else "_" for i in range(len(word))
            )
            st.info(f"Indice : {hint}")

    # show recent history
    if st.session_state.history["puzzle"]:
        st.markdown("**Historique (session) — dernières manches :**")
        df = pd.DataFrame(st.session_state.history["puzzle"][-6:])[["word","result"]]
        st.table(df)

def jeu_multiplication():
    st.header("✖️ Quiz de multiplication")
    st.markdown("Résous rapidement des multiplications. Tu peux changer la difficulté.")
    if "level" not in st.session_state.mult:
        st.session_state.mult["level"] = 10  # max multiplicand

    level = st.slider("Choisis la difficulté (max multiplicand):", 6, 20, st.session_state.mult["level"], step=1)
    st.session_state.mult["level"] = level

    if "a" not in st.session_state.mult or st.button("🔢 Nouvelle question", key="mult_new"):
        a = random.randint(1, level)
        b = random.randint(1, level)
        st.session_state.mult["a"] = a
        st.session_state.mult["b"] = b
        st.session_state.mult["asked"] = True
        st.session_state.mult["start"] = time.time()

    a = st.session_state.mult["a"]
    b = st.session_state.mult["b"]
    st.markdown(f"**Combien font {a} × {b} ?**")

    answer = st.number_input("Ta réponse :", key="mult_input", step=1, format="%d")
    if st.button("✅ Valider", key="mult_val"):
        correct = a * b
        if answer == correct:
            st.success("✅ Correct !")
            st.session_state.scores["multiplication"] += 1
            st.session_state.history["multiplication"].append({"q": f"{a}x{b}", "result": "win"})
        else:
            st.error(f"❌ Faux — la bonne réponse est {correct}")
            st.session_state.history["multiplication"].append({"q": f"{a}x{b}", "result": "lose"})
        # new question
        st.session_state.mult.pop("a", None)
        st.session_state.mult.pop("b", None)
        st.experimental_rerun()

    # show scoreboard small
    st.write(f"Score Multiplication (session): {st.session_state.scores['multiplication']}")
    if st.session_state.history["multiplication"]:
        df = pd.DataFrame(st.session_state.history["multiplication"][-6:])
        st.table(df)

def jeu_quiz():
    st.header("🧠 Quiz général")
    st.markdown("Questions rapides de culture générale.")
    if "q" not in st.session_state.quiz or st.button("❓ Nouvelle question", key="quiz_new"):
        q = random.choice(list(QUIZ_QS.keys()))
        st.session_state.quiz["q"] = q
        st.session_state.quiz["start"] = time.time()

    question = st.session_state.quiz["q"]
    st.write(question)
    resp = st.text_input("Ta réponse :", key="quiz_input").upper()

    if st.button("✅ Valider", key="quiz_val"):
        bonne = QUIZ_QS[question]
        if resp == bonne:
            st.success("Bravo 🎉")
            st.session_state.scores["quiz"] += 1
            st.session_state.history["quiz"].append({"q": question, "result": "win"})
        else:
            st.error(f"Mauvaise réponse — la bonne réponse était : {bonne}")
            st.session_state.history["quiz"].append({"q": question, "result": "lose"})
        st.session_state.quiz.pop("q", None)
        st.experimental_rerun()

    st.write(f"Score Quiz (session): {st.session_state.scores['quiz']}")
    if st.session_state.history["quiz"]:
        df = pd.DataFrame(st.session_state.history["quiz"][-6:])
        st.table(df)

# -----------------------
# Page routing
# -----------------------
page = st.session_state.page
if page == "Accueil":
    st.markdown(
        """
        <div class='card'>
        <h3 class='title'>Bienvenue au Centre de mini-jeux 🎉</h3>
        <p class='small'>Choisis un jeu dans le menu à gauche ou clique sur un gros bouton ci-dessous pour y aller.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(3)
    with cols[0]:
        if st.button("🧩 Puzzle de mots", key="home_puzzle"):
            st.session_state.page = "🧩 Puzzle de mots"
            st.experimental_rerun()
    with cols[1]:
        if st.button("✖️ Multiplication", key="home_mult"):
            st.session_state.page = "✖️ Multiplication"
            st.experimental_rerun()
    with cols[2]:
        if st.button("🧠 Quiz", key="home_quiz"):
            st.session_state.page = "🧠 Quiz"
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("📊 Récapitulatif de la session")
    scores = st.session_state.scores
    st.metric("Puzzle", scores["puzzle"])
    st.metric("Multiplication", scores["multiplication"])
    st.metric("Quiz", scores["quiz"])

    st.markdown("Historique global (dernières actions par jeu)")
    for g in ["puzzle", "multiplication", "quiz"]:
        if st.session_state.history[g]:
            st.write(f"**{g.capitalize()}**")
            st.table(pd.DataFrame(st.session_state.history[g][-6:]))

elif page == "🧩 Puzzle de mots":
    jeu_puzzle()
elif page == "✖️ Multiplication":
    jeu_multiplication()
elif page == "🧠 Quiz":
    jeu_quiz()

# -----------------------
# Footer & session summary button
# -----------------------
st.markdown("---")
col_a, col_b = st.columns([3,1])
with col_a:
    st.write("💡 Astuce : les scores sont gardés uniquement pendant cette session; ferme l'onglet pour réinitialiser.")
with col_b:
    if st.button("📋 Résumé session"):
        # build a neat summary modal-like area
        st.session_state.summary_shown = True

if st.session_state.get("summary_shown", False):
    st.markdown("## 🧾 Résumé de la session (temporaire)")
    df_list = []
    for game, hist in st.session_state.history.items():
        if hist:
            # produce counts
            wins = sum(1 for h in hist if h.get("result") == "win")
            total = len(hist)
            df_list.append({"Jeu": game.capitalize(), "Réussites": wins, "Total manches": total, "Score session": st.session_state.scores[game]})
    if df_list:
        st.table(pd.DataFrame(df_list))
    else:
        st.info("Aucune manche jouée pour l'instant — lance un jeu !")
