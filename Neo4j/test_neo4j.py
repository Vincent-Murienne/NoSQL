from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "password"

driver = GraphDatabase.driver(uri, auth=(user, password))

def run_query(query):
    with driver.session() as session:
        result = session.run(query)
        return list(result)

delete_nodes_and_relationships = "MATCH (n) DETACH DELETE n"
run_query(delete_nodes_and_relationships)


persons = [
    "CREATE (p:Person {name: 'Alice', age: 30})",
    "CREATE (p:Person {name: 'Bob', age: 28})",
    "CREATE (p:Person {name: 'Charlie', age: 35})"
]

for person in persons:
    run_query(person)

relationships = [
    "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Bob'}) CREATE (a)-[:FRIEND]->(b)",
    "MATCH (a:Person {name: 'Alice'}), (b:Person {name: 'Charlie'}) CREATE (a)-[:FRIEND]->(b)",
    "MATCH (a:Person {name: 'Bob'}), (b:Person {name: 'Charlie'}) CREATE (a)-[:FRIEND]->(b)"
]

for relationship in relationships:
    run_query(relationship)

query_all_persons = "MATCH (p:Person) RETURN p.name, p.age"
results = run_query(query_all_persons)

print("Registered People:")
for record in results:
    print(f"Name: {record['p.name']}, Age: {record['p.age']}")

def get_friends(name):
    query = f"MATCH (p:Person {{name: '{name}'}})-[:FRIEND]->(friend) RETURN friend.name, friend.age"
    return run_query(query)

name = "Alice"
friends = get_friends(name)

print(f"Friends of {name}:")
for record in friends:
    print(f"Name: {record['friend.name']}, Age: {record['friend.age']}")

actors = [
    "CREATE (a:Actor {name: 'Tom Hanks'})",
    "CREATE (a:Actor {name: 'Meryl Streep'})",
    "CREATE (a:Actor {name: 'Tom Cruise'})",
    "CREATE (a:Actor {name: 'Julia Roberts'})"
]

movies = [
    "CREATE (m:Movie {title: 'Forrest Gump', year: 1994})",
    "CREATE (m:Movie {title: 'The Post', year: 2017})",
    "CREATE (m:Movie {title: 'Top Gun', year: 1986})",
    "CREATE (m:Movie {title: 'Pretty Woman', year: 1990})"
]

for actor in actors:
    run_query(actor)

for movie in movies:
    run_query(movie)

relationships = [
    "MATCH (a:Actor {name: 'Tom Hanks'}), (m:Movie {title: 'Forrest Gump'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Tom Hanks'}), (m:Movie {title: 'The Post'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Meryl Streep'}), (m:Movie {title: 'The Post'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Tom Cruise'}), (m:Movie {title: 'Top Gun'}) CREATE (a)-[:ACTED_IN]->(m)",
    "MATCH (a:Actor {name: 'Julia Roberts'}), (m:Movie {title: 'Pretty Woman'}) CREATE (a)-[:ACTED_IN]->(m)"
]

for relationship in relationships:
    run_query(relationship)

run_query("CREATE (m:Movie {title: 'The Devil Wears Prada', year: 2006})")
run_query("MATCH (a:Actor {name: 'Meryl Streep'}), (m:Movie {title: 'The Devil Wears Prada'}) CREATE (a)-[:ACTED_IN]->(m)")

query_check = "MATCH (a:Actor)-[:ACTED_IN]->(m:Movie) RETURN a.name, m.title, m.year LIMIT 10"
results = run_query(query_check)

print("Existing Actors and Movies:")
for record in results:
    print(f"Actor: {record['a.name']}, Movie: {record['m.title']} ({record['m.year']})")

def recommend_movies(liked_actor_name):
    query = f"""
    MATCH (liked_actor:Actor {{name: '{liked_actor_name}'}})-[:ACTED_IN]->(liked_movie:Movie)
    MATCH (other_actor:Actor)-[:ACTED_IN]->(liked_movie)
    MATCH (other_actor)-[:ACTED_IN]->(recommended_movie:Movie)
    WHERE NOT (liked_actor)-[:ACTED_IN]->(recommended_movie)
    RETURN DISTINCT recommended_movie.title AS title, recommended_movie.year AS year
    ORDER BY year DESC
    """
    return run_query(query)

liked_actor_name = "Tom Hanks"
recommended_movies = recommend_movies(liked_actor_name)

print(f"Movie recommendations based on liking {liked_actor_name}:")
for record in recommended_movies:
    print(f"{record['title']} ({record['year']})")