from imports import *
from dashboard_app import auth_page, dash_default_page

import json


if "components" not in st.session_state:
    st.session_state.components= []   

direction = st.session_state['user_values']['direction']
if direction == 'CSBF':
    datas = ["Autorisé à Exercer en ME", "Données IMF_Banque"]
if direction == 'DRC':
    datas = ["Données FX"]
if direction == 'DIT':
    datas =["Autorisé à Exercer en ME", "Données IMF_Banque","Données FX"]
    
# Dictionnaire des types de graphiques supportés avec Plotly Express
graph_types = {
    "Ligne": px.line,
    "Barres": px.bar,
    "Nuage de points": px.scatter,
    "Aire": px.area,
    "Histogramme": px.histogram,
    "Heatmap": px.density_heatmap
}



with st.sidebar:
    st.header('Création de nouveau dashboard')
    
        
    dashboard_name = st.text_input("Nom du Dashboard", "Mon Dashboard")
        
    input_data = st.selectbox("Données brutes à charger :", datas)
    if input_data == "Autorisé à Exercer en ME":
        df = pd.read_csv("./data/ME.csv") 
        
    if input_data == "Données FX":  
        symbol = st.sidebar.radio("Symbole :", options=['EUR/MGA','USD/MGA'])
        if symbol == 'EUR/MGA' : 
            df = pd.read_csv('data/EUR_MGA.csv', parse_dates=['date'])
            
        if symbol == 'USD/MGA' :
            df = pd.read_csv('data/USD_MGA.csv', parse_dates=['date'])
            
    if input_data == "Données IMF_Banque":
        df = pd.read_csv("data/IMF_Banque.csv")
      
    
    component_type = st.selectbox("Type de composant", 
                                    ["Graphique", "Texte", "Curseur", "Sélecteur", "Case à cocher", "Sélecteur multiple", "Onglet"])
    
    if component_type == "Graphique":

        # Sélection du type de graphique
        selected_graph_type = st.selectbox("Type de graphique", list(graph_types.keys()))
        
        # Sélection des axes à partir des colonnes du DataFrame
        x_axis = st.selectbox("Sélectionner l'axe X", options=df.columns)
        # Pour l'axe Y, on exclut la colonne déjà sélectionnée pour X
        y_axis_options = [col for col in df.columns if col != x_axis]
        y_axis = st.selectbox("Sélectionner l'axe Y", options=y_axis_options)
        
        # Saisie du titre du graphique
        graph_title = st.text_input("Titre du graphique", value=f"Graphique {selected_graph_type}")
        st.plotly_chart(graph_types[selected_graph_type](df,x=x_axis,y=y_axis, title=graph_title),key= random.randint(0, max(0, 999)))
        
        if st.button("Ajouter le composant"):
            # Création du graphique avec le titre personnalisé
            # fig = graph_types[selected_graph_type](df, x=x_axis, y=y_axis, title=graph_title)
            # Stockage du graphique sous forme JSON pour la sérialisation
            st.session_state.components.append({'type':'graph','graph_type': selected_graph_type,'x':x_axis,'y':y_axis, 'title':graph_title, 'data':input_data})
        print(graph_types[selected_graph_type])

    
    if component_type == "Onglet":
        tab_labels = st.text_area("Noms des onglets (séparés par des virgules)", "Onglet 1, Onglet 2, Onglet 3")
        tab_list = [label.strip() for label in tab_labels.split(",")]

        if st.button("Ajouter le composant"):
            st.session_state.components.append({'type': 'tabs', 'labels': tab_list})
        
    elif component_type == "Texte":
        text_content = st.sidebar.text_area("Entrez votre texte")
        if st.button("Ajouter le composant"):
            st.session_state.components.append({'type':'text', 'content': text_content})
            
    elif component_type == "Curseur":
        slider_label = st.text_input("Label du curseur")
        min_value = st.number_input("Valeur minimale", value=0)
        max_value = st.number_input("Valeur maximale", value=100)
        default_value = st.number_input("Valeur par défaut", value=50)
        if st.button("Ajouter le composant"):
            st.session_state.components.append({'type': 'slider', 'label': slider_label, 'min': min_value, 'max': max_value, 'default': default_value})

    elif component_type == "Sélecteur":
        select_label = st.text_input("Label du sélecteur")
        select_options = st.text_area("Options (séparées par des virgules)", "Option 1, Option 2, Option 3")
        options_list = [option.strip() for option in select_options.split(",")]
        if st.button("Ajouter le composant"):
            st.session_state.components.append({'type': 'selectbox', 'label': select_label, 'options': options_list})

    elif component_type == "Case à cocher":
        checkbox_label = st.text_input("Label de la case à cocher")
        default_value = st.checkbox("Valeur par défaut", value=False) 
        if st.button("Ajouter le composant"):     
            st.session_state.components.append({'type': 'checkbox', 'label': checkbox_label, 'default': default_value})

    elif component_type == "Sélecteur multiple":
        multiselect_label = st.text_input("Label du sélecteur multiple")
        multiselect_options = st.text_area("Options (séparées par des virgules)", "Option 1, Option 2, Option 3")
        options_list = [option.strip() for option in multiselect_options.split(",")]
        if st.button("Ajouter le composant"):
            st.session_state.components.append({'type': 'multiselect', 'label': multiselect_label, 'options': options_list})

    # elif component_type == "Saisie de date":
    #     date_label = st.text_input("Label de la saisie de date")
    #     default_date = st.date_input("Date par défaut")
    #     if st.button("Ajouter le composant"):
    #         st.session_state.components.append({'type': 'date_input', 'label': date_label, 'default': default_date.to_dict(orient='list')})
    
    quitter = st.button('Quitter le dashboard')
    if quitter:
        st.switch_page(auth_page)
        st.session_state.clear()
        
