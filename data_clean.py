"""
Python script to load and clean the data
@author: jartavia05
source: Historical results: https://www.kaggle.com/datasets/piterfm/football-soccer-uefa-euro-1960-2024

"""


from itertools import count
import pandas as pd


history = pd.read_csv('dataset/qualifying_1960-2024.csv')
teams = pd.unique(history['home_team'])

# Calculate the average goals
ave_home = history['home_score'].mean()
ave_away = history['away_score'].mean()
ave = history['home_score'].mean() + history['away_score'].mean()
