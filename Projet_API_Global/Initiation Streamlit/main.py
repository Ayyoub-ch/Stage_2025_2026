import streamlit as st

# Charger le CSS
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    
st.title("Mon Application Streamlit")

st.write("Bonjour Streamlit !")
st.header("Ceci est un en-tête")
st.subheader("Ceci est un sous-en-tête")


st.write("Voici une équation en LaTeX :")
st.latex(r"E = mc^2")