from SPARQLWrapper import SPARQLWrapper, JSON


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
        "PREFIX dbo: <http://dbpedia.org/ontology/>PREFIX dbr: <http://dbpedia.org/resource/>SELECT distinct "
        "?country_name ?country_capitalWHERE {?country a dbo:Country.?country rdfs:label ?country_name.?country "
        "dbo:capital ?capital.?capital rdfs:label ?country_capital.FILTER NOT EXISTS { ?country dbo:dissolutionYear "
        "?yearEnd }.FILTER (langMatches(lang(?country_name), \"EN\")).FILTER (langMatches(lang(?country_capital), "
        "\"EN\")).FILTER (regex(?country_name, \"" + keyword + "\", \"i\" )).}ORDER BY ASC(?country_name) "
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
        "        SELECT distinct ?country_name ?country_capital ?country_abstract ?country_language ?country_currency\n"
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

    country_name = set()
    country_capital = set()
    country_abstract = set()
    country_language = set()
    country_currency = set()

    for country in results:
        country_name.add(country["country_name"]["value"])
        country_capital.add(country["country_capital"]["value"])
        country_abstract.add(country["country_abstract"]["value"])
        country_language.add(country["country_language"]["value"])
        country_currency.add(country["country_currency"]["value"])

    country_info = [list(country_name), list(country_capital), list(country_abstract), list(country_language),
                    list(country_currency)]
    print(country_info)
    return country_info
