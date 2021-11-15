import pandas as pd
import os
import re


def get_shooting_data(path = "./data/shooting.csv"):
    '''
    produces csv file "shooting.csv" with latest version of washington post database
    '''
    raw = "raw_data.csv"
    url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv"
    
    pd.read_csv(url, index_col = "id").to_csv(raw)
    file = open(path, "wt")

    # this is where all data cleaning takes place
    with open(raw, "rt") as f:
        for line in f:
            line = re.sub(" +", ' ', line) # remove extra spaces
            file.write(line)

    file.close()
    os.remove(raw)


def edit_features(path = "./data/shooting.csv"):
    '''
    function for all feature engineering prior to being loaded into a relational database
    '''
    data = pd.read_csv(path, index_col = "id")
    data[["year", "month", "day"]] = data["date"].str.split('-', expand = True)
    data.to_csv(path)


def main():
    path = "./data/shooting.csv"
    get_shooting_data(path)
    edit_features(path)


if __name__ == "__main__":
    main()

    