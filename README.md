# NoSQL

Redis :
  - docker pull redis
  - docker run --name my-redis -d redis
  - docker exec -it my-redis redis-cli
  - Exécuter les scripts python : python3 test_redis.py && python3 test2_redis.py 

Mongo :
  - docker pull mongo
  - docker run --name my-mongo -p 27017:27017 -d mongo
  - Install dépendances : pip install pymongo
  - Exécuter les scripts python : python3 test_mongo.py && python3 test2_mongo.py

Neo4j :
  - docker run\     
    \--name my_neo4j     
    \-p7474:7474 -p7687:7687     
    \-v ~/neo4j_data:/data     
    \-e NEO4J_AUTH=neo4j/password     
    \-d neo4j
    
  - Install dépendances : pip install neo4j
  - Exécuter le script python : python3 test_neo4j.py

ELK Stack :
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
        
  - Pour ELK Python API : 
          - docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.11.1
          - Exécuter le script python : python3 elk_test.py
                            
