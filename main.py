import pandas as pd
df_winter = pd.read_csv("folder_csv/winter.csv")
df_summer = pd.read_csv("folder_csv/summer.csv")
df_main = pd.read_csv("folder_csv/dictionary.csv")

df_summer = df_summer.rename(columns={'Country': 'Code'})
df_winter = df_winter.rename(columns={'Country': 'Code'})


df_summer['season'] = 'summer'
df_winter['season'] = 'winter'
df_summer_main = pd.merge(df_main, df_summer, how='outer', on='Code')
df_winter_main = pd.merge(df_main, df_winter, how='outer', on='Code')

df_general = pd.merge(df_summer_main, df_winter_main, how='outer', on=['Country', 'Code', 'Population', 'GDP per Capita', 'Year', 'City', 'Sport', 'Discipline', 'Athlete', 'Gender', 'Event', 'Medal', 'season'])
df_general = df_general[['Country', 'Code', 'Population', 'GDP per Capita', 'City', 'Sport', 'Discipline', 'Athlete', 'Gender', 'Event', 'Medal', 'season']]

df_general = df_general.dropna(axis=0, how='any')

new_df = df_general[['Country', 'Code', 'Population', 'GDP per Capita', 'season', 'Medal']]
new_df['number_medals'] = 1
df_general['win'] = 1

df_medals = new_df.groupby(['Code', 'Country', 'Population'])['number_medals'].count().reset_index()
df_medals['percentage_of_medalists'] = df_medals['number_medals'] / df_medals['Population'] * 100
print(df_medals)


country_info = new_df.groupby(['Code', 'Population', 'GDP per Capita', 'season', 'Medal'])['number_medals'].count()
print(country_info)

win_table = df_general.groupby(['Code', 'season', "Discipline"])['win'].count().reset_index()

max_win = win_table.groupby(['Code', 'season', "Discipline"])['win'].max().reset_index()
max_wins = win_table.groupby(['Code', 'Discipline', 'season'])['win'].sum().reset_index()
idx = max_wins.groupby(['Code', 'season'])['win'].idxmax()
table_results = max_wins.loc[idx, ['Code', 'season', 'Discipline', 'win']].reset_index()

new_table = pd.merge(df_medals, table_results, on=['Code'])
new_table.drop('index', axis=1, inplace=True)
new_table.rename(columns={'Discipline': 'top_discipline', 'win': 'number_of_victories_in_top_discipline'}, inplace=True)
new_table.to_excel('pandas_excel.xlsx')
df_medals.to_excel('pandas_medals_info.xlsx')
