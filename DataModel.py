import matplotlib.pyplot as plt
import lib.origin as org 
import pandas as pd
import sqlite3
import numpy as np
import os
from wordcloud import WordCloud

from io import BytesIO
import base64

#fig, (ax1, ax2) = plt.subplots(2)
keyword1 = 'tomato'
keyword2 = 'italian'
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10,8))


SQL = f'''SELECT R.ID, R.tag_value as recipe_name, N.tag_value 
         FROM recipe R 
         JOIN recipe_ner RN ON R.ID = RN.recipe_id
         JOIN ner N ON RN.ner_id = N.ID
         WHERE R.tag_value LIKE '%{keyword1}%' 
         AND R.tag_value LIKE '%{keyword2}%'
         ;'''

print(SQL)

currentDirectory = os.path.dirname(os.path.abspath(__file__))
DB = currentDirectory +'/database/recipe.db'

class DataModel:

    
    def bar_plot(self, filename):
        """
        Create a barplot from a csv file, use numpy to read a bytes stream
        :param filename: from form file upload
        :return: image stream to be placed in <img> tag
        """
        #read from database
        conn = sqlite3.connect(DB)
        df = pd.read_sql(SQL, conn)

        #get recipes
        df_recipes = df.drop_duplicates(subset = ['ID'])
        total = len(df_recipes)

        #get origin
        df_recipes['origin'] = df_recipes['recipe_name'].apply(org.get_origin)
        df_recipes = df_recipes[df_recipes.origin != '']
        dfnlargest = df_recipes.origin.value_counts().nlargest(10)

        ax3.pie(dfnlargest, labels = dfnlargest.index, autopct='%1.1f%%', textprops={'fontsize': 8})
        ax3.set_title('top 10 locations')

        # plot ingredient occurence
        freq = df.iloc[:,2:3].value_counts().nlargest(20)
        ingredients = list(list(zip(*freq.index))[0])
        counts = list(freq)
    
        ax1.bar(ingredients, counts, color='red', alpha = 0.7)
        ax1.set_ylabel('ingredient occurence', fontsize = 8)
        ax1.set_xticks(range(0,20))
        ax1.set_xticklabels(ingredients, rotation= 90, fontsize = 8)
        
        #plot number of ingredients distribution
        recipe_count = df.groupby(by="ID").count()
        recipe_count = recipe_count.iloc[:,1:2].reset_index().rename(columns = {'tag_value':'count'})
        rc = recipe_count.drop_duplicates(subset = 'ID')
        
        ax2.hist(rc['count'], color ='red', bins=50, alpha = 0.7)
        ax2.set_xlabel("# ingredients", fontsize = 8)
        ax2.set_ylabel('counts', fontsize = 8)

        text = " ".join(i for i in df.tag_value)
        wordcloud = WordCloud(stopwords=org.stopwords, background_color="white").generate(text)
        ax4.imshow(wordcloud)
        ax4.axis('off')


        fig.suptitle(f'{total} {keyword1} {keyword2} recipes')
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
