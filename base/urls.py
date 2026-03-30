from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),

    path('room/<str:pk>/', views.RoomView.as_view(), name="room"),

    path('create-room', views.CreateRoomView.as_view(), name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoomView.as_view(), name="update-room"),
    path('delete-room/<str:pk>/', views.DeleteRoomView.as_view(), name="delete-room"),

    path('login/', views.LoginView.as_view(), name="login"),
    path('register/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.LogoutView.as_view(), name="logout"),

    path('delete-message/<str:pk>/', views.DeleteMessageView.as_view(), name="delete-message"),

    path('profile/<str:pk>/', views.UserProfileView.as_view(), name="user-profile"),
    path('update-user/', views.UpdateUserView.as_view(), name="update-user"),

    path('add-topic/', views.AddTopicView.as_view(), name="add-topic"),
]