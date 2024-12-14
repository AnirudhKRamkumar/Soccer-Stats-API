import pandas as pd
from io import StringIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import tkinter as tk
from pandastable import Table
import time

options = Options()
options.add_argument('--headless')  # Run in headless mode
options.add_argument('--ignore-certificate-errors')  # Ignore SSL certificate errors
options.add_argument('--incognito') 

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

def comp_stat_display(selected_stat="stats", season=None, comp='EUR', f_a_ind=None):
  
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

  driver = webdriver.Chrome(options=options)

  # Construct the URL based on the selected statistic and season   
  url_df = f"https://fbref.com/en/comps/{comps[2]}/{season}/{selected_stat}/players/{season}-{(comps[0].replace(' ', '-'))}-Stats"
   
  driver.get(url_df)
  
  WebDriverWait(driver, 100).until(EC.presence_of_all_elements_located((By.ID, f'stats_{selected_stat}')))
  page_source = driver.page_source
  tables = pd.read_html(StringIO(page_source))[-3:]
  driver.quit()
   
  if f_a_ind.lower() == "individual":
     # df = pd.read_html(url_df, attrs={"id": "stats_possession"})[0]
     df = tables[2]
     df = dataframe_cleaning(df, comp, "player")
     print(df.head())
  else:
    df = pd.read_html(url_df, flavor='bs4')[0]
   
    df = dataframe_cleaning(df, comp)
    
    if comp != "EUR":
      df2 = pd.read_html(url_df, flavor='bs4')[1]
      df2 = dataframe_cleaning(df2, comp)
      print(df.head())
      print(df2.head())
      if f_a_ind.lower() == "for":
        return df
      elif f_a_ind.lower() == "against":
        return df2
  
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


def dataframe_cleaning(dataframe, comp, type = "squad"):
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

  type : str
      Specifies whether the table displays squad stats or player stats. Both types require 
      different aspects to be cleaned.

  Returns:
  --------
  pandas.DataFrame
      The cleaned DataFrame with modified column names, missing values handled, and unnecessary columns removed.
  """
  dataframe = dataframe_name_replacement(dataframe)
  # Flatten multi-level column headers by joining them with a space and stripping any extra whitespace
  dataframe.columns = [' '.join(col).strip() for col in dataframe.columns]
  # Reset index to ensure it's a standard range index
  dataframe = dataframe.reset_index(drop=True)
  new_columns = []
  for col in dataframe.columns:
    if 'level_0' in col:
      new_col = col.split()[-1]  # takes the last name
    elif "Performance" in col:
      new_col = "Raw " + col.split()[-1]
    elif "Per 90 Minutes" in col:
      new_col = col.split()[-1] + "/90 Min"
    else:
      new_col = col.split()[1:]
      if isinstance(new_col, list):
        new_col = ' '.join(new_col)
    new_columns.append(new_col)
  # Apply new column names to the DataFrame
  dataframe.columns = new_columns

  if type.lower() == "squad":
    if comp == "EUR":
      # Split the 'Pos' column into 'Position' and 'Position_2' based on character positions
      dataframe['Position'] = dataframe['Pos'].str[:2]
      dataframe['Position 2'] = dataframe['Pos'].str[3:]


      # Extract country code from 'Nation' column
      dataframe['Nation'] = dataframe['Nation'].str.split(' ').str.get(1)

      # Extract league names from 'Comp' column
      dataframe['League'] = dataframe['Comp'].str.split(' ').str.get(1)
      dataframe['League_'] = dataframe['Comp'].str.split(' ').str.get(2)
      dataframe['League'] = dataframe['League'] + ' ' + dataframe['League_']

      # Drop unnecessary columns
      dataframe = dataframe.drop(columns=['League_', 'Comp', 'Rk', 'Pos', 'Matches'])
      dataframe = dataframe[dataframe['Player'] != 'Player']

      # Replace position abbreviations with full position names
      dataframe['Position'] = dataframe['Position'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
      dataframe['Position 2'] = dataframe['Position 2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})

      # Fill any remaining NaN values in 'League' column with 'Bundesliga'
      dataframe['League'] = dataframe['League'].fillna('Bundesliga')
    else:
      dataframe = dataframe.drop(columns=['Pl'])
  else:
    dataframe['Position 1'] = dataframe['Pos'].str[:2]
    dataframe['Position 2'] = dataframe['Pos'].str[3:]
    
    if comp != "ENG":
      dataframe['Age'] = dataframe['Age'].astype(str)
    dataframe['Age'] = dataframe['Age'].apply(lambda x: f"{x.split('-')[0]} years, {x[3:]} days")
    dataframe['Nation'] = dataframe['Nation'].str.split(' ').str.get(1)
    
    dataframe = dataframe[dataframe['Player'] != 'Player']
    dataframe = dataframe.drop(columns=['Born', 'Rk', 'Pos', 'Matches'])
    
    dataframe['Position 1'] = dataframe['Position 1'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
    dataframe['Position 2'] = dataframe['Position 2'].replace({'MF': 'Midfielder', 'DF': 'Defender', 'FW': 'Forward', 'GK': 'Goalkeeper'})
  for col in dataframe.columns:
    try:
      dataframe[col] = dataframe[col].astype(float)
      dataframe[col] = dataframe[col].apply(lambda x: int(x) if x.is_integer() else x)
    except ValueError:
      dataframe[col] = dataframe[col]
  return dataframe
  
def dataframe_name_replacement(dataframe):
  replacements = [["Nott'ham Forest", "Nottingham Forest"], ["Eint Frankfurt", "Eintracht Frankfurt"]]
  for item in replacements:
    dataframe = dataframe.replace(f"{item[0]}", f"{item[1]}")
    dataframe = dataframe.replace(f"vs {item[0]}", f"vs {item[1]}")
  return dataframe

# view the data
"""root = tk.Tk()
root.title("PandasTable Example")
frame = tk.Frame(root)
frame.pack(fill='both', expand=True)
df = comp_stat_display(comp='FRA', selected_stat ="misc", f_a_ind="individual")
pt = Table(frame, dataframe=df)
pt.show()
root.mainloop()"""