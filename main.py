import pandas as pd

selected_stat = input("What stat? ")

url_df = f'https://fbref.com/en/comps/Big5/{selected_stat}/players/Big-5-European-Leagues-Stats'
df = pd.read_html(url_df)[0]

df.columns = [' '.join(col).strip() for col in df.columns]
df = df.reset_index(drop=True)

new_columns = []
for col in df.columns:
  if 'level_0' in col:
      new_col = col.split()[-1]  # takes the last name
  else:
      new_col = col
  new_columns.append(new_col)
# rename columns
df.columns = new_columns
df = df.fillna(0)
df['Age'] = df['Age'].str[:2]
df['Position_2'] = df['Pos'].str[3:]
df['Position'] = df['Pos'].str[:2]
df['Nation'] = df['Nation'].str.split(' ').str.get(1)
df['League'] = df['Comp'].str.split(' ').str.get(1)
df['League_'] = df['Comp'].str.split(' ').str.get(2)
df['League'] = df['League'] + ' ' + df['League_']
df = df.drop(columns=['League_', 'Comp', 'Rk', 'Pos','Matches'])

df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
df['League'] = df['League'].fillna('Bundesliga')
print(df.head())
