from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetRoutes.as_view(), name="routes"),
    
    path('rooms/', views.RoomList.as_view(), name="rooms"),
    path('rooms/<str:pk>/', views.RoomDetail.as_view(), name="roomid"),
    
    path('topics/', views.TopicList.as_view(), name="topics"),
    path('topics/<str:pk>/', views.TopicDetail.as_view(), name="topic"),
    
    path('users/', views.UserList.as_view(), name="users"),
    path('users/<str:pk>/', views.UserDetail.as_view(), name="user"),
    
    path('badges/', views.BadgeList.as_view(), name="users"),
    path('badges/<str:pk>/', views.BadgeDetail.as_view(), name="user"),
]