import pandas as pd
import tkinter as tk
from pandastable import Table
import time

european_leagues = [
    ("Premier League", "ENG", 9),
    ("La Liga", "SPA", 12),
    ("Serie A", "ITA", 11),
    ("Bundesliga", "GER", 20),
    ("Ligue 1", "FRA", 13),
    ("UEFA Champions League", "UCL", 8),
    ("UEFA Europa League", "UEL", 19),
    ("UEFA Conference League", "UECL", 882),
    ("Big 5 European Leagues", "EUR", "Big5")
]

def comp_stat_display(selected_stat="stats", season=None, comp='EUR', fa=None):
  
  # setting default arguments for 'season' because the conditions might change from the moment of initialization 
  if season is None:
      year = time.gmtime()[0]
      current_season = year if time.gmtime()[1] > 8 else (year - 1)
      season = f"{current_season}-{current_season+1}"

  # Some stats weren't tracked until the 2017-2018 season, allow the function to be recalled
  if int(season[0:4]) < 2017 and selected_stat == "":
    print("Sorry, but this stat wasn't tracked until the 2017-2018 season; only overall, goalkeeping, passing, shooting, and play time stats were tracked!")
    return None 

  for item in european_leagues:
    if comp == item[1]:
      comps = item

  # Construct the URL based on the selected statistic and season   
  url_df = f"https://fbref.com/en/comps/{comps[2]}/{season}/{selected_stat}/players/{season}-{(comps[0].replace(' ', '-'))}-Stats"
  
  df = pd.read_html(url_df, flavor='bs4')[0]
   
  _dataframe_cleaning(df, comp)
  
  if comp != "EUR":
    df2 = pd.read_html(url_df, flavor='bs4')[1]
    _dataframe_cleaning(df2, comp)
    print(df.head())
    print(df2.head())
    if fa.lower() == "for":
      return df
    elif fa.lower() == "against":
      return df2
   
  print(df.head())
  
  return df


def range_trimming(dataframe, column, condition, comparison=None):
  r"""
  Filters a pandas DataFrame based on a condition applied to a specific column.

  Parameters:
  ----------
  dataframe : pandas.DataFrame
      The DataFrame to be filtered.
  
  column : str
      The name of the column on which the condition will be applied.
  
  condition : int or str
      The value used to filter the DataFrame. If an integer is provided, the `comparison` 
      parameter must also be specified to determine whether to filter greater than or less than the value. 
      If a string is provided, the DataFrame will be filtered for exact matches in the specified column.
  
  comparison : str, optional
      The comparison operator for integer conditions. Can be '>' or '<'. This is ignored 
      if `condition` is a string. Default is None.

  Returns:
  -------
  pandas.DataFrame
      The filtered DataFrame based on the specified condition.
  """
  if isinstance(condition, int): 
    if comparison == ">":
      dataframe = dataframe[dataframe[column] > condition]
    elif comparison == '<':
      dataframe = dataframe[dataframe[column] < condition]
  elif isinstance(condition, str):
    dataframe = dataframe[dataframe[column] == condition]
  print(dataframe.head())
  return dataframe


def _dataframe_cleaning(df, comp):
  r"""
  Cleans and processes a pandas DataFrame by renaming columns, handling missing values, 
  and extracting or modifying certain data based on the competition type.

  Parameters:
  -----------
  df : pandas.DataFrame
      The DataFrame to be cleaned. Expected to have multi-level columns and specific columns 
      like 'Pos', 'Nation', and 'Comp' for additional processing.
  
  comp : str
      Specifies the competition type. If "EUR", the function performs additional cleaning 
      and extraction of position and league data. Otherwise, a different cleaning process is applied.

  Returns:
  --------
  pandas.DataFrame
      The cleaned DataFrame with modified column names, missing values handled, and unnecessary columns removed.
  """
  # Flatten multi-level column headers by joining them with a space and stripping any extra whitespace
  df.columns = [' '.join(col).strip() for col in df.columns]
  # Reset index to ensure it's a standard range index
  df = df.reset_index(drop=True)
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

  if comp == "EUR":
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
  else:
    df = df.drop(columns=['Pl'])
  
  


# view the data
root = tk.Tk()
root.title("PandasTable Example")
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)
df = comp_stat_display(comp='ENG', fa="against")
pt = Table(frame, dataframe=df)
pt.show()
root.mainloop()