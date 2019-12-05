import rdflib
import rdfextras
from SPARQLWrapper import SPARQLWrapper, JSON

prefix_dict = {
    "ex": "http://example.org/data/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "dbr": "http://dbpedia.org/resource/",
    "dbp": "http://dbpedia.org/property/",
    "dbo": "http://dbpedia.org/ontology/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "dct": "http://purl.org/dc/terms/",
    "dbc": "http://dbpedia.org/page/Category:",
}


def get_list_of_countries():
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery("\n"
                    "        PREFIX dbo: <http://dbpedia.org/ontology/>\n"
                    "        PREFIX dbr: <http://dbpedia.org/resource/>\n"
                    "        \n"
                    "        SELECT distinct ?country_name\n"
                    "        WHERE {\n"
                    "         ?country a dbo:Country.\n"
                    "         ?country rdfs:label ?country_name.\n"
                    "         ?capital rdfs:label ?country_capital.\n"
                    "         FILTER NOT EXISTS { ?country dbo:dissolutionYear ?yearEnd }.\n"
                    "         FILTER (langMatches(lang(?country_name), \"EN\")).\n"
                    "        }\n"
                    "        ORDER BY ASC(?country_name)\n"
                    "    ")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    list_of_countries = []
    for result in results:
        list_of_countries.append(result['country_name']['value'])

    return list_of_countries


def filter_list_of_countries(keyword):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
        "\n"
        "            PREFIX dbo: <http://dbpedia.org/ontology/>\n"
        "            PREFIX dbr: <http://dbpedia.org/resource/>\n"
        "            SELECT distinct ?country_name\n"
        "            WHERE {\n"
        "                ?country a dbo:Country.\n"
        "                ?country dbo:capital ?capital.\n"
        "                ?country rdfs:label ?country_name.\n"
        "                FILTER NOT EXISTS {\n"
        "                    ?country dbo:dissolutionYear ?yearEnd\n"
        "                }.\n"
        "                FILTER (langMatches(lang(?country_name), \"EN\")).\n"
        "                FILTER (regex(?country_name, \"" + keyword + "\", \"i\" )).\n"
                                                                      "            }\n"
                                                                      "            ORDER BY ASC(?country_name)\n"
                                                                      "        "
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    list_of_countries = []
    for result in results:
        list_of_countries.append(result['country_name']['value'])

    return list_of_countries


def information_of_a_country(keyword):
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(
        "\n"
        "        PREFIX dbo: <http://dbpedia.org/ontology/>\n"
        "        PREFIX dbr: <http://dbpedia.org/resource/>\n"
        "        \n"
        "        SELECT distinct ?country_name ?capital ?country_capital ?country_abstract ?language ?country_language ?currency ?country_currency\n"
        "        WHERE {\n"
        "         ?country a dbo:Country.\n"
        "         ?country rdfs:label ?country_name.\n"
        "         ?country dbo:capital ?capital.\n"
        "         ?capital rdfs:label ?country_capital.\n"
        "         ?country dbo:abstract ?country_abstract.\n"
        "         ?country dbo:language ?language.\n"
        "         ?language rdfs:label ?country_language.\n"
        "         ?country dbo:currency ?currency.\n"
        "         ?currency rdfs:label ?country_currency.\n"
        "         FILTER NOT EXISTS { ?country dbo:dissolutionYear ?yearEnd }.\n"
        "         FILTER (langMatches(lang(?country_name), \"EN\")).\n"
        "         FILTER (langMatches(lang(?country_capital), \"EN\")).\n"
        "         FILTER (langMatches(lang(?country_abstract), \"EN\")).\n"
        "         FILTER (langMatches(lang(?country_language), \"EN\")).\n"
        "         FILTER (langMatches(lang(?country_currency), \"EN\")).\n"
        "         FILTER (regex(?country_name, \"" + keyword + "\", \"i\")).\n"
                                                               "        }\n"
                                                               "        ORDER BY ASC(?country_name)\n"
                                                               "        "
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()["results"]["bindings"]

    country_name = []
    country_capital = []
    country_abstract = []
    country_language = []
    country_currency = []

    for country in results:
        country_name.append(country["country_name"]["value"])

        is_exist_country_capital = False
        is_exist_country_language = False
        is_exist_country_currency = False

        for i in range(len(max(
            country_capital,country_language,country_currency))):
            try:
                if country["capital"]["value"] == country_capital[i][1]:
                    is_exist_country_capital = True
            except: continue

            try:
                if country["language"]["value"] == country_language[i][1]:
                    is_exist_country_language = True
            except: continue

            try:
                if country["currency"]["value"] == country_currency[i][1]:
                    is_exist_country_currency = True
            except: continue

        if not is_exist_country_capital:
            country_capital.append([country["country_capital"]["value"],
            country["capital"]["value"]])
        
        country_abstract.append(country["country_abstract"]["value"])

        if not is_exist_country_language:
            country_language.append([country["country_language"]["value"],
            country["language"]["value"]])

        if not is_exist_country_currency:
            country_currency.append([country["country_currency"]["value"],
            country["currency"]["value"]])

    local_dict = check_local_store(keyword)

    # converts data from local store to list of tuples
    local_url = []
    new_local_dict = {}
    for key, value in local_dict:
        local_url.append(key)

        key_split = key.split("/")
        new_local_dict[key_split[-1]] = value

    local_tuples = list(new_local_dict.items())

    local_url = sorted(local_url, key=lambda x: x.split("/")[-1], reverse=False)
    local_tuples.sort()

    for i in range(len(local_tuples)):
        local_tuples[i] = [local_url[i], local_tuples[i][0], local_tuples[i][1]]

    country_info = [list(country_name), list(country_capital), list(country_abstract), list(country_language),
                    list(country_currency)]

    # append data from local store to country_info
    country_info.append(local_tuples)

    return country_info

def check_local_store(keyword):
    keyword2 = "dbr:" + keyword.replace(" ", "_")
    filename = "local-schema.ttl"
    rdfextras.registerplugins()

    local_graph = rdflib.Graph()
    local_graph.parse(filename, format='n3')

    # TODO: Handle regex query
    results = local_graph.query("""
        SELECT ?p ?o
        WHERE {
        %s ?p ?o.
        }
        """ % keyword2)

    return results
