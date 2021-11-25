import pandas as pd
import os
import re
import requests
import json

class WashingtonPostShootingData:

    def __init__(self, PATH: str) -> None:
        self.PATH = PATH


    def get_data(self) -> None:
        '''
        produces csv file "shooting.csv" with latest version of washington post database
        '''
        raw = "raw_data.csv"
        url = "https://raw.githubusercontent.com/washingtonpost/data-police-shootings/master/fatal-police-shootings-data.csv"
        
        pd.read_csv(url).to_csv(raw, index = False)
        file = open(self.PATH, "wt")

        # this is where all data cleaning takes place
        with open(raw, "rt") as f:
            for line in f:
                line = re.sub(" +", ' ', line) # remove extra spaces
                file.write(line)

        file.close()
        os.remove(raw)


    def edit_features(self) -> None:
        '''
        function for all feature engineering
        '''
        data = pd.read_csv(self.PATH)
        data[["year", "month", "day"]] = data["date"].str.split('-', expand = True)
        data.to_csv(self.PATH, index = False)


class CensusData:
    '''
    info on API response formate can be found in the Census Data API User Guide under Core Concepts.
    https://www.census.gov/data/developers/guidance/api-user-guide.Core_Concepts.html
    '''

    def __init__(self, API_KEY: str) -> None:
        self.API_KEY = API_KEY


    def get_age_data(self, PATH: str = "./data/age.csv"):
        ''' 
        save population estimates by single year of age from Census Data API.
        '''

        url = f"https://api.census.gov/data/2019/pep/charage?get=AGE,POP&SEX=0&for=us:1&key={self.API_KEY}"
        data: list[list[str]] = json.loads(requests.get(url).text)

        (pd.DataFrame(data[1:], columns = data[0]) # data[0] : ["AGE", "POP", "SEX", "us"]
           .drop(["SEX", "us"], axis = 1)
           .astype({"AGE" : int, "POP" : int})
           .query("AGE != 999")
           .sort_values("AGE")
           .to_csv(PATH, index = False)
           )

        print("Successfully saved population estimates by single year of age")


    def get_race_data(self, PATH: str = "./data/race.csv") -> None:
        '''
        save race populations from Census Data API.

        '''

        url = f"https://api.census.gov/data/2019/pep/charagegroups?get=RACE,POP&for=us:1&key={self.API_KEY}"
        data: list[list[str]] = json.loads(requests.get(url).text)

        (pd.DataFrame(data[1:], columns = data[0]) # data[0] : ["RACE", "POP", "NAME", "us"]
           .drop(["us"], axis = 1)
           .astype({"RACE" : int, "POP" : int})
           .sort_values("RACE")
           .to_csv(PATH, index = False)
           )

        print("Successfully saved population of race estimates")


def main() -> None:
    w = WashingtonPostShootingData(PATH = "./data/shooting.csv")
    w.get_data()
    w.edit_features()

    c = CensusData(API_KEY = "eed7905dcca3890bef8e1e203a30ce9f23d6a750")
    c.get_age_data()
    c.get_race_data()

        

if __name__ == "__main__":
    main()