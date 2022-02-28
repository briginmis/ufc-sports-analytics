import pandas as pd 
import joblib

# Create function to clean inputs for ML prediction

def clean_cols(fighter1:pd.DataFrame, fighter2:pd.DataFrame):
    # Create lists to clean column headers
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
                    "B_Stance",
                    "B_Height_cms",
                    "B_Reach_cms"
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
                    "R_Stance",
                    "R_Height_cms",
                    "R_Reach_cms"
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
                    "Stance",
                    "Height_cms",
                    "Reach_cms"
                    ]
    
    R_col_replace = {}
    B_col_replace = {}
    R_count = 0
    B_count = 0

    # Create dictionaries to replace column headers
    for header in new_column_list:
        R_col_replace[header] = R_column_list[R_count]
        R_count +=1

    for header in new_column_list:
        B_col_replace[header] = B_column_list[B_count]
        B_count +=1

    # Clean dataframe columns using dictionaries
    fighter1 = fighter1[new_column_list]
    fighter1 = fighter1.rename(columns = B_col_replace)

    fighter2 = fighter2[new_column_list]
    fighter2 = fighter2.rename(columns = R_col_replace)

    return fighter1, fighter2


# Create function to predict fight winner
def predict(fighter1:pd.DataFrame, fighter2:pd.DataFrame):

    # load model binaries 
    model = joblib.load("ml_models/model.sav")
    X_scaler = joblib.load("ml_models/x_scaler.sav")
    features = joblib.load("ml_models/features.sav")

    # clean dataframes for inputs
    fighter1_input = fighter1.drop("B_fighter", axis = 1).reset_index(drop = True)
    fighter2_input = fighter2.drop("R_fighter", axis = 1).reset_index(drop = True)

    # combine data into one dataframe 
    combined_df = pd.concat([fighter1_input,fighter2_input], axis = 1)

    # Create dataframe using features
    features_df = pd.DataFrame(columns=features, index = [0])

    # Use pandas to get dummies
    X = pd.get_dummies(combined_df)

    # Combine features df and X_scaled df
    input_df = pd.merge(features_df, X, how = "outer").drop(labels = 0, axis = 0)
    input_df = input_df.fillna(0)
    input_df

    # scale the X input df 
    X_scaled = X_scaler.transform(input_df)

    # obtain prediction (y) 
    prediction = model.predict(X_scaled)

    if prediction[0] == 0:
        winner = fighter1["B_fighter"]
    else:
        winner = fighter2["R_fighter"]
    
    # Return prediction
    return winner