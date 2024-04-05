import streamlit as st
import pandas as pd


import helper
import preprocessor

df=pd.read_csv('athlete_events.csv')
df2=pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,df2)

st.sidebar.title("Olympics Analysis")
user_menu=st.sidebar.radio(
    'select an option',
    ('Medal Tally','Overall Analysis','Country-Wise Analysis','Athlete wise Analysis')
)

#st.dataframe(df)

if user_menu == "Medal Tally":
    st.sidebar.header('Medal Tally')
    year,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year',year)
    selected_country = st.sidebar.selectbox('Select Country', country)

    medal_tally = helper.fetch_medal_Tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title('Medal Tally in '+str(selected_year)+' Olympics')
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country+' Overall Performance')
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(selected_country + ' Performance in '+ str(selected_year) + " Olympics")

    st.table(medal_tally)