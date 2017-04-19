from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'game/(?P<name>\w{0,50})/$', views.game, name='game'),
    url(r'^', views.upload_file, name='upload'),
]

