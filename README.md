# NoSQL

## MongoDB
Type: Base de données NoSQL orientée document.
Description: MongoDB est une base de données document-store où les données sont stockées sous forme de documents JSON/BSON. Elle est idéale pour gérer des données non structurées et évolutives.
Cas d'usage: Stockage d'objets complexes (par exemple, profils d'utilisateurs, articles, etc.).

- docker pull mongo
- docker run --name my-mongo -p 27017:27017 -d mongo
- Install dépendances : pip install pymongo
- Exécuter les scripts python : python3 test_mongo.py && python3 test2_mongo.py

## Redis
type: Base de données en mémoire clé-valeur.
Description: Redis est une base de données en mémoire utilisée principalement pour la mise en cache, les sessions, ou comme un store pour des structures de données en temps réel.
Cas d'usage: Cache, gestion de sessions, gestion des files d'attente.

- docker pull redis
- docker run --name my-redis -d redis
- docker exec -it my-redis redis-cli
- Exécuter les scripts python : python3 test_redis.py && python3 test2_redis.py 

## Neo4j
Type: Base de données graphique.
Description: Neo4j est une base de données graphique qui utilise des graphes pour représenter et interroger les relations entre des entités.
Cas d'usage: Représentation des relations complexes (par exemple, réseaux sociaux, recommandations, etc.).

- docker run\     
  \--name my_neo4j     
  \-p7474:7474 -p7687:7687     
  \-v ~/neo4j_data:/data     
  \-e NEO4J_AUTH=neo4j/password     
  \-d neo4j
    
- Install dépendances : pip install neo4j
- Exécuter le script python : python3 test_neo4j.py

## ELK Stack
Elasticsearch: Moteur de recherche et d’analyse basé sur Lucene.
Logstash: Outil d'ingestion et de traitement des logs.
Kibana: Interface web permettant de visualiser les données dans Elasticsearch.
Cas d'usage: Recherche, analyse des logs et données en temps réel.

- docker run -p 9200:9200 -p 9300:9300 -d -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0
- sudo apt-get install jq
- Une fois le docker-compose.yml créé -> il faut exécuter docker-compose up -d
- Créer des indexs à partir des fichiers json :
      
        curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/receipe/_bulk --data-binary "@receipe.json" &&\
        printf "\n✅ Insertion receipe index to elastic node OK ✅ "
        
        curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/accounts/docs/_bulk --data-binary "@accounts.json"
        printf "\n✅ Insertion accounts index to elastic node OK ✅ "
                                                    
        curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/movies/_bulk --data-binary "@movies.json"
        printf "\n✅ Insertion movies index to elastic node OK ✅ "
                                                    
        curl -s -H "Content-Type: application/x-ndjson" -XPOST localhost:9200/products/_bulk --data-binary "@products.json"
        printf "\n✅ Insertion products index to elastic node OK ✅ "
        
- Pour Elastic Python API (elk-python) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - Exécuter le script python : python3 elk_test.py

- Pour ELK CSV (elk-csv) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d
  - curl -X GET "0.0.0.0:9200/csv-data/_search?q=*" | jq

- Pour ELK JSON (elk-json) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d
  - curl -X GET "0.0.0.0:9200/json-data/_search?q=*" | jq

- Pour ELK Serveur Apache Kibana (elk-apache-server) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d

- Pour ELK Stack avec script Python logs pour diagram avec Filebeat (elk-filebeat-python) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d
  - Se connecter au localhost:5601

- Pour ELK avec toutes les pipelines ci-dessus regroupées (elk-stack-multiple) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d

- Pour ELK Stack avec Metricbeat "surveillance monitoring administrators" (elk-monitoring-admin) :
  - docker pull docker.elastic.co/elasticsearch/elasticsearch:7.11.1
  - docker-compose up -d
  - Se connecter au localhost:5601
