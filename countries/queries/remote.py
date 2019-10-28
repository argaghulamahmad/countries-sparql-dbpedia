from SPARQLWrapper import SPARQLWrapper, JSON


def get_list_of_countries():
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

    list_of_countries = []
    for result in results["results"]["bindings"]:
        list_of_countries.append(result["country"]["value"])

    return list_of_countries
