from django.urls import path
from . import views

app_name = 'test01'


urlpatterns = [
    path('post-list/', views.post_list, name='post_list'),
    path('post-detail/<int:pk>', views.post_detail, name='post_detail'),
    path('ticket/', views.ticket, name='ticket'),
    path('post-detail/<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.post_search, name='post_search'),
]