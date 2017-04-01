from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'index', views.index, name='index'),
    url(r'upload', views.upload_file, name='upload'),
    url(r'game/(?P<name>\w{0,50})/$', views.game, name='game'),
]

