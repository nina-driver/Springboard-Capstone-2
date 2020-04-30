import pandas as pd

def percentages(factor, df):
    p_list = factor.tolist()
    new_list = []
    for num in p_list:
        new_list.append(('{:.2%}'.format((num / len(df)))))
    return new_list