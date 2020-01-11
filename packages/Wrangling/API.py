import pandas as pd
import requests


def api_search_list(df_clean, df_CC, tolist=True):
    """
    :param df_clean:
    :param df_CC:
    :param tolist: sets what to return
    :return: a pandas dataframe or list
    """
    df_clean = df_clean[["id", "name", "gender", "country"]].copy()
    fn = df_clean[df_clean["gender"].isnull()].copy()
    fn["first_name"] = fn["name"].apply(lambda full_name: full_name.strip().split()[0])
    merged_df = pd.merge(fn, df_CC, how="left", on="country")
    merged_df["accuracy"] = 0
    if tolist:
        return merged_df.values.tolist()
    else:
        return merged_df


def api_search(api_search_lst, todf=False):
    for x in range(len(api_search_lst)):
        """
        [3808, 'Bernard Arnault', nan, 'France', 'Bernard', 'FR', 0]
        [id, 'Full Name', Gender, 'Country', 'First Name', 'Code', Accuracy]
        """
        name = api_search_lst[x][4]
        code = api_search_lst[x][5]

        toprint = api_search_lst[x]
        print(toprint)
        if pd.notnull(code):
            r = requests.get(f"https://api.genderize.io?name={name}&country_id={code}")
        else:
            r = requests.get(f"https://api.genderize.io?name={name}")

        if pd.isnull(r.json()["gender"]):
            api_search_lst[x][2] = r.json()["gender"]
            api_search_lst[x][6] = r.json()["probability"]
        else:
            api_search_lst[x][2] = r.json()["gender"].capitalize()
            api_search_lst[x][6] = r.json()["probability"]

    if todf:
        cols = ['id', 'name', 'new_gender', 'country', 'first_name', 'code', 'accuracy']
        fulldf = pd.DataFrame(api_search_lst, columns=cols)
        df = fulldf[["id", "new_gender", "accuracy"]].copy()
        return df
    else:
        return api_search_lst


def merge_enhanced_gender(clean_df, toadddf):
    data_enhanced_gender = pd.merge(clean_df, toadddf, how="left", on="id")
    for x in data_enhanced_gender.index:
        if pd.isna(data_enhanced_gender.loc[x, "gender"]):
            data_enhanced_gender.loc[x, "gender"] = data_enhanced_gender.loc[x, "new_gender"]
    data_enhanced_gender.drop(columns=["new_gender", "accuracy"], axis=1, inplace=True)
    file_name = "enhanced_gender_df.csv"
    data_enhanced_gender.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")
    return data_enhanced_gender


# df = pd.read_csv("/home/nicolas/ironhack/Ironhack-Module-1-Project-MyProject/data/processed/clean_df_enhanced_test.csv")
# lst = [[3808, 'David Thomson', None, None, 'David', None, 0]]

