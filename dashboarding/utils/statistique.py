from imports import *

def stats_dash_fx(filtered_data):
    var_cols = st.selectbox("Sélectionner une colonne :", ["Prix d'ouverture","Prix de clôture"])
    stat_col = st.columns(2)
    with stat_col[0]:
        st.subheader("Moyenne mobile :")
        period = st.slider('Période de la moyenne mobile', min_value=5, max_value=200, value=20)
        if var_cols == "Prix d'ouverture":
            filtered_data[f'MA_{period}'] = filtered_data['open'].rolling(window=period).mean()
            fig = px.line(filtered_data, x=filtered_data.date, y=['open', f'MA_{period}'], title=f'{var_cols} et Moyenne Mobile ({period} jours)',
                          labels={'value': 'Prix'})
            st.plotly_chart(fig)
        if var_cols == "Prix de clôture":
            filtered_data[f'MA_{period}'] = filtered_data['close'].rolling(window=period).mean()
            fig = px.line(filtered_data, x=filtered_data.date, y=['close', f'MA_{period}'], title=f'{var_cols} et Moyenne Mobile ({period} jours)',
                           labels={'value': 'Prix'})
            st.plotly_chart(fig)
       
    with stat_col[1]:
        st.subheader("Volatilité :")
        window = st.slider('Sélectionnez la taille de la fenêtre pour la volatilité', min_value=5, max_value=50, value=20, step=1)
        if var_cols == "Prix d'ouverture":
            filtered_data['Daily Return'] = filtered_data['open'].pct_change()

            # Calcul de la volatilité globale (écart-type des rendements quotidiens sur l'ensemble des données)
            volatility_global = filtered_data['Daily Return'].rolling(window=window).std() * np.sqrt(252)  # Volatilité annualisée

            # Créer une nouvelle colonne avec la volatilité globale répétée pour chaque jour
            filtered_data['Global Volatility'] = volatility_global

            # Créer un graphique en aire de la volatilité globale
            fig = px.area(filtered_data, x=filtered_data.date, y='Global Volatility', 
                        title=f"Volatilité du prix d'ouverture (sur {window} jours, annualisée)", 
                        labels={'Global Volatility': 'Volatilité', 'date': 'date'},
                        line_shape='linear')

            # Afficher le graphique dans Streamlit
            st.plotly_chart(fig) 
        if var_cols == 'Prix de clôture':
                filtered_data['Daily Return'] = filtered_data['close'].pct_change()

                # Calcul de la volatilité globale (écart-type des rendements quotidiens sur l'ensemble des données)
                volatility_global = filtered_data['Daily Return'].rolling(window=window).std() * np.sqrt(252)  # Volatilité annualisée

                # Créer une nouvelle colonne avec la volatilité globale répétée pour chaque jour
                filtered_data['Global Volatility'] = volatility_global

                # Créer un graphique en aire de la volatilité globale
                fig = px.area(filtered_data, x=filtered_data.date, y='Global Volatility', 
                            title=f"Volatilité du prix de Clôture (sur {window} jours, annualisée)", 
                            labels={'Global Volatility': 'Volatilité', 'date': 'date'},
                            line_shape='linear')

                # Afficher le graphique dans Streamlit
                st.plotly_chart(fig) 
                
    with stat_col[0]:
        fig = px.line(filtered_data, x='date', y=['open', 'close'], title="Évolution des prix d'ouverture et de clôture",
                    labels={'value': 'Prix', 'variable': 'Type de prix'})

        st.plotly_chart(fig)
        
    with stat_col[1]:
                       
        filtered_data['Daily Change'] = ((filtered_data['close']-filtered_data['open']) / filtered_data['open']) * 100 # diff() calcule la différence par rapport au jour précédent

        # Créer le graphique avec Plotly
        fig = go.Figure()

        # Ajouter la trace pour le changement quotidien (Daily Change)
        fig.add_trace(go.Scatter(x=filtered_data['date'], y=filtered_data['Daily Change'], mode='lines', name='Changement quotidien'))

        # Définir les propriétés du graphique
        fig.update_layout(
            title="Évolution des variations quotidiennes des prix",
            xaxis_title="date",
            yaxis_title="variation du prix",
            template="plotly_dark"  # Facultatif : pour une ambiance sombre
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig)
        
        
def stats_dash_csbd(df):
    # Graphique interactif
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribution statistique :")
        # Afficher les colonnes disponibles pour l'analyse
        col_to_analyze = st.selectbox("Sélectionnez une colonne ", df.columns)
        col3, col4 = st.columns(2, vertical_alignment='center')
        with col3:
            if col_to_analyze:
                st.write(df[col_to_analyze].describe())
           
        # with col2:
        #     # Afficher les statistiques descriptives
        
        #         # Afficher un Violin Plot
        #     fig_violin = px.violin(df, y=col_to_analyze, box=True, points="all", title=f"Violin Plot de {col_to_analyze}",color='type')
        #     st.plotly_chart(fig_violin)
       
        
        with col4:
            # Graphique en Histogramme
            fig_hist = px.histogram(df, x=col_to_analyze, title=f"Histogramme de {col_to_analyze}", color='type')
            st.plotly_chart(fig_hist)
   
    with col2: 
        st.subheader("Correlation :")

        # Sélectionner les colonnes à analyser
        cols_to_corr = st.multiselect("Sélectionnez des colonnes pour analyser la corrélation", df.select_dtypes(exclude='object').columns, 
                                      default=['resultat_net','nombre_agence'])

        # Calculer et afficher la corrélation si deux colonnes sont sélectionnées
        if len(cols_to_corr) >= 2:
            
            # Afficher la matrice de corrélation avec une heatmap
            corr_matrix = df[cols_to_corr].corr()

            # Utiliser seaborn pour créer une heatmap
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, cbar_kws={'shrink': 0.8})
            
            # Afficher la heatmap dans Streamlit
            st.pyplot(plt)