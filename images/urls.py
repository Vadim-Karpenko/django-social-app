from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^create/$', views.image_create, name='create'),
    url(r'^detail/(?P<id>\d+)/$', views.image_detail, name='detail'),
    url(r'^like/$', views.image_like, name='like'),
    url(r'^$', views.image_list, name='list'),
    url(r'^delete/$', views.image_delete, name='image_delete'),
]
