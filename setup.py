# This file will contain code you can call to get the data you want 
# presented as a list. 
import pandas as pd 

def get_china_dates():
  df = pd.read_csv('stripped_data/china-cases-deaths.csv')
  return list(df['date'])
  
def get_china_cases():
  df = pd.read_csv('stripped_data/china-cases-deaths.csv')
  return list(df['cases'])

def get_china_deaths():
  df = pd.read_csv('stripped_data/china-cases-deaths.csv')
  return list(df['deaths'])


def get_us_dates():
  df = pd.read_csv('stripped_data/us-cases-deaths.csv')
  return list(df['date'])

def get_us_cases():
  df = pd.read_csv('stripped_data/us-cases-deaths.csv')
  return list(df['cases'])

def get_us_deaths():
  df = pd.read_csv('stripped_data/us-cases-deaths.csv')
  return list(df['deaths'])


# Test
if __name__ == "__main__":
  print(get_china_dates())
  print(get_china_cases())
  print(get_china_deaths())
  print(get_us_dates())
  print(get_us_cases())
  print(get_us_deaths())
