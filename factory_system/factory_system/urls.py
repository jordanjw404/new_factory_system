"""
URL configuration for factory_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('customers/', include('customers.urls')),
    path("orders/", include("orders.urls")),
    path('production/', include(('production.urls', 'production'), namespace='production')),
<<<<<<< HEAD
<<<<<<< HEAD
    path("inventory/", include("inventory.urls", namespace="inventory")),

=======
    path('inventory/', include(('inventory.urls', 'inventory'), namespace='inventory')),
>>>>>>> b56bbc1 (Refactor inventory URLs and views; add specific views for cabinets, boards, hardware, and edge banding)
=======
    path("inventory/", include("inventory.urls", namespace="inventory")),

>>>>>>> d92dd45 (Implement inventory list view and template; add slug fields to models for better URL handling)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)