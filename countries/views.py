from django.shortcuts import render

from countries.queries.remote import get_list_of_countries, filter_list_of_countries


def index(request):
    return render(request, 'index.html')


def search(request, keyword):
    countries = filter_list_of_countries(keyword)
    return render(request, 'search.html', {'countries': countries})
