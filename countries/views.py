from django.shortcuts import render

from countries.queries.remote import get_list_of_countries, filter_list_of_countries


def index(request):
    countries = get_list_of_countries()
    return render(request, 'index.html', {'countries': countries})


def search(request, keyword):
    countries = filter_list_of_countries(keyword)
    return render(request, 'index.html', {'countries': countries})
