import pandas as pd 

def extract_us():
  # Load US database and add all state counts together
  us_df = pd.read_csv('og_data/us-states.csv')
  us_df = us_df.groupby(['date'])['date', 'cases', 'deaths'].sum()

  us_df['new_cases'] = us_df['cases'] - us_df['cases'].shift(1)
  us_df['new_cases'].iloc[0] = us_df['cases'].iloc[0]  # First day new cases is just case number
  us_df['new_deaths'] = us_df['deaths'] - us_df['deaths'].shift(1)
  us_df['new_deaths'].iloc[0] = us_df['deaths'].iloc[0]  # First day new deaths is just death number

  us_df.to_csv('./stripped_data/us-cases-deaths.csv')

def extract_china():
  # Load world database, extract China and rename columns to match above
  world_df = pd.read_csv('og_data/world-covid-data.csv')
  china_df = world_df[world_df['location'] == 'China']\
    [['date', 'total_cases', 'total_deaths', 'new_cases', 'new_deaths']]
  china_df.columns = ['date', 'cases', 'deaths', 'new_cases', 'new_deaths']
  china_df.to_csv('./stripped_data/china-cases-deaths.csv')

if __name__ == "__main__":
  extract_us()
  extract_china()