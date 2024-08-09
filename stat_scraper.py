import pandas as pd
import time

european_leagues = [
    ("Premier League", "ENG"),
    ("La Liga", "SPA"),
    ("Serie A", "ITA"),
    ("Bundesliga", "GER"),
    ("Ligue 1", "FRA"),
    ("UEFA Champions League", "UCL"),
    ("UEFA Europa League", "UEL", 19),
    ("UEFA Conference League", "UECL", 882)
]

def comp_stat_display(selected_stat="stats", season=None, comp='EUR'):
  
  # setting default arguments for 'season' because the conditions might change from the moment of initialization 
  if season is None:
      year = time.gmtime()[0]
      current_season = year if time.gmtime()[1] > 8 else (year - 1)
      season = f"{current_season}-{current_season+1}"

  # Some stats weren't tracked until the 2017-2018 season, allow the function to be recalled
  if int(season[0:4]) < 2017 and selected_stat == "":
    print("Sorry, but this stat wasn't tracked until the 2017-2018 season; only overall, goalkeeping, passing, shooting, and play time stats were tracked!")
    return None
 
  # Find out which competition the user wants to see by using the european_leagues list
  for item in european_leagues:
    if comp.upper() == item[1]:
      comps = [item[2]]
      break

  #if "EUR" not in comp:

  # Construct the URL based on the selected statistic   
  url_df = f"https://fbref.com/en/comps/Big5/{season}/{selected_stat}/players/{season}-Big-5-European-Leagues-Stats"
  print(f"Number of tables found: {len(pd.read_html(url_df))}")

  
  # Read the HTML table from the URL into a list of DataFrames and select the first DataFrame
  df = pd.read_html(url_df)[0]
  df.to_html('hello.html')
  # Flatten multi-level column headers by joining them with a space and stripping any extra whitespace
  df.columns = [' '.join(col).strip() for col in df.columns]
  # Reset index to ensure it's a standard range index
  df = df.reset_index(drop=True)
  
  # Rename columns to simplify the names by removing 'level_0' and keeping the last part
  new_columns = []
  for col in df.columns:
      if 'level_0' in col or 'Playing Time' in col or 'Progression' in col:
        new_col = col.split()[-1]  # takes the last name
      elif "Performance" in col:
        new_col = "Raw " + col.split()[-1]
      elif "Per 90 Minutes" in col:
        new_col = col.split()[-1] + "/90 Min"
      else:
        new_col = col
      new_columns.append(new_col)
  # Apply new column names to the DataFrame
  df.columns = new_columns

  # Fill any NaN values with 0
  df = df.fillna(0)
  # Split the 'Pos' column into 'Position' and 'Position_2' based on character positions

  df['Position'] = df['Pos'].str[:2]
  df['Position_2'] = df['Pos'].str[3:]


  # Extract country code from 'Nation' column
  df['Nation'] = df['Nation'].str.split(' ').str.get(1)

  # Extract league names from 'Comp' column
  df['League'] = df['Comp'].str.split(' ').str.get(1)
  df['League_'] = df['Comp'].str.split(' ').str.get(2)
  df['League'] = df['League'] + ' ' + df['League_']

  # Drop unnecessary columns
  df = df.drop(columns=['League_', 'Comp', 'Rk', 'Pos', 'Matches'])
  df = df[df['Player'] != 'Player']
  df = df.drop([0])

  # Replace position abbreviations with full position names
  df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
  df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})

  # Fill any remaining NaN values in 'League' column with 'Bundesliga'
  df['League'] = df['League'].fillna('Bundesliga')

  a = range_trimming(df, -1, "Bundesliga")

  # Print the first few rows of the processed DataFrame
  
  print(a)
  
  return df


def range_trimming(dataframe, column, condition, comparison=None):
  trimmed = []
  for row in dataframe.iterrows():
    row = row[1]
    if abs(column) in range(len(row)):
      if isinstance(condition, int): 
        value = row[column]
        try:
          if comparison == ">":
            if int(value) > condition:
              if value not in trimmed:
                trimmed.append(row[0])
          elif comparison == '<':
            if int(value) < condition:
              if value not in trimmed:
                trimmed.append(row[0])
        except ValueError:
            # Skip rows where conversion to integer fails
            continue
      elif isinstance(condition, str):
        value = row[column]
        try:
          if value == condition:
            if row[0] not in trimmed:
              trimmed.append(row[0])
        except ValueError:
          continue
  print(trimmed)

df = comp_stat_display()
