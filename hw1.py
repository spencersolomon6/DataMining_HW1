import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
from datetime import datetime
from collections import Counter
import os

# Question 1
def cardinality_items(filename):
  '''
  Takes a filename "*.csv" and returns an integer
  '''

  data = open(filename, 'r').readlines()

  expanded_data  = []
  for line in data:
    for word in line:
      expanded_data.append(word.strip().lower())

  return len(pd.unique(expanded_data))

print(f"Q1: {cardinality_items('basket_data.csv')}")

# Question 2
def all_itemsets(items, n):
  '''
  Takes a list of unique items and an integer N and outputs all of the possible
  unqiue itemsets with non-repeating N items
  '''
  results = []

  while len(items) >= n:
    first = items[0]
    rest = items[1:]

    while len(rest) >= n - 1:
      result = [first]
      for i in range(n - 1):
        result.append(rest[i])

      results.append(result)
      del rest[0]

    del items[0]

  return results

test_itemset = all_itemsets(["ham", "cheese", "bread"], 2)
print(f"Q2: {test_itemset}")

# Question 3
def preprocess_combined_netflix_data():
  if not os.path.exists("NetflixData/combined_data.csv"):
    write_combined_csv()

  data = pd.read_csv("NetflixData/combined_data.csv", names=['id', "userid", 'rating', 'rating-date'], header=None)

  print(data.columns)

  return data

def write_combined_csv():
  new_csv = open(f"NetflixData/combined_data.csv", 'w')

  for i in range(1, 5):
    current_data = list()
    filename = f"NetflixData/combined_data_{i}.txt"
    with open(filename, 'r') as f:

      for line in f:
        if f":" in line.strip():
          id = int(line.split(':')[0].strip())

          if id % 500 == 0:
            print(f'Processing results for movie #{id}')
          continue

        current_line = line.split(',')

        rating_date = None if current_line[2] == 'NULL' else datetime.strptime(current_line[2].strip(), "%Y-%m-%d")
        new_csv.write(f'{id},{current_line[0]},{current_line[1]},{rating_date}\n')


combined_data = preprocess_combined_netflix_data()

print(f"3a: {len(combined_data)}")

unique_users = pd.unique(combined_data['userid'])
print(f'3b: {len(unique_users)}')

min_year = combined_data['rating-date'].min()
max_year = combined_data['rating-date'].max()
print(f'3c: {min_year}-{max_year}')

# Question 4
def preprocess_movie_titles():
  cols = ['id', 'release-year', 'title']
  data = pd.DataFrame(columns=cols)

  filename =  "NetflixData/movie_titles.csv"
  with open(filename, 'r', encoding='cp1252') as f:

    for line in f:
      current_data = {}

      current_line = line.split(',')
      current_data['id'] = int(current_line[0])
      current_data['release-year'] = None if current_line[1] == 'NULL' else datetime.strptime(current_line[1], '%Y')
      current_data['title'] = ''.join(current_line[2:]).strip().lower()

      data = data.append(current_data, ignore_index=True)

  return data

movie_titles = preprocess_movie_titles()

unique_titles = pd.unique(movie_titles['title'])
print(f'4a: {len(unique_titles)}')

title_counts = Counter(movie_titles['title'])
four_plus_titles = {title: count for title, count in title_counts.items() if count >= 4}
print(f'4b: {len(four_plus_titles)}')

# Question 5
ratings_counts = Counter(combined_data['userid'])
filtered_counts = {userid: count for userid, count in ratings_counts.items() if count == 200}
print(f'5a: {len(filtered_counts)}')

min_user =  min(filtered_counts.keys())
five_star_movies = combined_data[combined_data['userid'] == min_user][combined_data['rating'] == 5]

print('5b:\n')
for i, movie in five_star_movies.iterrows():
  print(movie_titles[movie_titles['id'] == movie['id']]['title'].values[0])
