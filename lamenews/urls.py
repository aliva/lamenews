from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'post/(?P<title>.*)$', 'lamenews.views.post', name='lamenews'),
    url(r'submit$', 'lamenews.views.submit', name='lamenews'),
    url(r'logout$', 'lamenews.views.logout', name='lamenews'),
    url(r'login', 'lamenews.views.login', name='lamenews'),
    url(r'register', 'lamenews.views.register', name='lamenews'),
    url(r'', 'lamenews.views.root', name='lamenews'),
)