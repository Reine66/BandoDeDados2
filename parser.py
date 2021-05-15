"""
Nota:
Este programa foi adaptado de 
https://github.com/chezou/amazon-movie-review/blob/master/src/preparation/parse-amazon-meta.py
"""

import re
import gzip
from tqdm import tqdm

def rename_review_key(entry):
  if(b'reviews' in entry and type(entry[b'reviews']) == type('')):
    temp = entry[b'reviews']
    del entry[b'reviews']
    entry['review_stats'] = temp
  return entry

def parse(filename, total):
  
  f = gzip.open(filename, 'r')
  entry = {}
  categories = []
  reviews = []
  similar_items = []
  
  pular_primeiras_linhas = 0
  for line in tqdm(f, total=total):
    if not pular_primeiras_linhas < 7:
        
        line = line.strip()
        colonPos = line.find(b':')
        
        #print("Linha - ", line)
       
        if line.startswith(b"Id"):
            
            if reviews:
                entry["reviews"] = reviews
            if categories:
                entry["categories"] = categories
            entry = rename_review_key(entry)
            yield entry
            entry = {}
            categories = []
            reviews = []
            rest = line[colonPos+2:]
            entry["id"] = str(rest.strip(), errors='ignore')
      
        elif line.startswith(b"similar"):
            similar_items = line.split()[2:]
            entry['similar_items'] = similar_items

        # "cutomer" is typo of "customer" in original data
        elif line.find(b"cutomer:") != -1:
            review_info = line.split()

            reviews.append({'_date': review_info[0],
                            'customer_id': review_info[2], 
                            'rating': int(review_info[4]), 
                            'votes': int(review_info[6]), 
                            'helpful': int(review_info[8])})

        elif line.startswith(b"|"):
            categories.append(line)

        elif colonPos != -1:
            eName = line[:colonPos]
            rest = line[colonPos+2:]
            
            if not eName == 'Total items':
                if not eName == 'reviews':
                    if eName == b'categories':
                       entry['categories_id'] = str(rest.strip(), errors='ignore')  
                    else:
                        if eName == b'reviews':
                            
                            aux = str(rest.strip())
                            aux = aux.replace("'", "")
                            s1 = aux.split(' ')
                            
                            total      = float(s1[1])
                            downloaded = float(s1[4])
                            avg_rating = float(s1[8])

                            entry['reviews_total'] = total
                            entry['reviews_downloaded'] = downloaded
                            entry['reviews_avg_rating'] = avg_rating

                        else:
                            entry[eName] = str(rest.strip(), errors='ignore')
       
    pular_primeiras_linhas = pular_primeiras_linhas + 1

  if reviews:
    entry["reviews"] = reviews
  if categories:
    entry["categories"] = categories
  entry = rename_review_key(entry)
  yield entry

if __name__ == '__main__':
    file_path = "./amazon-meta.txt.gz"

    import simplejson

    for e in parse(file_path, 15010574):
        if e:
            print(simplejson.dumps(e))
            
    