placeholder = st.empty() 
  

# --- 2. Interfaces de création et de chargement du dashboard ---         

with placeholder.container():
    st.title(dashboard_name + " | " + direction)          
        
    if input_data == "Données FX":  
        if symbol == 'EUR/MGA' : 
            st.header(input_data +" : EUR/MGA")
        if symbol == 'USD/MGA' :
            st.header(input_data +" : USD/MGA")
        st.dataframe(df)
    else:              
        st.header(input_data)
        st.dataframe(df)

    for component in st.session_state.components:
        if component['type'] == 'graph':
            # st.plotly_chart(graph_types[selected_graph_type](df, x=x_axis, y=y_axis, title=graph_title))
            st.plotly_chart(graph_types[component['graph_type']](df,x=component['x'],y=component['y'],title =component['title']))
        elif component['type'] == 'text':
            st.write(component['content'])
        elif component['type'] == 'slider':
            st.slider(component['label'], min_value=component['min'], max_value=component['max'], value=component['default'])
        elif component['type'] == 'selectbox':
            st.selectbox(component['label'], component['options'])
        elif component['type'] == 'checkbox':
            st.checkbox(component['label'], value=component['default'])
        elif component['type'] == 'multiselect':
            st.multiselect(component['label'], component['options'])
        elif component['type'] == 'tabs':
            tabs = st.tabs(component['labels'])
            for i, tab in enumerate(tabs):
                with tab:
                    st.write(f"Contenu de l'onglet {component['labels'][i]}")
        # elif component['type'] == 'date_input':
        #     st.date_input(component['label'], value=component['default'])
            
    print(st.session_state.components)
    
    # col1, col2 = st.columns(2)
    # with col1:
    #     # Sauvegarde de la configuration
    #     if st.button("Sauvegarder le Dashboard"):
    #         if st.session_state.components == []:
    #             pass
    #         else:
    #             st.session_state.components.append({'type':'data','name':input_data})
    #             try:
    #                 query = """
    #                 INSERT INTO dashboards (user_id, nom, config, date_creation)
    #                 VALUES (%s, %s, %s, NOW())
    #                 RETURNING id
    #                 """
    #                 cursor.execute(query, (st.session_state['user_values']['matricule'], dashboard_name, json.dumps(st.session_state.components)))
    #                 dashboard_id = cursor.fetchone()[0]
    #                 conn.commit()
                    
    #                 with col2:
    #                     with st.spinner(text="Sauvegarde..."):
    #                         sleep(4)
                            
    #                 st.success("Dashboard créé avec succès")
    #                 # sleep(5)    
    #                 del st.session_state["components"] 
    #                 # load_dashboard(dashboard_id)
    #                 #st.switch_page(dash_default_page)
                    
    #                 # st.session_state.clear()
    #                 # st.rerun()
    #             except Exception as e:
    #                 st.warning(f"Erreur lors de la sauvegarde du dashboard : {str(e)}")          
                    
                
    
    
