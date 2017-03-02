from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^profile$', views.profile),
    # url(r'^addFriend/(?P<id>\d+)$', views.addFriend),
    url(r'^addFriend$', views.addFriend),
    url(r'^logout$', views.logout),
]
