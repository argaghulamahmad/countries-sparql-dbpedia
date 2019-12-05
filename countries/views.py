from django.shortcuts import render

from countries.queries.remote import filter_list_of_countries, information_of_a_country


def index(request):
    return render(request, 'index.html')


def search(request, keyword):
    countries = filter_list_of_countries(keyword)
    return render(request, 'search.html', {'countries': countries})


def detail(request, keyword):
    country_info = information_of_a_country(keyword)
    return render(request, 'detail.html', {'country_info': country_info, 'range_20': range(20)})
