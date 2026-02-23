from django.urls import path
from . import views

app_name = 'quizzes'

urlpatterns = [
    path('', views.home,name='home'),
    path('category/<int:category_id>/', views.start_quiz, name='start_quiz'),
    path('category/<int:category_id>/questin/', views.quiz_question,name='quiz_question'),
]