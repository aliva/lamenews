from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'logout$', 'lamenews.views.logout', name='lamenews'),
    url(r'login', 'lamenews.views.login', name='lamenews'),
    url(r'', 'lamenews.views.root', name='lamenews'),
)