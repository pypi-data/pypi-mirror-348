import pandas as pd


def score(row, legacy=False):
    try:
        return row["location_selected_delta"] <= 75
    except Exception as e:
        print(f"Error processing row: {e}")
        return None


def summarize(x, trials_expected=20, rt_outlier_low=100, rt_outlier_high=10000):

    d = {}
    # ----- Common Identifiers Start
    # -----
    # THIS MUST BE IN EVERY SCORING SCRIPT
    d["activity_begin_iso8601_timestamp"] = x["activity_begin_iso8601_timestamp"].iloc[0]
    # trial counts and validation checks
    d["n_trials"] = x["trial_index"].nunique()
    # ----

    # trial counts (for various denominators)
    d["n_trials_correct"] = sum(x["metric_accuracy"] == True)
    

    # Check if trials match expectations
    d["flag_trials_match_expected"] = d["n_trials_total"] == trials_expected
    
    # ----- Common Identifiers End
    
    # ----- Summary Scores Start

    # tabulate accuracy
    
    
    # Filter out outliers: RT < 100 ms or RT > 10,000 ms
    rt_filtered_color = x.loc[
        (x["color_selection_response_time_ms"] >= rt_outlier_low)
        & (x["color_selection_response_time_ms"] <= rt_outlier_high),
        "color_selection_response_time_ms",
    ]
    d["median_response_time_color_filtered"] = rt_filtered_color.median()

    rt_filtered_location = x.loc[
        (x["location_selection_response_time_ms"] >= rt_outlier_low)
        & (x["location_selection_response_time_ms"] <= rt_outlier_high),
        "location_selection_response_time_ms",
    ]
    d["median_response_time_location_filtered"] = rt_filtered_location.median()    
    
    #To-do
    # get RTs for correct and incorrect trials
    # d["median_response_time_overall"] = x["response_time_duration_ms"].median()
    # d["median_response_time_correct"] = x.loc[
    #     (x["user_response_index"] == x["correct_response_index"]),
    #     "response_time_duration_ms",
    # ].median()
    # d["median_response_time_incorrect"] = x.loc[
    #     (x["user_response_index"] != x["correct_response_index"]),
    #     "response_time_duration_ms",
    # ].median()

    # return as series
    indices = list(d.keys())
    return pd.Series(
        d,
        index=indices,
    )
    
    # ----- Summary Scores End
