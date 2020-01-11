import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def fixing_gender(df):
    # Switching None remaining values in gender column to Male. There were 16 None and about 85% of the total are Male.
    for x in range(len(df)):
        if pd.isnull(df.loc[x, "gender"]):
            df.loc[x, "gender"] = "Male"
    return df


def pie_chart(df):
    # Male vs Female distribution pie chart
    mf = df.groupby("gender").count()["id"]
    lab = df.groupby("gender").count().index
    col = ["#dea0e8", "#57a1eb"]

    plt.figure(figsize=(5, 5))
    plt.title("Male / Female Distribution")
    plt.pie(mf, labels=lab, colors=col, autopct="%.2f", explode=[.1, .1], textprops={'fontsize': 14})

    plt.savefig("data/results/Gender_PieChart.png", dpi=400)
    print("Pie chart generated")
    return


def bar_chart(df):
    sect = df.groupby("Sector").sum()["Worth(BUSD)"]
    lab = df.groupby("Sector").sum().index

    plt.figure(figsize=(16, 8))
    plt.title("Wealth distribution by sector (in BUSD)", fontdict={'fontsize': 20, "fontname": "Impact"})
    plt.bar(lab, sect)
    label_font = {"fontsize": 20, "fontname": "Arial"}
    plt.xlabel("Sector", fontdict=label_font)
    plt.ylabel("Worth in B$US", fontdict=label_font)
    plt.xticks(rotation=60)
    plt.savefig("data/results/Sector_BarChart.png", dpi=400, bbox_inches="tight")
    print("Basic bar chart generated")
    return


def bar_chart_full(df):
    sector_f = df.groupby(["gender", "Sector"]).sum()["Worth(BUSD)"]["Female"]
    sector_m = df.groupby(["gender", "Sector"]).sum()["Worth(BUSD)"]["Male"]
    f_values = sector_f.values
    m_values = sector_m.values
    indices = sector_m.index
    plt.figure(figsize=(14, 7))

    plt.bar(indices, m_values, width=0.6, color='#abcabc', label='Male')
    plt.bar(indices, f_values, width=0.5 * 0.6, color='r', label='Female')

    plt.title("Gender distribution by sector (in BUSD)", fontdict={'fontsize': 20, "fontname": "Impact"})

    label_font = {"fontsize": 20, "fontname": "Arial"}
    plt.xticks(indices, rotation=-45, ha="left")
    plt.ylabel("Worth(BUSD)", fontdict=label_font)
    plt.xlabel("Sector", fontdict=label_font)
    plt.legend()
    plt.savefig("data/results/SectorGenderBarChart.png", dpi=400, bbox_inches="tight")
    print("Bar chart sector 1 generated")
    return


