from django.urls import path
from . import views

urlpatterns = [
    path('', views.startpage, name="startpage"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('home', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('mypage/<str:pk>/', views.userPage, name="user-page"),
    path('create-room', views.createRoom, name="create-room"),
    path('topic-room', views.createTopic, name="topic-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]
