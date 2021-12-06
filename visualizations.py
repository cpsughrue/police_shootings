import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def comparePopulationByProportionOfRace():

    race = pd.read_csv("./data/race.csv").query("RACE > 0 and RACE < 5")
    washpost = pd.read_csv("./data/washpost.csv").query("race != 'H' and race != 'O'")

    map = pd.DataFrame({'lables_key'  : ["White", "Black", "Asia", "Native American"],
                        'washpost_key': ['W',     'B',     'A',    'N'],
                        'census_key'  : [ 1,       2,       4,      3 ]})

    washpost_df = (pd.DataFrame(washpost.loc[:, "race"].value_counts() / washpost.loc[:, "race"].dropna().size)
                     .rename(columns={"race": "washpost_race"}))
    census_df = (pd.DataFrame(race.loc[:, "POP"] / race.loc[:, "POP"].sum())
                   .rename(columns={"POP": "census_race"}))

    data = map.join(washpost_df, on = "washpost_key").join(census_df, on = "census_key")

    washpost_color = "#0b84a5"
    census_color = "#f6c85f"

    plt.figure(figsize = (10, 5))

    WIDTH = .6
    labels = data.loc[:, "lables_key"]
    x = np.linspace(0, 6, len(labels), dtype = int)

    plt.bar(x - WIDTH / 2, data.loc[:, "washpost_race"], WIDTH, color = washpost_color)
    plt.bar(x + WIDTH / 2, data.loc[:, "census_race"], WIDTH, color = census_color)
    plt.xticks(x, labels, fontsize = 12)

    # get current axis
    ax = plt.gca()

    # add title
    plt.title("Proportion by Race", fontsize = 18)

    # create legend
    washpost_patch = mpatches.Patch(color = washpost_color, label = "Washington Post")
    census_patch = mpatches.Patch(color = census_color, label = "US Census")
    ax.legend(handles = [washpost_patch, census_patch], prop = {"size": 12}, frameon = False,)

    # add measurment above bar
    for index, value in enumerate(x):
        plt.text(value - WIDTH / 2, data.loc[index, "washpost_race"] + .02, 
                                    "{:.0%}".format(data.loc[index, "washpost_race"]), 
                                    horizontalalignment = 'center', 
                                    fontsize = 14)

        plt.text(value + WIDTH / 2, data.loc[index, "census_race"] + .02, 
                                    "{:.0%}".format(data.loc[index, "census_race"]), 
                                    horizontalalignment = 'center', 
                                    fontsize = 14)

    # remove border around bar plot
    [ax.spines[s].set_visible(False) for s in ax.spines]

    # format ticks of kde plot
    ax.tick_params(axis = 'x', length = 0)
    ax.get_yaxis().set_visible(False)

    plt.savefig("race.svg", format = "svg", bbox_inches = "tight")

comparePopulationByProportionOfRace()