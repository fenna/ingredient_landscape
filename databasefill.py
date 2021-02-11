""" Script to demonstrate the creation and filling of recipe database """

__author__ = 'f.feenstra'

import pandas as pd
import sqlite3

#make connection with the database
#this need to be replaced with the actual database
conn = sqlite3.connect('TestDB.db')
c = conn.cursor()

#create table if not exist
c.execute('CREATE TABLE IF NOT EXISTS recipe (id TEXT PRIMARY KEY NOT NULL UNIQUE, tag TEXT, tag_value TEXT)')
conn.commit()


#create quickly a database from a dictionary
#this need to be replaced with the actual dataframe 
recipe = {'id': ['rec_1', 'rec_2'],
        'tag': ['name', 'name'], 'tag_value':['chocolat','salt']
        }

df = pd.DataFrame(recipe, columns= ['id', 'tag', 'tag_value'])

#parse dataframe to database
df.to_sql('recipe', conn, if_exists='replace', index = False)

#hint: use DB browser for sql lite to view the database