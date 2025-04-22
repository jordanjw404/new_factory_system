from django.shortcuts import render

# Create your views here.
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

# Create User views here.
def UserView(request):
    users = User.objects.all()
    password = 'password'
    hashed_password = make_password(password)
    return render(request, 'create_user.html', 
                {'users': users, 'hashed_password': hashed_password})


def dashboard_view(request):
    return render(request, 'core/pages/dashboard.html')