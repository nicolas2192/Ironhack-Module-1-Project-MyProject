import pandas as pd


def bday(year):
    """
    :param year: year of birth
    :return: turns year of birth into age
    """
    if year is None:
        return None
    elif len(year) == 4:
        return str(2018 - int(year))
    else:
        return year[0:2]


def business_df(b):
    """
    :param b: Business_info dataframe
    :return: returns a clean dataframe
    """
    # Splitting Source column into two columns, Sector and Company
    b["Sector"] = b["Source"].str.split("==>").apply(lambda x: x[0]).apply(str.strip)
    b["Company"] = b["Source"].str.split("==>").apply(lambda x: x[1]).apply(str.strip)

    # Replacing "" BUSD" with "" and converting it into a float type
    b["Worth(BUSD)"] = b["worth"].str.replace(" BUSD", "").astype("float")

    # Dropping unnecessary columns
    b.drop(columns=["Unnamed: 0", "worthChange", "realTimeWorth", "realTimePosition", "Source", "worth"],
           axis=1, inplace=True)

    # Sorting by Worth column in ascending order.
    b.sort_values(by="Worth(BUSD)", ascending=False, inplace=True)

    # Saving file
    file_name = "business_info.csv"
    b.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

    return b


def personal_df(p):
    """
    :param p: Personal_info dataframe
    :return: returns a clean dataframe
    """
    # Replacing strings from the age series
    p["age"] = p["age"].str.replace(" years old", "")

    # applying user defined function bday
    p["age"] = p["age"].apply(bday)
    p.head()

    # Cleaning gender series. Turn F into Female, M into Male and None string into actual None.
    new_sex = {"F": "Female", "Female": "Female", "M": "Male", "Male": "Male", "None": None, None: None}
    p["gender"] = p["gender"].map(new_sex)

    # Deleting unnecessary columns.
    p.drop(columns=["lastName", "Unnamed: 0"], axis=1, inplace=True)

    # Switching some country names to improve data consistency
    p["country"].replace({"None": None}, inplace=True)
    p["country"].replace({"UAE": "United Arab Emirates"}, inplace=True)
    p["country"].replace({"UK": "United Kingdom"}, inplace=True)
    p["country"].replace({"USA": "United States"}, inplace=True)
    p["country"].replace({"People's Republic of China": "China"}, inplace=True)

    # ñapa, adding some gender info
    p.loc[p[p["id"] == 6547].index, "gender"] = "Female"
    p.loc[p[p["id"] == 8952].index, "gender"] = "Female"
    p.loc[p[p["id"] == 1120].index, "gender"] = "Male"
    p.loc[p[p["id"] == 2452].index, "gender"] = "Male"
    p.loc[p[p["id"] == 4284].index, "gender"] = "Male"
    p.loc[p[p["id"] == 6005].index, "gender"] = "Male"

    # Saving file
    file_name = "personal_info.csv"
    p.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

    return p


def rank_df(r):
    """
    :param r: Rank_info dataframe
    :return: returns a clean dataframe
    """
    # Removing unnecessary columns
    r.drop(columns=["position", "Unnamed: 0"], axis=1, inplace=True)

    # Formatting names to title case style
    r["name"] = r["name"].str.title()

    # ñapa. Changing "Charles Cohen" to "Charles S. Cohen"
    r.loc[r.loc[r["name"] == "Charles Cohen"].index, "name"] = "Charles S. Cohen"

    # Saving file
    file_name = "rank_info.csv"
    r.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

    return r


def putting_all_together(df1: "personal df", df2: " rank df", df3: "business df"):
    """
    :param df1: First dataframe, personal
    :param df2: Second dataframe, rank
    :param df3: Third dataframe, business
    :return: A merged dataframe
    """
    pr = pd.merge(df1, df2, how="inner", on="id")
    pr = pr[['id', 'name', 'age', 'gender', 'country', 'image']]
    prb = pd.merge(pr, df3, how="inner", on="id")

    # Saving file
    file_name = "dataclean_info.csv"
    prb.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

    return prb
