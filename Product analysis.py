import pandas as pd
def convert_csv_to_df(csv_name, source_type):
    """converts a csv into dataframe with a column for the source
    args:
    csv_name(str): name of NPS csv file
    source_type(str): source of the NPS responses
    return:
    dataframe with csv data and column: source
    """
    df_NPS = pd.read_csv(csv_name)
    df_NPS['source'] = source_type
    df_NPS['nps_group'] = df_NPS['nps_rating'].apply(categorise_nps)
    return df_NPS
#convert_csv_to_df("datasets/2020Q4_nps_mobile.csv", "mobile")

def check_csv(csv_name):
    """check if the csvfile include three colnums: response_date, user_id, nps_rating
    args: csv_name
    return: True/ False
    """
    with open(csv_name) as f:
        first_line = f.readline()
        if first_line == 'response_date, user_id, nps_rating':
            return True
        else:
            return False
#check_csv("datasets/corrupted.csv") # test on a error file

def combine_nps_csv(csv_dict):
    """
    to combine the files and sources in dictionary to dataframe
    args: csv_name
    return: dataframe
    """
    combined = pd.DataFrame()
    for csv_name, source_type in csv_dict.items():
        if check_csv(csv_name):
            dataframe_NPS = convert_csv_to_df(csv_name, source_type)
            combined = pd.concat([combined, dataframe_NPS])
        else:
            print(f"{csv_name} is not a valid file to be added")
        return combined
#files_dict = {'nps_email.csv': 'email', 'nps_mobile.csv': 'mobile', 'nps_web.csv': 'web'}
#combine_nps_csv(files_dict)

def categorise_nps(rating):
    """To link score with the category
    args: rates from customers
    return: categorise
    """
    if rating >= 0 and rating <= 6:
        return 'detractor'
    elif 7 <= rating <= 8:
        return 'passive'
    elif 9 <= rating <= 10:
        return 'promotor'
    else:
        return 'invalid'
#categorise_nps(8)

def calculate_nps_score(combined_nps_df):
    """
    to calculate the score
    args: result of combination
    return: score
    """
    counts = combined_nps_df['nps_group'].value_counts()
    detractor = counts['detractor']
    passive = counts['passive']
    promotor = counts['promotor']
    total = counts.sum()
    return ((promotor - detractor)/total) * 100

#files_dict = {'nps_email.csv': 'email', 'nps_mobile.csv': 'mobile', 'nps_web.csv': 'web'}
#q4_nps = combine_nps_csv(files_dict)
#calculate_nps(q4_nps)

def calculate_nps_by_source(combined_nps_df):
    """
    to show scores by different source type
    args: result of combination
    return: score for source type
    """
    score = combined_nps_df.groupby(['source']).apply(calculate_nps_score)
    return score
#files_dict = {'nps_email.csv': 'email', 'nps_mobile.csv': 'mobile', 'nps_web.csv': 'web'}
#q4_nps = combine_nps_csv(files_dict)
#calculate_nps_score(q4_nps)

