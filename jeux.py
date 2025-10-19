import streamlit as st
import random

# -------------------------------
# 🎮 Jeu 1 : Puzzle de mots
# -------------------------------
def jeu_puzzle():
    st.subheader("🧩 Jeu de mots mélangés")
    MOTS = ["PYTHON", "PUZZLE", "JEU", "CODE", "ALGO", "ORDINATEUR"]

    if "mot" not in st.session_state:
        st.session_state.mot = random.choice(MOTS)
    if "melange" not in st.session_state:
        lettres = list(st.session_state.mot)
        random.shuffle(lettres)
        st.session_state.melange = " ".join(lettres)
    if "score1" not in st.session_state:
        st.session_state.score1 = 0

    st.write("🔠 Mélange :", st.session_state.melange)
    reponse = st.text_input("Entre le mot correct :").upper()

    if st.button("Valider", key="btn_puzzle"):
        if reponse == st.session_state.mot:
            st.success("Bravo 🎉 Bonne réponse !")
            st.session_state.score1 += 1
        else:
            st.error(f"Mauvaise réponse 😢 Le mot était {st.session_state.mot}")

        # Nouveau mot
        st.session_state.mot = random.choice(MOTS)
        lettres = list(st.session_state.mot)
        random.shuffle(lettres)
        st.session_state.melange = " ".join(lettres)

    st.write("🏆 Score :", st.session_state.score1)

# -------------------------------
# 🎯 Jeu 2 : Quiz de multiplication
# -------------------------------
def jeu_multiplication():
    st.subheader("✖️ Quiz de multiplication")

    if "score2" not in st.session_state:
        st.session_state.score2 = 0
    if "a" not in st.session_state:
        st.session_state.a = random.randint(1, 10)
        st.session_state.b = random.randint(1, 10)

    st.write(f"Combien font {st.session_state.a} × {st.session_state.b} ?")
    reponse = st.number_input("Ta réponse :", step=1, format="%d")

    if st.button("Valider", key="btn_mult"):
        if reponse == st.session_state.a * st.session_state.b:
            st.success("✅ Bonne réponse !")
            st.session_state.score2 += 1
        else:
            st.error(f"❌ Mauvaise réponse. C'était {st.session_state.a * st.session_state.b}.")

        # Nouvelle question
        st.session_state.a = random.randint(1, 10)
        st.session_state.b = random.randint(1, 10)

    st.write("🏆 Score :", st.session_state.score2)

# -------------------------------
# 🧠 Jeu 3 : Quiz simple
# -------------------------------
def jeu_quiz():
    st.subheader("🧠 Quiz de culture générale")
    questions = {
        "Quelle est la capitale du Maroc ?": "RABAT",
        "Combien font 3 + 5 ?": "8",
        "Langage utilisé pour Streamlit ?": "PYTHON",
    }

    if "score3" not in st.session_state:
        st.session_state.score3 = 0
    if "question" not in st.session_state:
        st.session_state.question = random.choice(list(questions.keys()))

    st.write(st.session_state.question)
    reponse = st.text_input("Ta réponse :").upper()

    if st.button("Valider", key="btn_quiz"):
        bonne = questions[st.session_state.question]
        if reponse == bonne:
            st.success("Bonne réponse 🎉")
            st.session_state.score3 += 1
        else:
            st.error(f"Mauvaise réponse 😢 La bonne réponse était : {bonne}")

        # Nouvelle question
        st.session_state.question = random.choice(list(questions.keys()))

    st.write("🏆 Score :", st.session_state.score3)

# -------------------------------
# 🏠 Page principale avec menu
# -------------------------------
st.title("🎮 Centre de jeux Streamlit")

choix = st.sidebar.selectbox(
    "Choisis ton jeu :",
    ["Accueil", "🧩 Puzzle de mots", "✖️ Multiplication", "🧠 Quiz"]
)

if choix == "Accueil":
    st.write("""
    👋 Bienvenue dans ton centre de jeux !
    
    Sélectionne un jeu dans le menu à gauche :
    - 🧩 **Puzzle de mots** : devine le mot mélangé  
    - ✖️ **Multiplication** : calcule vite les produits  
    - 🧠 **Quiz** : teste ta culture générale
    """)
elif choix == "🧩 Puzzle de mots":
    jeu_puzzle()
elif choix == "✖️ Multiplication":
    jeu_multiplication()
elif choix == "🧠 Quiz":
    jeu_quiz()
