import matplotlib.pyplot as plt
import lib.origin as org 
import pandas as pd
import sqlite3
import numpy as np
import os
from wordcloud import WordCloud
from io import BytesIO
import base64

keyword1 = 'tomato'
keyword2 = 'soup'

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,8))


SQL = f'''SELECT R.ID, R.tag_value as recipe_name, N.tag_value as ner_name
         FROM recipe R 
         JOIN recipe_ner RN ON R.ID = RN.recipe_id
         JOIN ner N ON RN.ner_id = N.ID
         WHERE R.tag_value LIKE '%{keyword1}%' 
         AND R.tag_value LIKE '%{keyword2}%'
         ;'''


currentDirectory = os.path.dirname(os.path.abspath(__file__))
DB = currentDirectory +'/database/recipe.db'


class RecipeQuery:

    def __init___(self):

        self.sql = f"""SELECT R.ID, R.tag_value as recipe_name, N.tag_value as ner_name
                        FROM recipe R 
                        JOIN recipe_ner RN ON R.ID = RN.recipe_id
                        JOIN ner N ON RN.ner_id = N.ID"""

    def __repr__(self):
        print(self.sql)
    

    def queryOnRecipe(self, searched_recipe, exact_search):
        """ create the query based on the form
        Inputs: keywords for searaching in recipes, boolean to indicate type of search
        Output: query
        """
        query = self.sql
        if exact_search == '1':
            query += f"""WHERE R.tag_value LIKE '%{searched_recipe}%';"""
        else:
            query += f"""WHERE R.tag_value LIKE '%{searched_recipe.split(' ')[0]}%'"""
            if len(searched_recipe.split(' ')) > 1:
                for i in searched_recipe.split(' ')[1:]:
                    query += f""" AND R.tag_value LIKE '%{i}%'"""
            query += """;"""
        return query


    def queryOnRecipeNer(searched_recipe, searched_ner, exact_search):
        sql = self.queryOnRecipe(searched_ner, exact_search)
    
        #Inputs: keywords for searaching in recipes, boolean to indicate type of search
        #Output: list of tuples as result, grouped dataframe on recipes 
    
        # generate first query to find recipe ID match criteria
    
        query1 = sql + f''' INTERSECT
                SELECT RN.recipe_id
                FROM recipe_ner RN
                JOIN ner N ON RN.ner_id = N.ID
                WHERE N.tag_value LIKE '%{searched_ner}%'
                '''

        # generate second query
        query2 = f"""SELECT R.ID, R.tag_value, N.tag_value 
                FROM recipe R 
                JOIN recipe_ner RN ON R.ID = RN.recipe_id
                JOIN ner N ON RN.ner_id = N.ID
                WHERE R.ID IN ({query1});"""
        return query2




class RecipeIngredients:
    def __init__(self, df):
        self.df = df

    @property
    def group(self):
        try:
            grouped = self.df.groupby(['ID', 'recipe_name'])['ner_name'].apply(list).reset_index()
        except:
            grouped = pd.DataFrame()
        return grouped

    def __repr__(self):
        print(self.group)



class DataModel:

    def __init__(self, sql=SQL, db=DB):
 
        self.df = pd.read_sql(sql, sqlite3.connect(db))
        self.df_recipes = self.df.drop_duplicates(subset = ['ID'])
        self.total = len(self.df_recipes)
        self.grouped = RecipeIngredients(self.df).group
        

    def get_origin(self, n=10):
        """ method that adds a column origin to the dataframe and selects the 10 largest into a new dataframe"""
        self.df_recipes['origin'] = self.df_recipes['recipe_name'].apply(org.get_origin)
        self.df_recipes = self.df_recipes[self.df_recipes.origin != '']
        dfnlargest = self.df_recipes.origin.value_counts().nlargest(n)
        return dfnlargest


    def get_count(self):
        """ method that gets the counts of the ingredients"""
        freq = self.df.iloc[:,2:3].value_counts().nlargest(20)
        ingredients = list(list(zip(*freq.index))[0])
        counts = list(freq)
        return ingredients, counts


    def create_fig(self, filename):
        """ method that plots the data """

        #create origin pie plot
        dfnlargest = self.get_origin()
        ax3.pie(dfnlargest, labels = dfnlargest.index, autopct='%1.1f%%', textprops={'fontsize': 8})
        ax3.set_title('top 10 locations')

        #create count per ingredient plot
        ingredients, counts = self.get_count()
        ax1.bar(ingredients, counts, color='red', alpha = 0.7)
        ax1.set_ylabel('ingredient occurence', fontsize = 8)
        ax1.set_xticks(range(0,20))
        ax1.set_xticklabels(ingredients, rotation= 90, fontsize = 8)
        
        #create number of ingredients distribution plot
        rc = self.df.groupby(by="ID").count()
        ax2.hist(rc.ner_name, color ='red', bins=50, alpha = 0.7)
        ax2.set_xlabel("# ingredients", fontsize = 8)
        ax2.set_ylabel('counts', fontsize = 8)
        
        #create wordcloud plot
        text = " ".join(i for i in self.df.ner_name)
        wordcloud = WordCloud(stopwords=org.stopwords, background_color="white").generate(text)
        ax4.imshow(wordcloud)
        ax4.axis('off')

        #main title
        fig.suptitle(f'{self.total} {keyword1} {keyword2} recipes')
        fig.tight_layout()

        return self.create_website_plot(fig)


    def create_website_plot(self, fig):
        """
        Given a figure create a stream that can be placed into a <img > tag
        Use the following attribute value for the <img>tag
        <img src="data:image/png;base64,{{ results }}">

        :param fig: a figure created using mathlotlib
        :return: png figure as stream to insert into html
        """

        figfile = BytesIO()
        fig.savefig(figfile, format='png')
        figfile.seek(0)  # rewind to beginning of file
        website_png = base64.b64encode(figfile.getvalue()).decode('ascii')

        return website_png
