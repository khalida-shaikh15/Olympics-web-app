
import numpy as np


def fetch_medal_Tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    temp_df = medal_df
    if year == "Overaall" and country == "Overall":
        temp_df = medal_df
    if year == "Overall" and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != "Overall" and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != "Overall" and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]
    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    return x


def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                                ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']

    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    year.sort()
    year.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return year,country

def nations_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('Year')
    nations_over_time = nations_over_time.rename(columns={'Year': 'Editions', 'count':col})
    return nations_over_time


def most_successful(df, Sport):
    temp_df = df.dropna(subset=['Medal'])

    if Sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == Sport]

    x = temp_df['Name'].value_counts().head(15).reset_index().merge(df, how='left')[['Name', 'count','Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={ 'count': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, region):
    temp_df = df.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == region]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df, how='left')[
        [ 'Name','count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={ 'count': 'Medals'}, inplace=True)
    return x

