from imports import * 
from dashboard_app import dash_default_page,dash_fx_page,dash_csbf_page,create_dash_page

col1, col2, col3 = st.columns([2,3,2],vertical_alignment='center')


# A REFAIRE DANS LA BASE
@st.dialog("Accès")
def show_option(user_values):
    if user_values['direction'] == "DIT":
        dash = st.selectbox("Dashboard(s) disponible(s) : ", ["FX Analytics dashboard",'Dashboard de Suivi'])
    if user_values['direction'] == "DRC":
        dash = st.selectbox("Dashboard(s) disponible(s) : ", ['FX Analytics dashboard'])
    if user_values['direction'] == 'CSBF':
        dash = st.selectbox("Dashboard(s) disponible(s) : ", ['Dashboard de Suivi'])
            
    if user_values['user'] == 'admin':
        col6, col7 = st.columns(2)
        with col6:
            charge = st.button('Charger le dashboard')
        with col7:
            create = st.button('Créer un dashboard')
        if create:
            st.switch_page(create_dash_page)
    else :
        charge = st.button('Charger le dashboard')
        
    if charge:
        if direction == "DRC" and dash != "FX Analytics dashboard":
            st.error('Vous n\'avez pas accès à ce type de dashboard')
        elif direction == "CSBF" and dash != "Dashboard de Suivi":
            st.error('Vous n\'avez pas accès à ce type de dashboard')
        else:
            st.session_state['user_values']['dashboard'] = dash
            if dash == 'FX Analytics dashboard':
                st.switch_page(dash_fx_page)
            elif dash == 'Dashboard de Suivi':
                st.switch_page(dash_csbf_page)
            else:
                st.switch_page(dash_default_page)
    
 
 
with col2: 
    st.title("DASHBOARD CENTRALISE")
    with st.container(border=True):
        col4, col5 = st.columns(2)
        with col4 :
            user = st.selectbox("Utilisateur : ", ["admin", "simple"])
        with col5 :         
            direction = st.selectbox("De : ", ["DIT","CSBF","DRC"])
            
        submit_button = st.button(label='Se connecter')
        
        if submit_button:
            user_values = {
                    "user": user,
                    "direction":direction
                }
            st.session_state["user_values"] = user_values
            print(st.session_state["user_values"])
            show_option(user_values)
    
        
        
            
            


