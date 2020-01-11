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


def bar_chart_money(df):
    gsect_money = df.groupby(["gender", "Sector"]).sum()["Worth(BUSD)"]

    gsect_money_f = gsect_money.loc["Female"].nlargest()
    gsect_money_m = gsect_money.loc["Male"].nlargest()

    labf = [lbl + "_f" for lbl in gsect_money_f.index]
    valf = gsect_money_f.values
    labm = [lbl + "_m" for lbl in gsect_money_m.index]
    valm = gsect_money_m.values

    labs_money = np.concatenate([labf, labm])
    vals_money = np.concatenate([valf, valm])

    plt.figure(figsize=(14, 7))
    plt.title("Gender distribution by sector (top 5) in Worth BUSD", fontdict={'fontsize': 20, "fontname": "Impact"})
    bars_count = plt.bar(labf, valf, color=["red"], label="Female") + plt.bar(labm, valm, color=["blue"], label="Male")
    label_font = {"fontsize": 20, "fontname": "Arial"}
    plt.xlabel("Sector", fontdict=label_font)
    plt.ylabel("Worth(BUSD)", fontdict=label_font)
    plt.xticks(rotation=60)
    plt.legend()
    plt.savefig("data/results/SectorGenderMoney_BarChart.png", dpi=400, bbox_inches="tight")
    print("Bar chart sector 1 generated")
    return


def bar_chart_count(df):
    gsect_count = df.groupby(["gender", "Sector"]).count()["id"]

    gsect_count_f = gsect_count.loc["Female"].nlargest()
    gsect_count_m = gsect_count.loc["Male"].nlargest()

    labf = [lbl + "_f" for lbl in gsect_count_f.index]
    valf = gsect_count_f.values
    labm = [lbl + "_m" for lbl in gsect_count_m.index]
    valm = gsect_count_m.values

    labs_count = np.concatenate([labf, labm])
    vals_count = np.concatenate([valf, valm])

    plt.figure(figsize=(14, 7))
    plt.title("Gender distribution by sector (top 5) (real)", fontdict={'fontsize': 20, "fontname": "Impact"})
    bars_count = plt.bar(labf, valf, color=["red"], label="Female") + plt.bar(labm, valm, color=["blue"], label="Male")
    label_font = {"fontsize": 20, "fontname": "Arial"}
    plt.xlabel("Sector", fontdict=label_font)
    plt.ylabel("People count", fontdict=label_font)
    plt.xticks(rotation=60)
    plt.legend()
    plt.savefig("data/results/SectorGenderAmount_BarChart.png", dpi=400, bbox_inches="tight")
    print("Bar chart sector 2 generated")
    return

