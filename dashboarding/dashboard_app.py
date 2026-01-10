from imports import *

def main():
    
    # Configuration de la page
    st.set_page_config(
        page_title="DASHBOARD CENTRALISE",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.logo("assets/img/bfm-min-v2_0.png", size='large')
    
    # pour inclure le CSS si nécessaire
    with open("assets/css/style.css") as f:
        st.html(f"<style>{f.read()}</style>") # ou st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)       

# les pages
    
# page d'authentification
auth_page = st.Page(
    page="navigation/auth.py",
    title="Authentification",
    default=True
)

dash_default_page =st.Page(
    page="navigation/dash_default.py",
    title="Dashboard par défaut"
)

create_dash_page=st.Page(
    page="navigation/create_dash.py",
    title="Création de dashboard"
)

dash_fx_page= st.Page(
    page="navigation/dash_fx.py",
    title="FX Analytics dashboard"
)

dash_csbf_page = st.Page(
    page="navigation/dash_csbf.py",
    title="Dashboard de suivi"
)

pg = st.navigation(
        [auth_page,dash_default_page,create_dash_page,dash_fx_page,dash_csbf_page],
        position='hidden'
    )
    
if __name__ == '__main__':
    main()
    pg.run()
