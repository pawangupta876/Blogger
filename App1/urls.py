from django.conf.urls import url
from App1 import views
urlpatterns = [

    
    url(r'^$', views.register, name='register'),
    url(r'^login/', views.user_login, name='user_login'),
    url(r'^home_page/', views.home_page, name='home_page'),
    url(r'^logout/', views.user_logout, name='user_logout'),
    url(r'^profile/', views.profile, name='profile'),
    url(r'^profile_view/(?P<pk>\d+)/', views.profile_view, name='profile_view'),
    url(r'^comments/(?P<pk>\d+)/', views.comments, name = 'comments'),
    url(r'^comment_done/(?P<pk>\d+)/', views.comment_done, name = 'comment_done'),
    url(r'^returned/(?P<pk>\d+)/', views.returned, name = 'returned'),


]