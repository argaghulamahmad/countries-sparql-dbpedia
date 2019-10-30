from django.shortcuts import render

from countries.queries.remote import filter_list_of_countries


def index(request):
    return render(request, 'index.html')


def search(request, keyword):
    countries = filter_list_of_countries(keyword)
    return render(request, 'search.html', {'countries': countries})


def detail(request, keyword):
    return render(request, 'detail.html', {'name': keyword})
