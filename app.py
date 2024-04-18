import pandas as pd
import streamlit as st
import plotly.express as px


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

if user_menu=='Overall Analysis':
    editions= df['Year'].unique().shape[0] - 1
    cities= df['City'].unique().shape[0]
    sports= df['Sport'].unique().shape[0]
    events= df['Event'].unique().shape[0]
    athletes= df['Name'].unique().shape[0]
    nations= df['region'].unique().shape[0]
    st.title('Top Statistics')
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1,col2,col3 = st.columns(3)
    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Nations')
        st.title(nations)
    with col3:
        st.header('Athletes')
        st.title(athletes)
    nations_over_time=helper.nations_over_time(df,'region')
    fig = px.line(nations_over_time, x='Editions', y='region')
    fig.update_layout(xaxis_title='Year',yaxis_title='Nations_Over_Time')
    st.title('Participating Nations Over Time')
    st.plotly_chart(fig)

    Events_over_time=helper.nations_over_time(df,'Event')
    fig = px.line(Events_over_time, x='Editions', y='Event')
    fig.update_layout(xaxis_title='Year', yaxis_title='Events_Over_Time')
    st.title('Participating Events Over Time')
    st.plotly_chart(fig)

    athlete_over_time=helper.nations_over_time(df,'Name')
    fig = px.line(athlete_over_time, x='Editions', y='Name')
    fig.update_layout(xaxis_title='Year', yaxis_title='Athletes_Over_Time')
    st.title('Participating Athletes Over Time')
    st.plotly_chart(fig)

