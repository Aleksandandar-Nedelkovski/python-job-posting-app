from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^quotes$', views.quotes),
    url(r'^post_quote$', views.post_quote),
    url(r'^delete$', views.delete),
    url(r'^user/(?P<id>[0-9]+)$', views.users_id),
    url(r'^user/(?P<id>[0-9]+)/edit$', views.edit),
    url(r'^user/(?P<id>[0-9]+)/update$', views.update),
]