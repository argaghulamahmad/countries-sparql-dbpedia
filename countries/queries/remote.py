from SPARQLWrapper import SPARQLWrapper, JSON


def get_list_of_countries():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("""
        PREFIX dbo: <http://dbpedia.org/ontology/>
        PREFIX dbr: <http://dbpedia.org/resource/>
        
        SELECT distinct ?country_name ?country_capital
        WHERE {
         ?country a dbo:Country.
         ?country rdfs:label ?country_name.
         ?country dbo:capital ?capital.
         ?capital rdfs:label ?country_capital.
         FILTER NOT EXISTS { ?country dbo:dissolutionYear ?yearEnd }.
         FILTER (langMatches(lang(?country_name), "EN")).
         FILTER (langMatches(lang(?country_capital), "EN")).
         FILTER (regex(?country_name, "indonesia", "i" )).
        }
        ORDER BY ASC(?country_name)
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    list_of_countries = []
    for result in results["results"]["bindings"]:
        list_of_countries.append(result["country"]["value"])

    return list_of_countries
