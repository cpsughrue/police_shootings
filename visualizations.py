import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def calculateAgeDistribution(path: str = "./data/age.csv") -> tuple[int, np.ndarray]:
    '''
    create array of integers that represent age distribution of US population.
    array will be used to plot kernel density estimation of US population's age
    in comparePopulationsByAgeDistribution()
    '''
    census_age: pd.DataFrame = pd.read_csv(path)
    total_us_pop: int = sum(census_age.loc[:, "POP"])

    # scale down count to decrease number of data points in us_age_dist
    SCALE: int = 10000
    us_age_dist: pd.Series = np.repeat(census_age.loc[:, "AGE"], 
                                       census_age.loc[:, "POP"] / SCALE)

    return  total_us_pop, us_age_dist


def comparePopulationsByAgeDistribution(WASHPOST_COLOR, CENSUS_COLOR) -> None:
    '''
    produces plot that compares the age distribution of the entire US 
    populations and the age distribution of the casualities
    '''

    total_us_pop, us_age_dist = calculateAgeDistribution()
    washpost_age_dist = pd.read_csv("./data/washpost.csv").loc[:, "age"].dropna()

    f, [ax_kde, ax_box] = plt.subplots(2, figsize = (10, 6),
                                          linewidth = 1, 
                                          sharex = True, 
                                          gridspec_kw = {"height_ratios": (0.85, 0.15)})

    ################################################
    ### EDITS TO KERNAL DENSITY ESTIMATION PLOTS ###
    ################################################

    # plot US population age distribution and cauality age distribution
    us_age_dist.plot.density(ax = ax_kde, linewidth = 3, color = CENSUS_COLOR)
    washpost_age_dist.plot.density(ax = ax_kde, linewidth = 3, color = WASHPOST_COLOR,)

    # format x-axis of box plot
    ax_kde.set_xlabel("Years", fontsize = 14)
    ax_kde.set_xlim(-5, 100)

    # format ticks of kde plot
    ax_kde.get_yaxis().set_visible(False)
    ax_kde.tick_params(axis = 'x', length = 0)

    # remove border around kde plot
    ax_kde.spines["top"].set_visible(False)
    ax_kde.spines["right"].set_visible(False)
    ax_kde.spines["left"].set_visible(False)

    #########################
    ### EDITS TO BOX PLOT ###
    #########################

    # create box plot
    bp = ax_box.boxplot(washpost_age_dist.values, 
                        vert = False, 
                        showmeans = False, 
                        patch_artist = True, 
                        widths = 0.8, 
                        whis = 3)

    # color in box of boxplot
    plt.setp(bp["medians"], alpha = 0)
    for patch in bp["boxes"]:
        patch.set(facecolor = WASHPOST_COLOR, alpha = .9)

    # format ticks of box plot
    ax_box.tick_params(size = 0, labelsize = 12, pad = 12)
    ax_box.xaxis.tick_top()
    ax_box.get_yaxis().set_visible(False)

    # remove border around box plot
    [ax_box.spines[s].set_visible(False) for s in ax_box.spines]

    # calculate minimum, lower quartile, upper quartile, and maximum of box plot
    [mi, p25, p75, ma] = np.quantile(washpost_age_dist.values, [0, 0.25, 0.75, 1]).astype(int)

    # label minimum, lower quartile, upper quartile, and maximum of box plot
    ax_box.text(ma + 1.5, 1, str(ma), fontsize = 16, ha = "left", va = "center")
    ax_box.text(mi - 1.5, 1, str(mi), fontsize = 16, ha = "right", va = "center")
    ax_box.text(p25, .3, str(p25), fontsize = 16, ha = "center", va = "center")
    ax_box.text(p75, .3, str(p75), fontsize = 16, ha = "center", va = "center")

    # label mean of box plot
    x = p75 - (p75 - p25) / 2
    mean = round(np.mean(washpost_age_dist.values), 2)
    ax_box.text(x, 1, f"$\mu = {mean}$", fontsize = 16, ha = "center", va = "center", color = "white")

    #############################
    ### GENERAL EDITS TO PLOT ###
    #############################

    # add title
    ax_kde.text(43, .03, "Comparing Age Distributions (Years)", fontsize = 18)

    # calculate and format size of each popuatlation
    census_total = '{:,}'.format(len(washpost_age_dist))
    washpost_total = '{:,}'.format(total_us_pop)

    # create legend
    washpost_patch = mpatches.Patch(color = WASHPOST_COLOR, label = f"Washington Post (n = {census_total})")
    census_patch = mpatches.Patch(color = CENSUS_COLOR, label = f"US Census (n = {washpost_total})")
    ax_kde.legend(handles = [washpost_patch, census_patch], 
                  prop = {"size": 12}, 
                  frameon = False, 
                  bbox_to_anchor = (.485, 0.87))

    plt.savefig("./images/age.svg", format = "svg", bbox_inches = "tight", edgecolor = "black")


