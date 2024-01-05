from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('home_studybuddy', views.home_studybuddy, name="home_studybuddy"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('update-user/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),

    #----------------------------- Course Section -------------------------------------#

    path('lessons_page', views.lessons_page, name="lessons_page"),
    path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('complete_lesson/<int:lesson_id>/', views.complete_lesson, name='complete_lesson'),
    path('aboutPage', views.aboutPage, name='aboutPage'),
]