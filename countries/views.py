from django.shortcuts import render

from countries.queries.remote import get_list_of_countries


def index(request):
    countries = get_list_of_countries()
    return render(request, 'index.html', {'countries': countries})
