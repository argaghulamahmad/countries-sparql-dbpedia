from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbr: <http://dbpedia.org/resource/>

    SELECT ?country ?capital
    WHERE {
     ?country a dbo:Country.
     ?country dbo:capital ?capital.
     FILTER NOT EXISTS { ?country dbo:dissolutionYear ?yearEnd }
    }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

for result in results["results"]["bindings"]:
    print(result["country"]["value"])
