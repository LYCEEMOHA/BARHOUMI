import streamlit as st

st.set_page_config(page_title="Quiz interactif", page_icon="🧠")

st.title("🧠 Petit Quiz interactif")

# Questions, options et bonnes réponses
questions = [
    {
        "question": "Quel langage est utilisé pour créer Streamlit ?",
        "options": ["Java", "Python", "C++", "PHP"],
        "reponse": "Python"
    },
    {
        "question": "Quelle commande permet de lancer une app Streamlit ?",
        "options": ["python app.py", "run streamlit app", "streamlit run app.py", "launch streamlit"],
        "reponse": "streamlit run app.py"
    },
    {
        "question": "Streamlit est principalement utilisé pour :",
        "options": [
            "Créer des jeux vidéo 3D",
            "Faire du traitement de texte",
            "Créer des applications web de données",
            "Programmer des microcontrôleurs"
        ],
        "reponse": "Créer des applications web de données"
    }
]

# Initialisation de l’état du quiz
if "score" not in st.session_state:
    st.session_state.score = 0
if "index" not in st.session_state:
    st.session_state.index = 0

# Affichage de la question actuelle
q = questions[st.session_state.index]
st.subheader(f"Question {st.session_state.index + 1} / {len(questions)}")
reponse = st.radio(q["question"], q["options"])

# Bouton pour valider la réponse
if st.button("Valider"):
    if reponse == q["reponse"]:
        st.success("✅ Bonne réponse !")
        st.session_state.score += 1
    else:
        st.error(f"❌ Mauvaise réponse. La bonne était : {q['reponse']}")

    # Passer à la question suivante
    if st.session_state.index + 1 < len(questions):
        st.session_state.index += 1
        st.experimental_rerun()
    else:
        st.balloons()
        st.success(f"🎉 Quiz terminé ! Ton score : {st.session_state.score} / {len(questions)}")
        if st.button("Rejouer"):
            st.session_state.score = 0
            st.session_state.index = 0
            st.experimental_rerun()
