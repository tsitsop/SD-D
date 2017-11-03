from django.conf.urls import url
from . import views

urlpatterns = [
	# /player/
    url(r'^$', views.index, name = 'index'),

    # /player/712/
    url(r'^(?P<player_id>[0-9]+)/$', views.detail, name = 'detail') 
]