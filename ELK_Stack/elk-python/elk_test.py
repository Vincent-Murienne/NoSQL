import warnings
from elasticsearch import Elasticsearch
warnings.filterwarnings('ignore')


## Ping du container
import requests
res = requests.get('http://localhost:9200?pretty')
print(res.content)
es = Elasticsearch('http://localhost:9200')


## Create, delete and verify index
#create
print("Create :", es.indices.create(index="first_index",ignore=400))

#verify
print("Verify :", es.indices.exists(index="first_index"))

#delete
print("Delete :", es.indices.delete(index="first_index", ignore=[400,404]))


## Insert Document
#documents to insert in the elasticsearch index "cities"
doc1 = {"city":"New Delhi", "country":"India"}
doc2 = {"city":"London", "country":"England"}
doc3 = {"city":"Los Angeles", "country":"USA"}

#Inserting doc1 in id=1
es.index(index="cities", id=1, body=doc1)

#Inserting doc2 in id=2
es.index(index="cities", id=2, body=doc2)

#Inserting doc3 in id=3
es.index(index="cities", id=3, body=doc3)

# Trouver la fonction qui vérifie que votre index est bien crée.
exists = es.indices.exists(index="cities")
print(f"L'index cities existe: {exists}")

## Retrieve data with id get
retrieve = es.get(index="cities", id=2)
print("Data avec id 2 :", retrieve)

# Afficher uniquement les informations ci-dessous à partir de la variable res
# 'city': 'London', 'country': 'England'}
doc = {"city":"London", "country":"England"}
print("Doc exo :", doc)

## Mapping
print("Mapping :", es.indices.get_mapping(index='cities'))


## Endpoint search
endpoint = es.search(index="cities", body={"query":{"match_all":{}}})
print("Endpoint search : ",endpoint)

# Affiner ces critères de recherche avec _source
source = es.search(index="movies", body={
  "_source": {
    "includes": [
      "*.title",
      "*.directors"
    ],
    "excludes": [
      "*.actors*",
      "*.genres"
    ]
  },
  "query": {
    "match": {
      "fields.directors": "George"
    }
  }
})

print("Search avec _source : ", source)

## Logique Booléenne
bool = es.search(index="movies", body=
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "fields.directors": "George"
          }
        },
        {
          "match": {
            "fields.title": "Star Wars"
          }
        }
      ]
    }
  }
})

print("Logique Booléenne : ", bool)

## Logique Booléenne avec should_must
should_must = es.search(index="movies", body=
{
  "query": {
    "bool": {
      "must": [
                  { "match": { "fields.title": "Star Wars"}}
                  
      ],
      "must_not": { "match": { "fields.directors": "George Miller" }},
      "should": [
                  { "match": { "fields.title": "Star" }},
                  { "match": { "fields.directors": "George Lucas"}}
      ]
    }
  }
})

print("Logique Booléenne avec should_must : ", should_must)

## Logique Booléenne avec filter

filter = es.search(index="receipe", body={
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "ingredients.name": "parmesan"
          }
        }
      ], 
      "must_not": [
        {
          "match": {
            "ingredients.name": "tuna"
          }
        }
      ], 
      "filter": [
        {
          "range":{
            "preparation_time_minutes": {
              "lte":15
            }
          }
        }
        ]
    }
  }
})

print("Logique Booléenne avec filter : ", filter)

## Prefix
prefix = es.search(index="cities", body={"query": {"prefix" : { "city" : "l" }}})
print("Prefix : ", prefix)

## Regex
# tout afficher
regex_all = es.search(index="cities", body={"query": {"regexp" : { "city" : ".*" }}})
print("Regex : ", regex_all)

#afficher les cities qui commencent par L
regex_cities_L = es.search(index="cities", body={"query": {"regexp" : { "city" : "l.*" }}})
print("Regex cities qui commencent par L : ", regex_cities_L)

#afficher les cities qui commencent par L et terminent par n 
regex_cities_L_N = es.search(index="cities", body={"query": {"regexp" : { "city" : "l.*n" }}})
print("Regex cities qui commencent par L et terminent par n : ", regex_cities_L_N)

