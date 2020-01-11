import sqlalchemy
import pandas as pd

# cnx = "sqlite:///../../data/raw/nicolascortinas.db"
# tables = {"b": "business_info", "p": "personal_info", "r": "rank_info"}

# engine = sqlalchemy.create_engine("sqlite:///../../data/raw/nicolascortinas.db")
# b = pd.read_sql_table("business_info", engine)
# p = pd.read_sql_table("personal_info", engine)
# r = pd.read_sql_table("rank_info", engine)


def engine_connection(tables_dict, eng):
    """
    :param tables_dict: Dictionary with tables. Key: variable name, value: table name in database
    :param eng: Engine
    :return: Dictionary comprised by dataframes. Key: variable name, value: dataframe
    """
    dfs_dict = {}

    engine = sqlalchemy.create_engine(eng)

    # for key, value in tables_dict.items():
    #     dfs_dict[key] = pd.read_sql_table(value, engine)

    dfs_dict["b"] = pd.read_sql_table(tables_dict["b"], engine)
    dfs_dict["p"] = pd.read_sql_table(tables_dict["p"], engine)
    dfs_dict["r"] = pd.read_sql_table(tables_dict["r"], engine)

    print("Tables read into a dictionary")
    return dfs_dict


# dfs = engine_connection(tables, connect)
# print(dfs["r"])



