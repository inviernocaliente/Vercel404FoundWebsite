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
    path('lesson/<int:lesson_id>/redirect/', views.lesson_redirect, name='lesson_redirect'),
    path('lesson/<int:lesson_id>/<int:lesson_page_id>/', views.lesson_page_detail, name='lesson_page_detail'),
    path('complete_lesson/<int:lesson_page_id>/', views.complete_lesson, name='complete_lesson'),

    #----------------------------------Misc.----------------------------------------------#

    path('aboutPage', views.aboutPage, name='aboutPage'),
    path('opportunitiesPage', views.opportunitiesPage, name='opportunitiesPage'),

    #-------------------------------------Admin-------------------------------------------#

    path('adminHome', views.adminHome, name='adminHome'),
    path('lessonAdminPage/<int:lesson_id>/', views.lessonAdminPage, name='lessonAdminPage'),
    path('lesson/<int:lesson_id>/edit', views.lesson_detail_admin, name='lesson_detail_admin'),

    path('lesson/<int:lesson_id>/page/<int:lesson_page_id>/edit/', views.edit_lesson_page, name='edit_lesson_page'),

    path('lesson/<int:lesson_id>/create-lesson-page/', views.create_lesson_page, name='create_lesson_page'),
    path('lesson/<int:lesson_id>/delete-lesson-page/<int:lesson_page_id>/', views.delete_lesson_page, name='delete_lesson_page'),
]