from imports import *
from utils.overview import place_dash_csbf
from utils.statistique import stats_dash_csbd
from utils.analyse import analyse_dash_csbf
from dashboard_app import auth_page


# sidebar
with st.sidebar:
    st.title('Filtre')
    
    aff = st.checkbox("Afficher les données brutes")
    
    df = pd.read_csv("data/IMF_Banque.csv")
    
    selected_year = st.multiselect(
        "Année :",
        options=df["annee"].unique(),
        default=df["annee"].unique()
    )
    
    select = st.radio("Par :",options= ['Type', 'Entité'])
    if select == 'Entité':
        col_select = 'entite'
        selected = st.multiselect(
            "Entité :",
            options=df["entite"].unique(),
            default=df["entite"].unique()
        )
    if select == 'Type':
        col_select='type'
        selected = st.multiselect(
            "Type :",
            options=df["type"].unique(),
            default=df["type"].unique()
        )
    
    quitter = st.button('Quitter le dashboard')
    if quitter:
        st.switch_page(auth_page)
        st.session_state.clear()
    
    filtered_data = df[(df["annee"].isin(selected_year)) & (df[col_select].isin(selected))]
    
   

# dashboard
st.title(st.session_state['user_values']['dashboard'] + " | " + st.session_state['user_values']['direction'])


onglets = st.tabs(["Vue d'ensemble", "Statistique", "Analyse"]) 

with onglets[0]:
    # Indicateurs clés
    col1, col2, col3, col4 = st.columns(4)
   
    col1.metric("Crédits Bruts (Mds Ar)", f"{filtered_data['credits_bruts'].sum():,.2f}")
    col2.metric("Dépôts Clientèle (Mds Ar)", f"{filtered_data['depots'].sum():,.2f}")
    col3.metric("Produit Net (Mds Ar)", f"{filtered_data['produit_net_bancaire'].sum():,.2f}")
    col4.metric("Résultat Net (Mds Ar)", f"{filtered_data['resultat_net'].sum():,.2f}")

    # Table des données filtrées
    if aff:
        st.header("Données IMF et banque")
        st.dataframe(filtered_data, use_container_width=True)
        
    place_dash_csbf(filtered_data=filtered_data, col_select=col_select)
    
    
with onglets[1]:
    stats_dash_csbd(df)
            
                  
with onglets[2]:
    def predicting(model,type, annee, nb):
        x = np.array([type, annee]+nb).reshape(1,2+len(nb))
        return model.predict(x)
    analyse_dash_csbf(df=df, predicting=predicting)
    