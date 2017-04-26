from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^add_quote$', views.add_quote),
    url(r'^fav/(?P<id>\d+)$', views.fav),
    url(r'^remove/(?P<id>\d+)$', views.remove),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^logout$', views.logout),
]
