import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import numpy as np

import helper
import preprocessor
from PIL import Image
from rembg import remove

df=pd.read_csv('athlete_events.csv')
df2=pd.read_csv('noc_regions.csv')

df = preprocessor.preprocess(df,df2)

st.sidebar.title("Olympics Analysis")

input = Image.open("images5.png")
output = remove(input)
st.sidebar.image(output,width=300)

input1 = Image.open("images6.jpg")
output2 = remove(input1)
output.putalpha(70)
col1,col2,col3 = st.columns([20,10,20])
col2.image(output2,width=80)


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

    st.title("No. of Events Over Time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)

    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-Wise Analysis':
    st.sidebar.title('country-Wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country=st.sidebar.selectbox('Select a Country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + ' Medal Tally Over The Years')
    st.plotly_chart(fig)

    st.title(selected_country + ' excel in the following sports')
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)

    st.pyplot(fig)

    st.title('Top 10 Athletes of ' + selected_country )
    top10_df=helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis':

    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronzze  Medalist'],
                             show_hist=False, show_rug=False)
    fig.update_layout(xaxis_title='Age', yaxis_title='Count',autosize= False, width= 800,height= 600)
    st.title('Age Distribution')
    fig.show()
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Juddo', 'Football', 'Tug-Of-War', 'Athletics',
                      'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                      'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                      'Water Polo', 'Hockey', 'Rowing', 'Fencing', 'Equestrianism',
                      'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                      'Tennis', 'Golf', 'Softball', 'Archery',
                      'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                      'Rhythmic Gymnastics', 'Rugby Sevens', 'Trampolining',
                      'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo',
                      'Cricket', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        gold_ages = temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna()
        if not gold_ages.empty:
            x.append(gold_ages)
            name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(xaxis_title='Age', yaxis_title='Count',autosize= False, width= 800,height= 600)
    st.title('Distribution of Age wrt Sports')
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'],style=temp_df['Sex'],s=60)
    st.title("Height vs Weight")
    st.pyplot(fig)

    st.title('Men Vs Women Participation Over The Year')
    final = helper.men_vs_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    st.plotly_chart(fig)
