import streamlit as st

st.set_page_config(page_title="Logical Style", layout="wide")

# CSS custom
with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
        <div class="hero-content">
            <h1>Élevez vos données au rang de levier stratégique</h1>
            <p>Des solutions conçues pour vos vrais enjeux métier, pas pour cocher des cases techniques.</p>
            <div class="hero-actions">
                <a class="btn primary">Prendre RDV</a>
                <a class="btn secondary">Découvrir nos expertises</a>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True
)

st.markdown("<h2 class='section-title'>Nos piliers data</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="card">
            <h3>Stratégie data</h3>
            <p>Un cap clair, partagé par toute l’entreprise.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="card">
            <h3>Qualité de la donnée</h3>
            <p>Des décisions fondées sur des données fiables.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="card">
            <h3>IA & Analytics</h3>
            <p>Des modèles utiles, pas juste impressionnants.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        """
        <div class="card">
            <h3>Architecture & gouvernance</h3>
            <p>Une base solide pour durer.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
