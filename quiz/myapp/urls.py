from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('quiz/', views.quiz, name='quiz'),
    path("quiz_questions/", views.quiz_questions, name="quiz_questions"),
    path('submit_answer/', views.submit_answer, name='submit_answer'),
    path('score/', views.score, name='score'),


]

