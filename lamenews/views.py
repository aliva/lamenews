from lamenews import forms
from lamenews import models

from django.shortcuts import render, redirect
from django.contrib.auth.views import logout as logout_view
from django.contrib.auth.views import login as login_view
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.http.response import HttpResponse

def root(request):
    context = {
        'recent':models.Post.objects.get_recent(),
        'top':models.Post.objects.get_top(),
    }
    return render(request, 'lame/index.html', context)

def logout(request):
    return logout_view(request, reverse('lamenews.views.root'))

def login(request):
    return login_view(request, 'lame/login.html')

def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid() == True:
            form.save()
            user = authenticate(username=form.cleaned_data['username'],
                                password=form.cleaned_data['password1'])
            login_user(request, user)
            return root(request)
    else:
        form = forms.RegisterForm()
    context = {
        'register_form': form,
    }
    return render(request, 'lame/register.html', context)

def post(request, title):
    try:
        post = models.Post.objects.get(title=title)
        post.visit_count+=1
        post.save()
        return render(request, 'lame/post.html', {'post':(post,)})
    except models.Post.DoesNotExist:
        return HttpResponse('not found')

def submit(request):
    if not request.user.is_authenticated():
        return redirect(reverse('lamenews.views.login')+'?next='+reverse('lamenews.views.submit'))
    if request.method == 'POST':
        form = forms.PostForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.creator = request.user
            obj.save()
            form.save_m2m()
            return redirect(reverse('lamenews.views.post', args=[obj.title]))
    else:
        form = forms.PostForm()
    context = {
        'form': form,
    }
    return render(request, 'lame/submit.html', context)

def vote(request, id, value):
    msg ='what'
    if not request.user.is_authenticated():
        msg = 'login to vote'
    else:
        try:
            msg = models.Post.objects.get(id=id).vote_post(request.user, value)
        except models.Post.DoesNotExist:
            msg = 'does not exist'
    return HttpResponse(msg)