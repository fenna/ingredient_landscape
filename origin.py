from geotext import GeoText
import pandas as pd
import os

curdir = os.path.dirname(os.path.abspath(__file__))

with open(curdir + '/data/english') as e:
    stopwords= [word.strip() for word in e]

def get_origin(text):
    """ 
    function that searches for countries associated with a text
    The words of the text needs to be capitalized and seperated by a comma
    The Geotext returns a list of country abbreviations (isocodes)
    It uses the country information from https://www.geonames.org/countries/ 
    to relate the name of the country to the isocode
    
    input: Text
    output: country names seperated by space
    parameter: countries dataframe
    
    """
    freqwords = ['green', 'red', 'orange', 'yellow', 'cream', 'creamy', 'tomato', 'soup', 'leek','best']
    countries = get_countries()
    t = ""
    textlist = text.split(" ")
    textlist = [word.lower() for word in textlist if not word in stopwords and not word in freqwords]
    textlist = [word.capitalize() for word in textlist]
    text = ",".join(textlist)
    result = GeoText(text).country_mentions.keys()
    for i in result:
        try:
            t += countries.loc[countries['iso2'] == i.strip()]['country'].values[0] + ' '
        except:
            try:
                t += {countries.loc[countries['fips'] == i.strip()]['country'].values[0]} + ' '
            except:
                t = i
    return t


def get_countries():
    ''' retrieve the country data'''
    return pd.read_csv(curdir + '/data/countries', sep = '\t')


def main():
    ''' main function with test'''
    print(get_origin('italian soup'))


if __name__ == '__main__':
    main()

