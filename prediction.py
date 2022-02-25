import pandas as pd 
import joblib
from tensorflow.keras.utils import to_categorical

# Create function to clean inputs for ML prediction

def clean_cols(fighter1, fighter2):
    B_column_list = ["B_fighter",
                    "B_wins",
                    "B_losses",
                    "B_draw",
                    "B_current_lose_streak",
                    "B_current_win_streak",
                    "B_avg_SIG_STR_landed",
                    "B_avg_SIG_STR_pct",
                    "B_avg_SUB_ATT",
                    "B_avg_TD_landed",
                    "B_avg_TD_pct",
                    "B_longest_win_streak",
                    "B_total_rounds_fought",
                    "B_total_title_bouts",
                    "B_win_by_Decision_Majority",
                    "B_win_by_Decision_Split",
                    "B_win_by_Decision_Unanimous",
                    "B_win_by_KO/TKO",
                    "B_win_by_Submission",
                    "B_win_by_TKO_Doctor_Stoppage",
                    "B_age",
                    "B_Stance"
                    ]

    R_column_list = ["R_fighter",
                    "R_wins",
                    "R_losses",
                    "R_draw",
                    "R_current_lose_streak",
                    "R_current_win_streak",
                    "R_avg_SIG_STR_landed",
                    "R_avg_SIG_STR_pct",
                    "R_avg_SUB_ATT",
                    "R_avg_TD_landed",
                    "R_avg_TD_pct",
                    "R_longest_win_streak",
                    "R_total_rounds_fought",
                    "R_total_title_bouts",
                    "R_win_by_Decision_Majority",
                    "R_win_by_Decision_Split",
                    "R_win_by_Decision_Unanimous",
                    "R_win_by_KO/TKO",
                    "R_win_by_Submission",
                    "R_win_by_TKO_Doctor_Stoppage",
                    "R_age",
                    "R_Stance"
                    ]

    new_column_list = ["name",
                    "wins",
                    "losses",
                    "draw",
                    "current_lose_streak",
                    "current_win_streak",
                    "avg_SIG_STR_landed",
                    "avg_SIG_STR_pct",
                    "avg_SUB_ATT",
                    "avg_TD_landed",
                    "avg_TD_pct",
                    "longest_win_streak",
                    "total_rounds_fought",
                    "total_title_bouts",
                    "win_by_Decision_Majority",
                    "win_by_Decision_Split",
                    "win_by_Decision_Unanimous",
                    "win_by_KO/TKO",
                    "win_by_Submission",
                    "win_by_TKO_DoctoStoppage",
                    "age",
                    "Stance"
                    ]
    
    R_col_replace = {}
    B_col_replace = {}
    R_count = 0
    B_count = 0

    for header in new_column_list:
        R_col_replace[header] = R_column_list[R_count]
        R_count +=1

    for header in new_column_list:
        B_col_replace[header] = B_column_list[B_count]
        B_count +=1

    fighter1 = fighter1[new_column_list]
    fighter1 = fighter1.rename(columns = B_col_replace)
    fighter1 = fighter1.drop("B_fighter", axis = 1)
    fighter2 = fighter2[new_column_list]
    fighter2 = fighter2.rename(columns = R_col_replace)
    fighter2 = fighter1.drop("R_fighter", axis = 1)

    return fighter1, fighter2


# Create function to predict fight winner
def predict(fighter1, fighter2):

    # load model binaries 
    model = joblib.load("ml_models/model.sav")
    X_scaler = joblib.load("ml_models/x_scaler.sav")
    
    # combine data into one dataframe 
    input_data = pd.concat([fighter1,fighter2], axis = 1, ignore_index = True)

    # scale the X input df 
    X_scaled = X_scaler.transform(input_data)

    # obtain prediction (y) 
    prediction = model.predict(X_scaled)
    
    # Return prediction
    return prediction