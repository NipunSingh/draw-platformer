from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'play/(?P<map_name>\w{0,50})/updatescore', views.update_score, name='update_score'),
    url(r'play/(?P<map_name>\w{0,50})', views.game, name='play_game'),
    url(r'vote', views.vote, name='vote'),
    url(r'discover/page/(?P<page>\w{0,50})', views.discover, name='discover'),
    url(r'discover', views.discover_home, name='discover_home'),
    url(r'^', views.upload_file, name='upload')
]