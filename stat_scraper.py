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
  
  """COME BACK TO THIS"""
  
  if int(season[0:4]) < 2017 and selected_stat == "":
    print("Sorry, but this stat wasn't tracked until the 2017-2018 season; only overall, goalkeeping, passing, shooting, and play time stats were tracked!")
    return None 

  # Construct the URL based on the selected statistic and season   
  url_df = f"https://fbref.com/en/comps/Big5/{season}/{selected_stat}/players/{season}-Big-5-European-Leagues-Stats"

  
  # Read the HTML table from the URL into a list of DataFrames and select the first DataFrame
  df = pd.read_html(url_df)[0]
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

  # Replace position abbreviations with full position names
  df['Position'] = df['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
  df['Position_2'] = df['Position_2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})

  # Fill any remaining NaN values in 'League' column with 'Bundesliga'
  df['League'] = df['League'].fillna('Bundesliga')
  
  #for item in european_leagues:
    #if comp
  
  print(df.head())
  
  return df


def range_trimming(dataframe, column, condition, comparison=None):
  if isinstance(condition, int): 
    if comparison == ">":
      dataframe = dataframe[dataframe[column] > condition]
    elif comparison == '<':
      dataframe = dataframe[dataframe[column] < condition]
  elif isinstance(condition, str):
    dataframe = dataframe[dataframe[column] == condition]
  print(dataframe.head())
  return dataframe

df = comp_stat_display()
