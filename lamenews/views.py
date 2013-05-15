from lamenews import forms

from django.shortcuts import render
from django.contrib.auth.views import logout as logout_view
from django.contrib.auth.views import login as login_view
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user

def root(request):
    return render(request, 'lamenews.html')

def logout(request):
    return logout_view(request, reverse('lamenews.views.root'))

def login(request):
    return login_view(request, 'lamelogin.html')

def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid() == True:
            form.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login_user(request, user)
            return root(request)
    else:
        form = forms.RegisterForm()
    context = {
        'register_form': form,
    }
    return render(request, 'lameregister.html', context)