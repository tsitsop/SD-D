from django.conf.urls import url
from . import views

app_name = 'player'

urlpatterns = [
	# /player/
    url(r'^$', views.index, name = 'index'),

 	# /player/<player_id>/
    url(r'^(?P<player_id>[0-9]+)/$', views.detail, name = 'detail'),

    # /player/<player_id>/important
    url(r'^(?P<player_id>[0-9]+)/important/$', views.important, name = 'important') 
]