from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration$', views.registration),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^showDestination/(?P<id>\d+)$', views.showDestination),
    url(r'^addTrip$', views.addTrip),
    url(r'^showTrip$', views.showTrip),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout)
]
