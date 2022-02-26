import requests
import pandas as pd
import re


def recommend_movie(movie_name):

  

  api_key = "API Key is here"

  movie_name = re.sub(r' ', '-',movie_name).lower()
  movie_name = re.sub(r'[^\w\s]', '-', movie_name)

  movie = requests.get("https://api.themoviedb.org/3/search/movie?api_key="+ api_key+"&query=" + movie_name)
  step = movie.json()
  movie_id = []
  for i in step["results"]:
    movie_id.append(i["id"])
  movie_id = "{}".format(movie_id[0])



  movie_data = requests.get("https://api.themoviedb.org/3/movie/" +movie_id+ "/credits?api_key=" + api_key)
  movie_data2 = movie_data.json()

  director_id = [] 
  for i in movie_data2["crew"]:
    if i["job"] == "Director": 
      director_id.append(i["id"])
  director_id = "{}".format(director_id[0])

  director = requests.get("https://api.themoviedb.org/3/person/"+director_id +"/movie_credits?api_key=" +  api_key)
  director_json= director.json()
    
  columns = ["title", "point"]
  df = pd.DataFrame(columns=columns)

  for i in director_json["crew"]:
    df.loc[len(df)]=[i['title'],i['vote_average']]


  print(df.sort_values("point",ascending=False).drop_duplicates().head(7))




