import pandas as pd
import packages.Acquisition.Acquisition as aq
import packages.Wrangling.Wrangling as wr
import packages.Wrangling.DataEnhancement as de
import packages.Wrangling.GDP as my
import packages.Wrangling.CountryVsNationality as cn
import packages.Wrangling.API as sx
import packages.Analyzing.Analysis as an
import packages.Reporting.Emaildelivery as em


def main(wikipedia=False, api_gender=False, send_to=None):

    cnx = "sqlite:///data/raw/nicolascortinas.db"
    tables = {"b": "business_info", "p": "personal_info", "r": "rank_info"}

    # Main data, import from database
    dfs = aq.engine_connection(tables, cnx)

    # Wrangling
    business = wr.business_df(dfs["b"])
    personal = wr.personal_df(dfs["p"])
    rank = wr.rank_df(dfs["r"])
    clean_df = wr.putting_all_together(personal, rank, business)

    # WebScraping
    my.gdp_nominal()
    my.gdp_per_capita()
    my.population()
    countries_df = cn.country_nationality_table()

    if wikipedia:
        missing_age = de.null_values(clean_df, "a", tolist=True)
        missing_age_result = de.data_enhancement(missing_age, "a", countries_df)
        clean_df = de.merge_enhanced_data(clean_df, missing_age_result, "age", "Age")

        missing_country = de.null_values(clean_df, "c", tolist=True)
        missing_country_result = de.data_enhancement(missing_country, "c", countries_df)
        clean_df = de.merge_enhanced_data(clean_df, missing_country_result, "country", "Nationality")

        clean_df.to_csv("data/processed/clean_df_enhanced.csv", index=False)
    else:
        clean_df = pd.read_csv("data/processed/clean_df_enhanced.csv")

    # API
    if api_gender:
        country_relation = pd.read_csv("data/raw/TwoLettersCountryCodes.csv")
        search_list = sx.api_search_list(clean_df, country_relation, tolist=True)
        missing_gender = sx.api_search(search_list, todf=True)
        clean_df = sx.merge_enhanced_gender(clean_df, missing_gender)

        clean_df.to_csv("data/processed/clean_df_enhanced.csv", index=False)
    else:
        clean_df = pd.read_csv("data/processed/clean_df_enhanced.csv")

    # Analyzing
    clean_df = an.fixing_gender(clean_df)
    an.pie_chart(clean_df)
    an.bar_chart(clean_df)
    an.bar_chart_count(clean_df)
    an.bar_chart_money(clean_df)
    clean_df.to_csv("data/results/data_table.csv", index=False)

    # Reporting
    em.send_mail(send_to)


if __name__ == "__main__":
    main(wikipedia=False, api_gender=False, send_to="nicosduty@gmail.com")








