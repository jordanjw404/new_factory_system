from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from .forms import CustomLoginForm

# ✅ Dashboard view (protected)
@login_required
def dashboard_view(request):
    return render(request, 'core/pages/dashboard.html')

# ✅ Create User view (protected)
@login_required
def UserView(request):
    users = User.objects.all()
    password = 'password'
    hashed_password = make_password(password)
    return render(request, 'create_user.html', 
                {'users': users, 'hashed_password': hashed_password})

# ✅ Login view (public)
class CustomLoginView(LoginView):
    template_name = 'core/pages/login.html'


def root_redirect_view(request):
    return redirect('login')


class CustomLoginView(LoginView):
    template_name = 'core/pages/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return '/dashboard/'

