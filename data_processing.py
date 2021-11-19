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


def get_age_data(path = "./data/test.csv"):
    
    url = "https://api.census.gov/data/2019/acs/acs5/pums?tabulate=weight(PWGTP)&row+AGEP_RC1&recode+AGEP_RC1=%7B%22b%22:%22AGEP%22,%22d%22:%5B%5B%220%22%5D,%5B%221%22%5D,%5B%222%22%5D,%5B%223%22%5D,%5B%224%22%5D,%5B%225%22%5D,%5B%226%22%5D,%5B%227%22%5D,%5B%228%22%5D,%5B%229%22%5D,%5B%2210%22%5D,%5B%2211%22%5D,%5B%2212%22%5D,%5B%2213%22%5D,%5B%2214%22%5D,%5B%2215%22%5D,%5B%2216%22%5D,%5B%2217%22%5D,%5B%2218%22%5D,%5B%2219%22%5D,%5B%2220%22%5D,%5B%2221%22%5D,%5B%2222%22%5D,%5B%2223%22%5D,%5B%2224%22%5D,%5B%2225%22%5D,%5B%2226%22%5D,%5B%2227%22%5D,%5B%2228%22%5D,%5B%2229%22%5D,%5B%2230%22%5D,%5B%2231%22%5D,%5B%2232%22%5D,%5B%2233%22%5D,%5B%2234%22%5D,%5B%2235%22%5D,%5B%2236%22%5D,%5B%2237%22%5D,%5B%2238%22%5D,%5B%2239%22%5D,%5B%2240%22%5D,%5B%2241%22%5D,%5B%2242%22%5D,%5B%2243%22%5D,%5B%2244%22%5D,%5B%2245%22%5D,%5B%2246%22%5D,%5B%2247%22%5D,%5B%2248%22%5D,%5B%2249%22%5D,%5B%2250%22%5D,%5B%2251%22%5D,%5B%2252%22%5D,%5B%2253%22%5D,%5B%2254%22%5D,%5B%2255%22%5D,%5B%2256%22%5D,%5B%2257%22%5D,%5B%2258%22%5D,%5B%2259%22%5D,%5B%2260%22%5D,%5B%2261%22%5D,%5B%2262%22%5D,%5B%2263%22%5D,%5B%2264%22%5D,%5B%2265%22%5D,%5B%2266%22%5D,%5B%2267%22%5D,%5B%2268%22%5D,%5B%2269%22%5D,%5B%2270%22%5D,%5B%2271%22%5D,%5B%2272%22%5D,%5B%2273%22%5D,%5B%2274%22%5D,%5B%2275%22%5D,%5B%2276%22%5D,%5B%2277%22%5D,%5B%2278%22%5D,%5B%2279%22%5D,%5B%2280%22%5D,%5B%2281%22%5D,%5B%2282%22%5D,%5B%2283%22%5D,%5B%2284%22%5D,%5B%2285%22%5D,%5B%2286%22%5D,%5B%2287%22%5D,%5B%2288%22%5D,%5B%2289%22%5D,%5B%2290%22%5D,%5B%2291%22%5D,%5B%2292%22%5D,%5B%2293%22%5D,%5B%2294%22%5D,%5B%2295%22%5D,%5B%2296%22%5D,%5B%2297%22%5D,%5B%2298%22%5D,%5B%2299%22%5D%5D%7D"
    raw_data = requests.get(url)
    parsed_data = json.loads(raw_data.text)

    # parsed_data
    # [
    #  ['tabulate', 'AGEP_RC1'],
    #  [3701318.0, '1'],
    #  [3894732.0, '2'],
    #  ...
    #  [1303.0, '98'],
    #  [0.0, '99'],
    #  [0.0, '100']
    # ]

    pd.DataFrame(parsed_data, columns = ['count', 'age']).to_csv(path, index = False)


def main():
    get_shooting_data()
    edit_shooting_features()

    # get_age_data()


if __name__ == "__main__":
    

    