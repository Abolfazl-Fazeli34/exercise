from django.urls import path
from . import views

app_name = 'test01'


urlpatterns = [
    path('post_list', views.post_list, name='post_list'),
    path('post_detail/<int:pk>', views.post_detail, name='post_detail'),
]