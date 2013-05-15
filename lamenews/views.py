from django.shortcuts import render
from django.contrib.auth.views import logout as logout_django
from django.contrib.auth.views import login as login_django
from django.core.urlresolvers import reverse

def root(request):
    return render(request, 'lamenews.html')

def logout(request):
    return logout_django(request, reverse('lamenews.views.root'))

def login(request):
    return login_django(request, 'lamelogin.html')