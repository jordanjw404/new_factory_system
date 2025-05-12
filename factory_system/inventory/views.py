from django.shortcuts import render
from django.http import HttpResponse

def inventory_list(request):
    return HttpResponse("Inventory List")
