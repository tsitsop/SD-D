from django.conf.urls import url
from . import views #import views from current package

urlpatterns = [
    #url is regexp that simply starts (^) and ends ($) - essentially just an index
    url(r'^$', views.HomeView.as_view(), name='get'),
    url(r'^contact/',views.ContactView.as_view(), name='get'),
    url(r'^statistics/', views.StatView.as_view(), name='statistics')
]
