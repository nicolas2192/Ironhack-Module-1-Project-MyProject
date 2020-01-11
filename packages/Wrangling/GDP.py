import pandas as pd
import re


def gdp_nominal():
    """
    This function sorts through a wikipedia page looking for a table listing all countries by nominal GDP
    :return: Clean CSV file with the data, 3 columns: Rank, Country and GDP
    """
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"  # GDP nominal

    # parsing all tables looking for the one we are interested in.
    tables = pd.read_html(url)
    gdp = tables[4]

    # cleaning the data, removing special characters, computing total amount and renaming column names.
    gdp["Country/Territory"] = gdp["Country/Territory"].apply(lambda country: re.sub(r"\[.+", "", country))
    gdp["GDP(US$million)"] = gdp["GDP(US$million)"].apply(lambda x: re.sub(r"\s\(\d+\)", "", x))
    gdp["GDP(US$million)"] = gdp["GDP(US$million)"].apply(lambda x: re.sub(r",", "", x))
    gdp["GDP(US$million)"] = gdp["GDP(US$million)"].astype("int")
    gdp.iloc[0, 2] = gdp.iloc[1:191, 2].sum()
    gdp["Rank"] = gdp.index

    # changing columns' name.
    gdp = gdp.rename(columns={'Country/Territory': 'Country', 'GDP(US$million)': 'GDP(US$M)'})
    # gdp.drop(["Country/Territory", "GDP(US$million)"], axis=1, inplace=True)

    # saving dataframe into a csv.
    file_name = "GDP_nominal.csv"
    # gdp.to_csv(f"../../data/processed/{file_name}", index=False)
    gdp.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")


def gdp_per_capita():
    """
    This function sorts through a wikipedia page looking for a table listing all countries by per capita GDP
    :return: Clean CSV file with the data, 3 columns: Rank, Country and US$ per capita
    """
    url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)_per_capita"  # GDP per capita

    # parsing all tables looking for the one we are interested in.
    tables = pd.read_html(url)
    gdp = tables[3]

    # cleaning the data, removing special characters and renaming column names.
    gdp["Country/Territory"] = gdp["Country/Territory"].apply(lambda country: re.sub(r"\[.+", "", country))
    gdp["Rank"] = gdp.index
    gdp["Rank"] = gdp["Rank"].apply(lambda x: x + 1)
    gdp = gdp.rename(columns={'Country/Territory': 'Country'})

    # saving dataframe into a csv.
    file_name = "GDP_per_capita.csv"
    # gdp.to_csv(f"../../data/processed/{file_name}", index=False)
    gdp.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")


def population():
    """
    This function sorts through a wikipedia page looking for a table listing all countries by population
    :return: Clean CSV file with the data, 3 columns: Rank, Country and Population
    """

    url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"

    # Parsing web page and returning raw table
    tables = pd.read_html(url)
    pop = tables[0]

    # Cleaning the data, removing special characters, computing total, fixing rank and renaming column names.
    pop["Country(or dependent territory)"] = pop["Country(or dependent territory)"].apply(lambda country: re.sub(r"\[.+" ,"", country))
    pop["Rank"] = pop.index
    pop["Rank"] = pop["Rank"].apply(lambda x: x+1)
    pop = pop.rename(columns={'Country(or dependent territory)': 'Country'})
    pop.iloc[len(pop)-1, 2] = pop.iloc[0:len(pop)-1, 2].sum()

    # Deleting unnecessary columns
    pop.drop(columns=list(pop.columns)[3:6], axis=1, inplace=True)

    # saving dataframe into a csv.
    file_name = "Population.csv"
    # pop.to_csv(f"../../data/processed/{file_name}", index=False)
    pop.to_csv(f"data/processed/{file_name}", index=False)
    print(f"{file_name} was successfully saved!")

