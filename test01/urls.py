from django.urls import path
from . import views

app_name = 'test01'


urlpatterns = [
    path('post-list/', views.post_list, name='post_list'),
    path('post-detail/<int:pk>', views.post_detail, name='post_detail'),
]