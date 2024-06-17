"""
Python script to predict a English Premier League match result based on poisson distribution
@author: jartavia05

"""

from data_clean import history
from scipy.stats import poisson
import matplotlib.pyplot as plt
import pandas as pd


def get_match_score(home, away, nsim):
    teams_history = history.loc[(history['home_team'] == home) & (history['away_team'] == away) ]
    ave_h_s = 0 if teams_history['home_score'].empty else teams_history['home_score'].mean()
    ave_a_s = 0 if teams_history['away_score'].empty else teams_history['away_score'].mean()

    # Stats of the Home Team
    t_ave_h_s = 0 if teams_history['home_score'].empty else teams_history['home_score'].loc[history['home_team'] == home].mean()
    t_ave_h_c = 0 if teams_history['away_score'].empty else teams_history['away_score'].loc[history['home_team'] == home].mean()

    # Stats of the Away Team
    t_ave_a_s = 0 if teams_history['away_score'].empty else teams_history['away_score'].loc[history['away_team'] == away].mean()
    t_ave_a_c = 0 if teams_history['home_score'].empty else teams_history['home_score'].loc[history['away_team'] == away].mean()
  
    h_goal = []
    a_goal = []
    score_pred = []
    score_prob = []
    h_goal_prob = []
    a_goal_prob = []
    m_result = []

    for i in range(nsim):                   
        for j in range(nsim):
            h_goal.append(i)
            a_goal.append(j)
            if i > j:
                m_result.append('H')
            elif i == j:
                m_result.append('D')
            else:
                m_result.append('A')

            if len(teams_history) > 3 :
                h_goal_prob.append(poisson.pmf(k=i,mu=ave_h_s))
                a_goal_prob.append(poisson.pmf(k=j,mu=ave_a_s))
                score_pred.append('"{}-{}"'.format(i,j))
                score_prob.append(poisson.pmf(k=i,mu=ave_h_s) + poisson.pmf(k=j,mu=ave_a_s))
            else:  # take into account both attacking stat of home and defense stats of away
                h_goal_prob.append(poisson.pmf(k=i,mu=(1/2 * (t_ave_h_s + t_ave_a_c))))
                a_goal_prob.append(poisson.pmf(k=j,mu=(1/2 * (t_ave_a_s + t_ave_h_c))))
                score_pred.append('"{}-{}"'.format(i,j))
                score_prob.append(poisson.pmf(k=i,mu=(1/2 * (t_ave_h_s + t_ave_a_c))) + poisson.pmf(k=j,mu=(1/2 * (t_ave_a_s + t_ave_h_c))))
    
    match_score = pd.DataFrame({'Home': home,'home_score': h_goal, 'home_prob': h_goal_prob,'Away': away,'away_score': a_goal,'away_prob':a_goal_prob,'score_pred': score_pred,'m_result':m_result, 'prob': score_prob}).sort_values(by='prob', ascending=False).head(10)
    match_score.to_csv('match_simulate_{}_vs_{}.csv'.format(home, away))
    return match_score
        
match_simulate = get_match_score('Austria','France', 6)
print(match_simulate)

