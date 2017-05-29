from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'game/(?P<name>\w{0,50})/$', views.game, name='play_game'),
    url(r'game/(?P<name>\w{0,50})/updatescore/', views.update_score, name='update_score'),
    url(r'game/(?P<name>\w{0,50})/upvote/', views.upvote, name='upvote'),
    url(r'discover/', views.discover, name='discover'),
    url(r'^', views.upload_file, name='upload')
]