def comparePopulationsByRace(WASHPOST_COLOR, CENSUS_COLOR):
    '''
    name: census, type: pd.Series, dtype: int64
    1     250522190
    2     44075086
    3     4188092
    4     19504862
    
    name: washpost, type: pd.Series, dtype: int64
    W     2970
    B     1557
    A     106
    N     91
    '''

    census   = (pd.read_csv("./data/race.csv")
                  .query("0 < RACE < 5")
                  .rename(columns = {"POP": "census"})
                  .loc[:, "census"])
    
    washpost = (pd.read_csv("./data/washpost.csv")
                  .query("race != 'H' and race != 'O'")
                  .rename(columns = {"race": "washpost"})
                  .loc[:, "washpost"]
                  .value_counts(dropna = True))

    map = pd.DataFrame({'lables_key'  : ["White", "Black", "Asia", "Native American"],
                        'washpost_key': ['W',     'B',     'A',    'N'],
                        'census_key'  : [ 1,       2,       4,      3 ]})

    washpost_df = pd.DataFrame(washpost / washpost.sum())
    census_df = pd.DataFrame(census / census.sum())

    data = map.join(washpost_df, on = "washpost_key").join(census_df, on = "census_key")

    plt.figure(figsize = (10, 6), linewidth = 1)

    labels = data.loc[:, "lables_key"]
    x = np.linspace(0, 6, len(labels), dtype = int)

    WIDTH = .6
    plt.bar(x - WIDTH / 2, data.loc[:, "washpost"], WIDTH, color = WASHPOST_COLOR)
    plt.bar(x + WIDTH / 2, data.loc[:, "census"], WIDTH, color = CENSUS_COLOR)

    plt.xticks(x, labels, fontsize = 12)

    # get current axis
    ax = plt.gca()

    # add title
    plt.title("Proportion by Race", fontsize = 18)

    # create legend
    washpost_patch = mpatches.Patch(color = WASHPOST_COLOR, label = "Washington Post")
    census_patch = mpatches.Patch(color = CENSUS_COLOR, label = "US Census")
    ax.legend(handles = [washpost_patch, census_patch], prop = {"size": 12}, frameon = False,)

    # add measurment labels above each bar
    for index, value in enumerate(x):
        plt.text(value - WIDTH / 2, data.loc[index, "washpost"] + .02, 
                                    "{:.0%}".format(data.loc[index, "washpost"]), 
                                    horizontalalignment = 'center', 
                                    fontsize = 14)

        plt.text(value + WIDTH / 2, data.loc[index, "census"] + .02, 
                                    "{:.0%}".format(data.loc[index, "census"]), 
                                    horizontalalignment = 'center', 
                                    fontsize = 14)

    # remove border around plot
    [ax.spines[s].set_visible(False) for s in ax.spines]

    # format ticks from plot
    ax.tick_params(axis = 'x', length = 0)
    ax.get_yaxis().set_visible(False)

    # save figure
    plt.savefig("./images/race.svg", format = "svg", bbox_inches = "tight", edgecolor = "black")


if __name__ == "__main__":
    WASHPOST_COLOR = "#0b84a5"
    CENSUS_COLOR = "#f6c85f"

    comparePopulationsByAgeDistribution(WASHPOST_COLOR, CENSUS_COLOR)
    print("comparePopulationsByAgeDistribution completed")

    comparePopulationsByRace(WASHPOST_COLOR, CENSUS_COLOR)
    print("comparePopulationsByRace completed")