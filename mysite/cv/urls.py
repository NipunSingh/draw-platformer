from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'game/(?P<name>\w{0,50})/$', views.game, name='play_game'),
    url(r'game/(?P<name>\w{0,50})/updatescore/', views.update_score, name='update_score'),
    url(r'game/(?P<name>\w{0,50})/updatevotes/', views.update_votes, name='update_votes'),
    url(r'discover/', views.discover, name='discover'),
    url(r'^', views.upload_file, name='upload'),
]

