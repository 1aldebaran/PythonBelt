from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^main$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^wish_items/(?P<id>\d+)$', views.wish_items, name='wish_items'),
    url(r'^wish_items/create$', views.add_new_item, name='add_new_item'),
    url(r'^create_item$', views.create_item, name='create_item'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^add_item/(?P<id>\d+)$', views.add_item, name='add_item'),
    url(r'^delete_item/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^remove_item/(?P<id>\d+)$', views.remove, name='remove'),
]
