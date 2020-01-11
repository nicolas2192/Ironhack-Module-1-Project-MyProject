import pandas as pd
import requests
import re


def switching_countries(df):
    df["country"].replace({"None": None}, inplace=True)
    df["country"].replace({"U.A.E.": "United Arab Emirates"}, inplace=True)
    df["country"].replace({"U.K.": "United Kingdom"}, inplace=True)
    df["country"].replace({"England": "United Kingdom"}, inplace=True)
    df["country"].replace({"Wales": "United Kingdom"}, inplace=True)
    df["country"].replace({"U.S.": "United States"}, inplace=True)


def country_or_nationality(df: "country vs nationality dataframe",
                           mode: "c for country, n for nationality, b for both"):
    """
    :param df: country vs nationality dataframe
    :param mode: c for country, n for nationality, b for both
    :return: returns a list containing countries or nationalities
    """
    cn = df.values.tolist()
    coun, nati = zip(*cn)
    if mode == "c":
        return coun
    elif mode == "n":
        return nati
    elif mode == "b":
        return cn
    else:
        return None


def null_values(df, mode: "g, c or a", tolist=False):
    """
    :param df: Clean dataframe
    :param mode: g for gender, c for country and a for age
    :param tolist: creates a list of names from the dataframe
    :return: 1. returns a pandas dataframe with empty gender or country registries,
            depending on mode selection. If tolist is set to True, it will return a list of names
    """
    if mode == "g":
        # Creating dataframe with empty values
        nullgender = df[df["gender"].isnull()].iloc[:, :2]  # 550

        # Creating search name column. This column will be used to access each's millionaire wikipedia page.
        nullgender["SearchName"] = nullgender["name"].apply(lambda full_name: "_".join(full_name.strip().split()))

        if tolist:
            return nullgender["SearchName"].values.tolist()
        else:
            return nullgender

    elif mode == "c":
        # Creating dataframe with empty values
        nullcountry = df[df["country"].isnull()].iloc[:, :2]  # 1391

        # Creating search name column. This column will be used to access each's millionaire wikipedia page.
        nullcountry["SearchName"] = nullcountry["name"].apply(lambda full_name: "_".join(full_name.strip().split()))
        if tolist:
            return nullcountry["SearchName"].values.tolist()
        else:
            return nullcountry

    elif mode == "a":
        # Creating dataframe with empty values
        nullage = df[df["age"].isnull()].iloc[:, :2]  # 1391

        # Creating search name column. This column will be used to access each's millionaire wikipedia page.
        nullage["SearchName"] = nullage["name"].apply(lambda full_name: "_".join(full_name.strip().split()))
        if tolist:
            return nullage["SearchName"].values.tolist()
        else:
            return nullage
    else:
        return None


def search_list(df: "dataframe to parse"):
    return df["SearchName"].values.tolist()


def get_age(nums: "List of 19xx years"):
    if len(nums) == 1:
        return 2019 - int(nums[0])
    else:
        return None


def country_search(words: "list of words in Born tag", countries: "list of countries in countries tuple"):
    for word in words:
        for country in countries:
            if word == country:
                return country
    else:
        return None


def nationality_country(Natio: "Nationality to search", CvsN: "Country vs. Nationality relationship table"):
    for element in CvsN:
        if element[1] == Natio:
            return element[0]
    else:
        return None


def merge_enhanced_data(original_df, toadd_df, column_to_improve, column_to_drop):
    original_df["SearchName"] = original_df["name"].apply(lambda full_name: "_".join(full_name.strip().split()))
    enhanced_df = pd.merge(original_df, toadd_df, how="left", on="SearchName")
    for x in enhanced_df.index:
        if pd.isna(enhanced_df.loc[x, column_to_improve]):
            enhanced_df.loc[x, column_to_improve] = enhanced_df.loc[x, column_to_drop]
    enhanced_df.drop(columns=["SearchName", column_to_drop], axis=1, inplace=True)
    enhanced_df.rename(columns={column_to_drop: column_to_improve}, inplace=True)
    enhanced_df = enhanced_df[['id', 'name', 'age', 'gender', 'country', 'image', 'Sector', 'Company', 'Worth(BUSD)']]
    switching_countries(enhanced_df)
    print(f"dataframe was improved by adding new {column_to_improve} values")
    return enhanced_df


