from datetime import timedelta
from imports import *



# analyse dans FX dashboard
def analyse_dash_fx():
    df1 = pd.read_csv('data/EUR_MGA.csv', parse_dates=['date']).sort_values(by='date')
    df2 = pd.read_csv('data/USD_MGA.csv', parse_dates=['date']).sort_values(by='date')
    type_anal = st.radio("Type d'analyse : ", options=["Analyse comparative", "Analyse prédictive"])
    if type_anal == "Analyse comparative":
        st.header(type_anal)
        
        
        parr = st.selectbox("Par rapport à", ['Taux de change', 'Prix'])
        
        if parr == 'Taux de change':
            name_col = 'change'
        if parr == 'Prix':
            name_col = 'close'
        # Créer un graphique interactif avec Plotly
        fig = go.Figure()

        # Ajouter la série EUR/MGA
        fig.add_trace(go.Scatter(
            x=df1['date'],
            y=df1[name_col],
            mode='lines',
            name='EUR/MGA',
            line=dict(color='blue', width=2),
            hovertemplate='Date: %{x}<br>EUR/MGA: %{y:.2f}'
        ))

        # Ajouter la série USD/MGA
        fig.add_trace(go.Scatter(
            x=df2['date'],
            y=df2[name_col],
            mode='lines',
            name='USD/MGA',
            line=dict(color='green', width=2),
            hovertemplate='Date: %{x}<br>USD/MGA: %{y:.2f}'
        ))

        # Ajouter des labels et configurer l'affichage
        fig.update_layout(
            title="EUR/MGA vs USD/MGA",
            xaxis_title="Date",
            yaxis_title=parr,
            template="plotly_white",
            legend=dict(orientation="h", x=0.5, y=-0.2, xanchor='center')
        )

        # Afficher le graphique dans Streamlit ou en dehors
        st.plotly_chart(fig, use_container_width=True)
    
    if type_anal == 'Analyse prédictive':
        st.header(type_anal)
        currency_pair = st.selectbox("Choisir la paire de devises :", ["EUR/MGA", "USD/MGA"])
        days_to_predict = st.number_input("Nombre de jours pour la prédiction :", min_value=30, value=30)

        # Chargement des données historiques (exemples simulés)
        if currency_pair == "EUR/MGA":
            df = df1  # Données EUR/MGA
        elif currency_pair == "USD/MGA":
            df = df2  # Données USD/MGA

        # S'assurer que la colonne 'date' est au format datetime
        df['date'] = pd.to_datetime(df['date'])

        # Préparation des données pour le modèle
        df['days_since_start'] = (df['date'] - df['date'].min()).dt.days  # Convertir les dates en jours
        X = df[['days_since_start']]
        y = df['close']

        # Entraîner le modèle
        model = LinearRegression()
        model.fit(X, y)

        # Générer des prédictions pour les jours à venir
        future_dates = [df.iloc[-1]['date'] + timedelta(days=i+1) for i in range(days_to_predict)]
        future_days_since_start = [(date - df['date'].min()).days for date in future_dates]
        future_X = np.array(future_days_since_start).reshape(-1, 1)
        future_predictions = model.predict(future_X)
        
        # Créer un DataFrame pour les prédictions
        predictions_df = pd.DataFrame({
            'date': future_dates,
            'predicted_close': future_predictions
        })
        print(predictions_df)
        # Graphique des données historiques et des prédictions
        fig = go.Figure()

        # Ajouter les données historiques
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['close'],
            name='Historique',
            line=dict(color='blue'),
            hovertemplate='Date: %{x}<br>Close: %{y:.2f}'
        ))

        # Ajouter les prédictions
        fig.add_trace(go.Scatter(
            x=predictions_df['date'],
            y=predictions_df['predicted_close'],
            name='Marge de prédictions',
            line=dict(color='red', dash='dash'),
            hovertemplate='Date: %{x}<br>Marge de prédiction: %{y:.2f}'
        ))

        # Configurer le graphique
        fig.update_layout(
            title=f"Évolution des prix de clôture pour {currency_pair}",
            xaxis_title="Date",
            yaxis_title="Prix de Clôture",
            template="plotly_white",
            legend=dict(orientation="h", x=0.5, y=-0.2, xanchor="center")
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig, use_container_width=True)
       
       
# analyse dans dashboard de suivi       
def analyse_dash_csbf(df, predicting):
    
    
    type_anal = st.radio("Type d'analyse : ", options=["Analyse comparative", "Analyse prédictive"])
    
    if type_anal == "Analyse comparative":
        st.header(type_anal)
        # Demander à l'utilisateur de sélectionner plusieurs colonnes à comparer
       
        dfcolumns = df.select_dtypes(exclude='object').drop(columns='annee', axis=1)
        columns_to_compare = st.multiselect("Sélectionnez les colonnes à comparer", dfcolumns.columns)
        graphical_compare = st.selectbox("Graphique de comparaison", ['Barre', 'Ligne','Nuage de points'])

        if len(columns_to_compare) > 0:
            # Calculer la somme ou la moyenne pour chaque colonne, par catégorie
            df_grouped_multi = df.groupby('annee')[columns_to_compare].sum().reset_index()
            if graphical_compare == 'Barre':
                # Créer un graphique en barres pour plusieurs colonnes
                fig_bar_multi = px.bar(df_grouped_multi, x='annee', y=columns_to_compare, title="Comparaison multiple")
                st.plotly_chart(fig_bar_multi)
            if graphical_compare == 'Ligne':
                # Créer un graphique en ligne pour plusieurs colonnes
                fig_line_multi = px.line(df_grouped_multi, x='annee', y=columns_to_compare, title="Comparaison par rapport à l'évolution")
                st.plotly_chart(fig_line_multi)
            if graphical_compare == 'Nuage de points':
                fig_scatter_multi = px.scatter(df_grouped_multi, x='annee', y=columns_to_compare, title="Comapraison par rapport à la relation")
                st.plotly_chart(fig_scatter_multi)
                
    if type_anal == "Analyse prédictive":
        st.header(type_anal)
        numeric_columns = ['total_actifs', 'credits_bruts', 'depots', 'produit_net_bancaire', 'resultat_net']
        target_column = st.selectbox("Sélectionnez ce que vous voulez prédire", numeric_columns)
        pred_col = st.columns(2)
        with pred_col[0]:
            car_type = st.selectbox("De type", df["type"].unique())
            if car_type == 'Banque':
                type=1
            if car_type == 'IMF':
                type=2
        with pred_col[1]:
            annee = st.selectbox("Pour quelle année", [2025,2026,2027])
        var_preds =st.multiselect("A partir de :", df.select_dtypes(exclude='object').drop(columns=['annee', target_column], axis=1).columns)
        condition = []
        for col in var_preds:
            if col == 'nombre_agence':
                condition_val = st.number_input(col, step=1, value=1)  
            else:
                condition_val = st.number_input(col)
            condition.append(condition_val)
        
        y = df[target_column]
        X = df[['type' , 'annee'] + var_preds]
        X['type'].replace(['Banque','IMF'],[1,2], inplace=True)
        
        pred = st.button("Prédire")
        if pred:

            # Créer et entraîner le modèle
            model = LinearRegression()
            model.fit(X, y)

            y_pred = predicting(model, type=type, annee=annee, nb=condition)
            st.write(f"La valeur prédite de {target_column} est **:red[{y_pred[0]:.2f} milliards d'Ar]**")
    
            fig = go.Figure()

                # Ajouter les données d'entraînement au graphique
            fig.add_trace(go.Scatter(
                x=X['annee'],
                y=y,
                mode='markers',
                name='Données d\'entraînement',
                marker=dict(color='blue', size=10),
                hovertemplate='Année: %{x}<br>Valeur: %{y:.2f} milliards'
            ))

            # Ajouter la prédiction au graphique
            fig.add_trace(go.Scatter(
                x=[annee],
                y=[y_pred[0]],
                mode='markers',
                name='Prédiction',
                marker=dict(color='red', size=15, symbol='diamond'),
                hovertemplate='Année: %{x}<br>Prédiction: %{y:.2f} milliards'
            ))
            
            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig, use_container_width=True)