from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, dashboard_view, root_redirect_view

urlpatterns = [
    path("", root_redirect_view, name="root"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