def data_enhancement(millionaires, enh_mode, con):
    """
    :param millionaires: List of millionaires to parse
    :param enh_mode: enhancement mode, c for country, a for age
    :param con: Country vs Nationality dataframe
    :return:
    """

    counter = 0
    mill_lst = []
    for millionaire in millionaires:
        url = f"https://en.wikipedia.org/wiki/{millionaire}"

        # Checking whether the page exists.
        if str(requests.get(url)) == "<Response [404]>":
            mill_lst.append((millionaire, None))
            counter += 1
            print(counter, millionaire, "<Response [404]>")
            continue

        # Checking if there are tables in the page.
        try:
            pd.read_html(url)
        except ValueError as err:
            mill_lst.append((millionaire, None))
            counter += 1
            print(counter, millionaire, err)
            continue

        # Accessing each's millionaire wikipedia page and turning first table into a list.
        wiki = pd.read_html(url)
        wikilist = wiki[0].values.tolist()

        # Data enhancing mode: COUNTRY.
        if enh_mode == "c":

            c = country_or_nationality(con, "c")
            cn = country_or_nationality(con, "b")

            # Looping each "tag" in table/list.
            for x in wikilist:

                # Getting country of origin in "Born" tag.
                if x[0] == "Born":
                    pattern_country = r"\bSouth\s[A-Za-z]+|New\s[A-Za-z]+|[A-Za-z]\.[A-Za-z]\.|[A-Za-z]+\b"
                    born_country = re.findall(pattern_country, x[1])
                    country_found = country_search(born_country, c)
                    if country_found is not None:
                        mill_lst.append((millionaire, country_found))
                        break

                # Getting country of origin in "Nationality" tag if it was not found in previous tag.
                elif x[0] == "Nationality":
                    nationality_found = nationality_country(x[1], cn)
                    if nationality_found is not None:
                        mill_lst.append((millionaire, nationality_found))
                        break

            # Setting country to None if it was not found.
            else:
                mill_lst.append((millionaire, None))

            counter += 1
            print(counter, millionaire, millionaires.index(millionaire), "    ",
                  mill_lst.index(mill_lst[len(mill_lst) - 1]), mill_lst[len(mill_lst) - 1])

        # Data enhancing mode: AGE
        elif enh_mode == "a":

            # Looping each "tag" in table/list.
            for x in wikilist:

                # Getting year of birth in "Born" tag.
                if x[0] == "Born":
                    # Looking for "age xx" string
                    pattern_age = r"age\s\d\d"
                    born_age = re.findall(pattern_age, x[1])
                    if len(born_age) == 1:
                        age_found = int(born_age[0][len(born_age[0]) - 2:len(born_age[0])])
                        mill_lst.append((millionaire, age_found))
                        break

                    # Looking for the year and computing current age
                    pattern_age = r"19\d\d"
                    born_age = re.findall(pattern_age, x[1])
                    age_found = get_age(born_age)
                    if age_found is not None:
                        mill_lst.append((millionaire, age_found))
                        break

            # Setting age to None if it was not found.
            else:
                mill_lst.append((millionaire, None))

            counter += 1
            print(counter, millionaire, millionaires.index(millionaire), "    ",
                  mill_lst.index(mill_lst[len(mill_lst) - 1]), mill_lst[len(mill_lst) - 1])

    if enh_mode == "c":
        enhanced_df = pd.DataFrame(mill_lst, columns=["SearchName", "Nationality"])
        file_name = "enhanced_nationality_df.csv"
        enhanced_df.to_csv(f"data/processed/{file_name}", index=False)
        print(f"{file_name} was successfully saved!")
        return enhanced_df
    elif enh_mode == "a":
        enhanced_df = pd.DataFrame(mill_lst, columns=["SearchName", "Age"])
        file_name = "enhanced_age_df.csv"
        enhanced_df.to_csv(f"data/processed/{file_name}", index=False)
        print(f"{file_name} was successfully saved!")
        return enhanced_df


# test = ['Bernard_Arnault', 'Amancio_Ortega', 'Alice_Walton', 'Jack_Ma', 'Steve_Ballmer', "Elon_Musk"]
# mike = ["Michael_Bloomberg"]
# bill = ["Bill_Gates", "Warren Buffett", 'Bernard_Arnault']
# chen = ["Charles_S._Cohen"]
#
# paises = pd.read_csv("../../data/processed/CountryNationality.csv")
# clean_df = pd.read_csv("../../data/processed/dataclean_info.csv")
#
# all_names = null_values(clean_df, "a", tolist=True)
#
# result = data_enhancement(test, "a", paises)
# print(result)
