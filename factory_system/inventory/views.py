from django.shortcuts import render
from django.http import HttpResponse

def inventory_list(request):
    return HttpResponse("Inventory List")

def cabinet_list(request):
    return HttpResponse("Cabinet List")

def board_list(request):
    return HttpResponse("Board List")

def hardware_list(request):
    return HttpResponse("Hardware List")

def edgebanding_list(request):
    return HttpResponse("Edge Banding List")

