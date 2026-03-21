from django.urls import path
from . import views
from .views import submit_answer

app_name = 'quizzes'

urlpatterns = [
    path('', views.home,name='home'),
    path('category/<int:category_id>/start/', views.start_quiz, name='start_quiz'),
    path('category/<int:category_id>/questin/', views.quiz_question,name='quiz_question'),
    path('category/<int:category_id>/answer/',views.submit_answer,name='submit_answer'),
    path('category/<int:category_id>/results',views.quiz_results,name='results'),
]
