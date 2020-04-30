import pandas as pd
import numpy as np

columns = {'Unnamed: 0': 'id', 'Age (years)': 'age', 'Gender': 'gender',
           'Positive history of Parkinson disease in family': 'fam_hist',
           'Age of disease onset (years)': 'onset_age',
           'Duration of disease from first symptoms (years)': 'duration',
           'Antidepressant therapy': 'depress_med', 'Antiparkinsonian medication': 'pd_med',
           'Antipsychotic medication': 'psych_med', 'Benzodiazepine medication': 'benz_med',
           'Levodopa equivalent (mg/day)': 'levodopa', 'Clonazepam (mg/day)': 'clonazepam',
           'Hoehn & Yahr scale (-)': 'hy_scale', 'UPDRS III total (-)': 'updrs_total', '18. Speech': 'updrs_speech',
           '19. Facial Expression': 'updrs_face_exp', '20. Tremor at Rest - head': 'updrs_tremor_rest_head',
           '20. Tremor at Rest - RUE': 'updrs_trem_rest_RUE', '20. Tremor at Rest - LUE': 'updrs_trem_rest_LUE',
           '20. Tremor at Rest - RLE': 'updrs_trem_rest_RLE', '20. Tremor at Rest - LLE': 'updrs_trem_rest_LLE',
           '21. Action or Postural Tremor - RUE': 'updrs_trem_act_RUE',
           '21. Action or Postural Tremor - LUE': 'updrs_trem_act_LUE', '22. Rigidity - neck': 'updrs_rig_neck',
           '22. Rigidity - RUE': 'updrs_rig_RUE', '22. Rigidity - LUE': 'updrs_rig_LUE',
           '22. Rigidity - RLE': 'updrs_rig_RLE', '22. Rigidity - LLE': 'updrs_rig_LLE',
           '23.Finger Taps - RUE': 'updrs_taps_RUE', '23.Finger Taps - LUE': 'updrs_taps_LUE',
           '24. Hand Movements  - RUE': 'updrs_hand_RUE', '24. Hand Movements  - LUE': 'updrs_hand_LUE',
           '25. Rapid Alternating Movements - RUE': 'updrs_altmove_RUE',
           '25. Rapid Alternating Movements -  LUE': 'updrs_altmove_LUE', '26. Leg Agility - RLE': 'updrs_leg_RLE',
           '26. Leg Agility - LLE': 'updrs_leg_LLE', '27.  Arising from Chair ': 'updrs_rise_chair',
           '28. Posture': 'updrs_posture', '29. Gait': 'updrs_gait', '30. Postural Stability': 'updrs_post_stab',
           '31. Body Bradykinesia and Hypokinesia': 'updrs_brady_hypo', 'Entropy of speech timing (-)': 'pass_est',
           'Rate of speech timing (-/min)': 'pass_rst',
           'Acceleration of speech timing                                (-/min2)': 'pass_ast',
           'Duration of pause intervals (ms)': 'pass_dpi', 'Duration of voiced intervals (ms)': 'pass_dvi',
           'Gaping                          in-between voiced\nintervals  (-/min)': 'pass_gvi',
           'Duration of unvoiced stops (ms)': 'pass_dus',
           'Decay of unvoiced fricatives              (‰/min)': 'pass_duf',
           'Relative loudness of respiration (dB)': 'pass_rlr',
           'Pause intervals per respiration (-)': 'pass_pir',
           'Rate of speech respiration                (-/min)': 'pass_rsr',
           'Latency of\nrespiratory exchange (ms)': 'pass_lre',
           'Entropy of speech timing (-).1': 'mono_est', 'Rate of speech timing (-/min).1': 'mono_rst',
           'Acceleration of speech timing (-/min2)': 'mono_ast',
           'Duration of pause intervals (ms).1': 'mono_dpi',
           'Duration of voiced intervals (ms).1': 'mono_dvi',
           'Gaping                         in-between voiced\nintervals                   (-/min)': 'mono_gvi',
           'Duration of unvoiced stops (ms).1': 'mono_dus',
           'Decay of unvoiced fricatives              (‰/min).1': 'mono_duf',
           'Relative loudness of respiration (dB).1': 'mono_rlr',
           'Pause intervals per respiration (-).1': 'mono_pir',
           'Rate of speech respiration           (- /min)': 'mono_rsr',
           'Latency of\nrespiratory exchange (ms).1': 'mono_lre'
           }

def clean_data(df):
    # remove empty rows
    df = df.dropna()

    # rename columns
    df = df.rename(columns=columns)

    # remove columns with only 1 value
    def remove_cols(df):
        remove = []
        for col in df:
            if len(df[col].unique()) == 1:
                remove.append(col)
        df = df.drop(columns=remove)
        return df

    df = remove_cols(df)

    # rename and encode id column
    df['id'] = df['id'].str[:2]
    df = df.rename(columns={'id': 'status'})

    # encode categorical data
    encode = {'status': {'PD': 1, 'RB': 2, 'HC': 0},
              'gender': {'F': 0, 'M': 1},
              'fam_hist': {'No': 0, 'Yes': 1, '-': -1},
              'depress_med': {'No': 0, 'Yes (Aurorix)': 1, 'Yes (Trittico)': 2, 'Yes (Remood)': 3,
                              'Yes (Zoloft)': 4, 'Yes (Anafranil)': 5, 'Yes (Citalec)': 6,
                              'Yes (Velaxin)': 7, 'Yes (Asentra)': 8, 'Yes (Cipralex)': 9},
              'benz_med': {'No': 0, 'Yes (Rivotril)': 1, 'Yes (Xanax)': 2, 'Yes (Neurol)': 3}
              }
    df.replace(encode, inplace=True)

    # fill in rows with now data with nan
    df = df.replace('-', np.nan)

    # convert data types
    df['hy_scale'] = df['hy_scale'].astype(float)
    df['age'] = df['age'].astype(int)
    
    #create age range column
    bins = [30, 40, 50, 60, 70, 80, 90]
    labels = ['30-39', '40-49', '50-59', '60-69', '70-79','80+']
    df['age_range'] = pd.cut(df.age, bins, labels = labels,include_lowest = True)
    
    #rearrange columns
    cols = df.columns.tolist()
    cols = cols[:2] + cols[-1:] + cols[2:62]
    df_final = df[cols]

    return df_final



