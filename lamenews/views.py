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
        'most_visited':models.Post.objects.get_most_visited(),
        'most_upvoted': models.Post.objects.get_most_upvoted(),
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
        comment_form = forms.CommentForm()
        comments = models.Comment.objects.filter(post=post)
        return render(request, 'lame/post.html',
                        {'post':(post,),
                        'comment_form':comment_form,
                        'comments':comments}
                    )
    except models.Post.DoesNotExist:
        return HttpResponse('not found')

def tag(request, name):
    try:
        tag = models.Tag.objects.get(name=name)
        posts = tag.post_set.all()
    except models.Tag.DoesNotExist:
        posts = []
    return render(request, 'lame/post.html', {'post':posts})

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
    return render(request, 'lame/submitform.html', context)

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

def comment(request, id):
    if not request.user.is_authenticated():
        return redirect(reverse('lamenews.views.login'))
    try:
        post = models.Post.objects.get(id=id)
    except models.Post.DoesNotExist:
        return HttpResponse('post not found')
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.post = post
            obj.save()
    return redirect(reverse('lamenews.views.post', args=[post.title,]))
