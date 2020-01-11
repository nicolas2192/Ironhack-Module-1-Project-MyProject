import pandas as pd


def country_nationality_table():
    """
    This function reads from the web a table with countries and nationalities.
    Output: Clean pandas dataframe
    """
    # Reading the table from a webpage
    tables = pd.read_html("https://www.vocabulary.cl/Basic/Nationalities.htm")
    con = tables[1]

    # Cleaning the table
    con["Country"].replace("Colombia *", "Colombia", inplace=True)
    con["Country"].replace("(The) United Kingdom", "United Kingdom", inplace=True)
    con["Country"].replace("(The) United States", "United States", inplace=True)
    con[r"Nationality  (Adjective)"].replace("American **", "American", inplace=True)

    # Creating new Nationality column by copying it
    con["Nationality"] = con[r"Nationality  (Adjective)"]

    # Fixing Argentina
    con.drop(index=3, inplace=True)
    con = con.append({"Country": "Argentina", "Nationality": "Argentine"}, ignore_index=True)
    con = con.append({"Country": "Argentina", "Nationality": "Argentinian"}, ignore_index=True)

    # Adding additional matches and countries
    additional = {"Country": ["U.S.", "U.K.", "U.A.E.", "Angola", "Cyprus", "Hong Kong", "Kazakhstan"],
                  "Nationality": ["American", "British", "Emirati", "Angolan", "Cypriot", "Hongkonger", "Kazakhstani"]}
    df_to_add = pd.DataFrame(additional, columns=["Country", "Nationality"])

    final = pd.concat([con, df_to_add], sort=False)

    # Final details; sorting, setting index and deleting unnecessary columns.
    final.sort_values(by=["Country"], inplace=True)
    final.reset_index(drop=True, inplace=True)
    final.drop(columns=['Nationality  (Adjective)', 'Nationailty  (Noun)', 'Language'], axis=1, inplace=True)

    # Saving as csv file
    file_name = "CountryNationality.csv"
    # final.to_csv(f"../../data/processed/{file_name}", index=False)
    final.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

    # Returning clean dataframe
    return final
