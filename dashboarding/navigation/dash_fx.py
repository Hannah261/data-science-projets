from imports import * 
from utils.overview import place_dash_fx
from utils.statistique import stats_dash_fx
from utils.analyse import analyse_dash_fx
from dashboard_app import auth_page


# sidebar
with st.sidebar:
    st.title('Paramétrage')
    symbol = st.selectbox('Symbole : ', ['EUR/MGA','USD/MGA'])
    st.session_state['symbol'] = symbol
    if symbol =='EUR/MGA':
        df= pd.read_csv('data/EUR_MGA.csv', parse_dates=['date'])
    if symbol == 'USD/MGA':
        df= pd.read_csv('data/USD_MGA.csv', parse_dates=['date'])
    df.sort_values(by='date', ascending=True, inplace=True)   
    aff = st.checkbox("Afficher les données brutes")
    start_date = st.date_input('Date de début :', pd.to_datetime(df['date'].min()))
    end_date = st.date_input('Date de fin :', pd.to_datetime(df['date'].max()))
    quitter = st.button('Quitter le dashboard')
    if quitter:
        st.switch_page(auth_page)
        st.session_state.clear()
        
    filtered_data = df[(df['date'].dt.date >= start_date) & (df['date'].dt.date <= end_date)]
    

# dashboard
st.title(st.session_state['user_values']['dashboard'] +  " | " +st.session_state["user_values"]['direction'])


onglets = st.tabs(["Vue d'ensemble", "Statistique", "Analyse"]) 

with onglets[1]:
    st.header("Statistique sur les données "+st.session_state['symbol'])
    stats_dash_fx(filtered_data=filtered_data)

with onglets[2]:
    analyse_dash_fx()

with onglets[0]:
    kpi_placeholder = st.empty()           
    if aff:
        cols = st.columns([2,3])
        with cols[0]:
            st.header("Données FX" + " : " + st.session_state['symbol'])
            st.dataframe(filtered_data,height=550)
        with cols[1]:
            place_dash_fx(filtered_data=filtered_data,kpi_placeholder=kpi_placeholder)
    else:
        place_dash_fx(filtered_data=filtered_data,kpi_placeholder=kpi_placeholder)
            
        

    



