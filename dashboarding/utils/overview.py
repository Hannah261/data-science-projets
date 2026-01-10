from imports import * 

@st.fragment
def place_dash_fx(filtered_data, kpi_placeholder):    
    st.header("Graphique : "+st.session_state['symbol'])       
    # chart_type = st.selectbox(
    #         'Type de Graphique :',
    #         ['Bougies','Ligne','Aire']
    # )
    chart_placeholder = st.empty()
    start_index = random.randint(0, max(0, len(filtered_data) -500))
    for i in range(start_index, len(filtered_data), 1):
        data_ = filtered_data.iloc[:i+1] 
        #if chart_type == 'Bougies': 
        chart = StreamlitChart(height=500, toolbox=True)
        chart.grid(vert_enabled=False, horz_enabled=False)
        chart.legend(visible=True, font_family='Trebuchet MS', ohlc=True, percent=True, color="#1D1C1CFF")
        chart.layout(background_color="#ffffff",text_color="#1D1C1CFF")
            
        chart.set(data_)
        with chart_placeholder.container():
            chart.load()
        fig = go.Figure()
        
        # if chart_type == 'Aire':
        #    pass
            
        # if chart_type == 'Ligne':
        #     pass
            
        with kpi_placeholder.container():
            kpi = st.columns(5)
            kpi[0].metric(label="Taux de change", value=f"{data_.iloc[-1]['change']}%",
                        delta=((data_.iloc[-1]['change']-data_.iloc[-2]['change']).round(2) if i > 0 else 0))
            kpi[1].metric(label="Volatilité (MGA)", value=f"{(data_.iloc[-1]['high']-data_.iloc[-1]['low']).round(2)}",
                        delta=((data_.iloc[-1]['high']-data_.iloc[-1]['low']).round(2)-(data_.iloc[-1-i]['high']-data_.iloc[-1-i]['low']).round(2)).round(2))
            kpi[2].metric(label="Prix maximum (MGA)", value=f"{data_.iloc[-1]['high']}")
            kpi[3].metric(label='Prix minimun (MGA)'
                          , value=f"{data_.iloc[-1]['low']}")
            kpi[4].metric(label='Volume (MGA)', value=f"{data_.iloc[:i]['volume'].sum()}")
        
        sleep(1)  


def place_dash_csbf(filtered_data,col_select):
    col_chart = st.columns(4)
    
    with col_chart[0]:
        # Ttotal des actifs par année 
        fig_tree_map = px.treemap(
        filtered_data,
        path=[col_select],
        values="total_actifs",
        title="Total des actifs (en milliards d'ar) par année",
        )
        st.plotly_chart(fig_tree_map, use_container_width=True)
    
        # Graphique en radar pour le taux de solvabilité
        solvabilite_radar = filtered_data.groupby(col_select)["ratio_solvabilite"].mean().reset_index()
        fig_solvabilite_radar = px.line_polar(solvabilite_radar, r="ratio_solvabilite", theta=col_select, line_close=True,
                                            title="Ratio de solvabilité moyen",
                                            labels={"ratio_solvabilite": "Taux de solvabilité (%)"})
        st.plotly_chart(fig_solvabilite_radar, use_container_width=True)
   
        
    with col_chart[1]:
        # nombre des agences
        fig_agence = px.bar(filtered_data, x="annee", y="nombre_agence", color=col_select,
                            title="Nombre d'agences")
        st.plotly_chart(fig_agence, use_container_width=True)
        
        
        #Ratio de liquidité
        # Tracer le graphique en aires (Area Chart) avec Plotly Express
        fig = px.area(filtered_data, x=col_select, y='ratio_liquidite',
                    title='Ratio de Liquidité Moyen',
                    labels={'ratio_liquidite': 'Ratio de Liquidité Moyen (%)'},
                    line_group=col_select, color=col_select)

        # Affichage du graphique
        st.plotly_chart(fig)

        
    with col_chart[2]:
        # coeficient d'exploitation
        fig2 = px.pie(
            filtered_data,
            names=col_select,
            values="coeff_exploitation",
            title="Répartition des coefficients d'exploitation",
            hole=0.4
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        #ROA
        fig_bubble = px.scatter(filtered_data, x="annee", y="roa", size="total_actifs", color=col_select,
                        title="ROA par année selon les actifs",
                        labels={"roa": "ROA (%)", "annee": "Année", "total_actifs": "Volume des Actifs"})
        st.plotly_chart(fig_bubble)
       
    with col_chart[3]:
        # Résultat net (en milliards d'ar)": "Résultat net (milliards d'ar)
        fig_evolution_resultat = px.area(filtered_data, x="annee", y="resultat_net", color=col_select,
                                     title="Évolution du Résultat Net",
                                     labels={"resultat_net": "Résultat net (milliards d'ar)"})
        st.plotly_chart(fig_evolution_resultat, use_container_width=True)
        
        #CES
        fig_sunburst = px.sunburst(filtered_data, path=["annee",col_select], values="taux_ces",
                           title="Répartition du CES par Année")
        st.plotly_chart(fig_sunburst)
        