import pandas as pd
import os
import re
import requests
import json


def get_shooting_data(path = "./data/shooting.csv"):
    '''
    produces csv file "shooting.csv" with latest version of washington post database
    '''
    raw = "raw_data.csv"
    url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv"
    
    pd.read_csv(url).to_csv(raw, index = False)
    file = open(path, "wt")

    # this is where all data cleaning takes place
    with open(raw, "rt") as f:
        for line in f:
            line = re.sub(" +", ' ', line) # remove extra spaces
            file.write(line)

    file.close()
    os.remove(raw)


def edit_shooting_features(path = "./data/shooting.csv"):
    '''
    function for all feature engineering
    '''
    data = pd.read_csv(path)
    data[["year", "month", "day"]] = data["date"].str.split('-', expand = True)
    data.to_csv(path, index = False)


def get_age_data(path = "./data/census_age.csv"):
    '''
    save population estimates by single year of age from Census Data API.
    info on API response formate can be found in the Census Data API User Guide under Core Concepts.
    https://www.census.gov/data/developers/guidance/api-user-guide.Core_Concepts.html
    '''

    API_KEY = "eed7905dcca3890bef8e1e203a30ce9f23d6a750"
    url = f"https://api.census.gov/data/2019/pep/charage?get=AGE,POP&SEX=0&for=us:1&key={API_KEY}"
    data: list[list[str]] = json.loads(requests.get(url).text)

    (pd.DataFrame(data[1:], columns = data[0]) # data[0] : ["AGE", "POP", "SEX", "us"]
       .drop(["SEX", "us"], axis = 1)
       .astype({"AGE" : int, "POP" : int})
       .query("AGE != 999")
       .sort_values("AGE")
       .to_csv(path, index = False)
       )

    print("Successfully saved population estimates by single year of age from Census Data API")


def main():
    get_shooting_data()
    edit_shooting_features()
    get_age_data()


if __name__ == "__main__":
    #main()
    get_age_data()