# content based recommendation system
# database:tmdb 5000 (kaggle)

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os 
import ast 
import nltk  #natural language processing 
from nltk.stem import PorterStemmer #to remove suffixes. imp for information retrieval
import sklearn 
from sklearn.feature_extraction.text import CountVectorizer # converts collection of text documents in matrix of token counts 
from sklearn.metrics.pairwise import cosine_similarity #to find cosine similarity between vectors
import pickle 

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

movies = movies.merge(credits, on ='title')
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]


#DATA ANALYZATION
def convert(text):
    l=[]
    for i in ast.literal_eval(text): #string to list
         l.append(i['name'])
    return l

movies['genres']=movies['genres'].apply(convert)
movies['keywords']=movies['keywords'].apply(convert)


def convert_cast(text):
    l=[]
    counter=0
    for i in ast.literal_eval(text): #string to list
        if counter<3:
         l.append(i['name'])
         counter+=1
    return l

movies['cast']=movies['cast'].apply(convert_cast)

def fetch_director(text):
    l=[]
    for i in ast.literal_eval(text):
        if i['job']=='Director':
            l.append(i['name'])
            break

    return l

movies['crew']=movies['crew'].apply(fetch_director)
movies.dropna(inplace=True) #remove missing values
movies['overview']=movies['overview'].apply(lambda x:x.split())  # converts string to list (depending on separartion using commas)

def remove_space(word):
    l=[]
    for i in word:
        l.append(i.replace(" ",""))
    return l

movies['cast']=movies['cast'].apply(remove_space)
movies['crew']=movies['crew'].apply(remove_space)
movies['genre']=movies['genres'].apply(remove_space)
movies['keywords']=movies['keywords'].apply(remove_space)

movies['tags']=movies['overview']+movies['genres']+movies['keywords']+movies['cast']+movies['crew']

new_df=movies[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x: " ".join(x))#join if seperated by single comma, keep separated if double comma
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())#convert all words to lowercase in tags

#function to remove suffixes
ps=PorterStemmer()
def stems(text):
  l=[]
  for i in text.split():
    l.append(ps.stem(i))
  return " ".join(l)

  new_df['tags']=new_df['tags'].apply(stems) 


#to remove meaningless words
cv=CountVectorizer(max_features=5000, stop_words='english')
vector = cv.fit_transform(new_df['tags']).toarray()


#to find cosine similarity between vectors 
similarity = cosine_similarity(vector)

#function to recommend movie
def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])  #sort similarity in descending order
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)


pickle.dump(new_df, open('artifacts/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))