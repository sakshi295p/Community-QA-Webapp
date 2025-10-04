from django.contrib import admin
from django.urls import path,include
from QandA import views

urlpatterns = [
    path('',views.home, name='home'),
    path('home',views.home, name='home'),
    path('login',views.Login, name='login'),
    path('logout',views.Logout, name='logout'),
    path('createNewAccount',views.create_new_accout, name='createNewAccount'),
    path('createpost',views.create_post, name='createPost'),
    path('question/<int:id>',views.question, name='question'),
    path('answer/<int:id>',views.answer, name='answer'),
    path('edit/<int:id>',views.edit, name='edit'),
    path('delete/<int:id>',views.delete, name='delete')
]