## Aggregations
#agregation simple -> movies/years
aggregation_simple = es.search(index="movies",body={"aggs" : {
    "nb_par_annee" : {
        "terms" : {"field" : "fields.year"}
}}})
print("Aggregation simple : ", aggregation_simple['aggregations'])

#agregation et stats simple -> moyennes des raitings 
aggregation_avg_raiting = es.search(index="movies",body={"aggs" : {
    "note_moyenne" : {
        "avg" : {"field" : "fields.rating"}
}}})
print("Aggregation et stats simple : ", aggregation_avg_raiting['aggregations'])

#agregation et stats simple -> stats basiques raitings/years
aggregation_years_raiting = es.search(index="movies",body={"aggs" : {
    "group_year" : {
        "terms" : { "field" : "fields.year" },
        "aggs" : {
            "note_moyenne" : {"avg" : {"field" : "fields.rating"}},
            "note_min" : {"min" : {"field" : "fields.rating"}},
            "note_max" : {"max" : {"field" : "fields.rating"}}
        }
}}})
print("Aggregation et stats simple : ", aggregation_years_raiting['aggregations'])

## DateTime aggregation
import datetime
docTime1 = {"city":"Bangalore", "country":"India","datetime": datetime.datetime(2018,1,1,10,20,0)} #datetime format: yyyy,MM,dd,hh,mm,ss
docTime2 = {"city":"London", "country":"England","datetime": datetime.datetime(2018,1,2,22,30,0)}
docTime3 = {"city":"Los Angeles", "country":"USA","datetime": datetime.datetime(2018,4,19,18,20,0)}
es.index(index="travel", id=1, body=docTime1)
es.index(index="travel", id=2, body=docTime2)
es.index(index="travel", id=3, body=docTime3)
#specify mapping and create index 
if es.indices.exists(index="travel"):
    es.indices.delete(index="travel", ignore=[400,404])

settings = {
    "settings": {
        "number_of_shards": 2,
        "number_of_replicas": 1
    },
    "mappings": {
            "properties": {
                "city": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "country": {
                        "type": "text",
                        "fields": {
                            "keyword": {
                                "type": "keyword",
                                "ignore_above": 256
                            }
                        }
                    },
                    "datetime": {
                        "type": "date",
                    }
        }
     }
}
es.indices.create(index="travel", ignore=400, body=settings)

es.indices.get_mapping(index='travel')

es.search(index="travel", body={"from": 0, "size": 0, "query": {"match_all": {}}, "aggs": {
                  "country": {
                      "date_histogram": {"field": "datetime", "calendar_interval": "year"}}}})



## Analyseur
#Analyseur exemple :
{
  "settings": {
    "analysis": { 
      "filter": {
        "french_elision": {
          "type": "elision",
          "articles_case": True,
          "articles": ["l", "m", "t", "qu", "n", "s", "j", "d", "c", "jusqu", "quoiqu", "lorsqu", "puisqu"]
        },
        "french_synonym": {
          "type": "synonym",
          "ignore_case": True,
          "expand": True,
          "synonyms": [
            "réviser, étudier, bosser",
            "mayo, mayonnaise",
            "grille, toaste"
          ]
        },
        "french_stemmer": {
          "type": "stemmer",
          "language": "light_french"
        }
      },
      "analyzer": {
        "french_heavy": {
          "tokenizer": "icu_tokenizer",
          "filter": [
            "french_elision",
            "icu_folding",
            "french_synonym",
            "french_stemmer"
          ]
        },
        "french_light": {
          "tokenizer": "icu_tokenizer",
          "filter": [
            "french_elision",
            "icu_folding"
          ]
        }
      }
    }
  }
}

# Traduction
phraseFr = {"text" : "Une phrase en français :) ..."}
print (es.index(index="french", id=1, body=phraseFr))

# Analyseur français
print (es.indices.analyze(index="french",body={
  "text" : "Je dois bosser pour mon QCM sinon je vais avoir une sale note :( ..."
}))