from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from .models import Inventory


def inventory_list_view(request):
    inventory_items = Inventory.objects.select_related("location").all()
    context = {
        "inventory_items": inventory_items,
    }
    return render(request, "inventory/inventory_list.html", context)


def cabinet_list(request):
    return HttpResponse("Cabinet List")


def board_list(request):
    return HttpResponse("Board List")


def hardware_list(request):
    return HttpResponse("Hardware List")


def edgebanding_list(request):
    return HttpResponse("Edge Banding List")
