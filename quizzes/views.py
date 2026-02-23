# Create your views here.
from django. shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
import json
import random
from .models import Category, Question, Answer, QuizAttempt


def home(request):

    """ Главная страница с Категориями"""
    categories = Category.objects.all()
    return render (request, 'quizzes/home.html', {'categories': categories})

@login_required
def start_quiz(request, category_id):
    category = Category.objects.get(id=category_id )

    questions = list(Question.objects.filter(category=category).order_by('?')[:10])

    if len(questions) < 10:
        messages.error(request, 'недостаточно вопросов!')
        return redirect('home')

    request.session ['quiz_category'] = category_id
    request.session ['current_questions'] = [q.id for q in questions]

    request.session['current_question'] = 0
    request.session['score'] = 0
    request.session['start_time'] = random.randint(1000,999)

    return redirect('quiz_question', category_id =category_id)

@login_required
def quiz_question(request, category_id ):
    if not request.session.get('current_questions'):
        return redirect('home')

    current_idx = request.session['current_question']

    questions = request.session['current_questions']

    if current_idx >= len(questions):
        return redirect('quiz_results', category_id=category_id)

    question = Question.objects.get(id=questions[current_idx])
    answers = Answer.objects.filter(question=question).order_by('id')

    category = Category.objects.get(id=category_id)



    context = {
        'category': category,
        'questions': questions,
        'answers': answers,
        'current': current_idx,
        'total': len(questions),
        'time_limit':question.time_limit
    }

    return render(request, 'quizzes/quiz.html', context)

@login_required

def submit_answer(request, category_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        answer_id = data.get('answer-id')
        question_id = data.get('question_id')


    answer = Answer.objects.get(id=answer_id)
    is_correct = answer.is_correct

    if is_correct:
       request.session['score'] += answer.question.points

       request.session['current_question'] =+ 1

    return JsonResponse({
        'correct': is_correct,
        'points': answer.question.points,
        'next_question': request.session['current_question'] <
len(request.session['current_questions'])

        })

    return JsonResponse({ 'error': 'invalid request'}, status=400)


@login_required
def quiz_results(request,category_id):
    if not request.session.get('current_questions'):

        return redirect('home')

    category = Category.objects.get(id=category_id)
    score = request.session.get('score', 0 )
    total_questions = len(request.session['current_questions'])

    attempt = QuizAttempt.objects.create(

        user=request.user,
        category=category,
        score=score,
        total_questions=total_questions

    )
    del request.session['currebt_questions']
    del request.session['current_question']
    del request.session['score']

    context = {
        'attempt': attempt,
        'percentage': round((score / (total_questions * 10)) * 100)
    }
    return render(request,'quizzes/results.html,context')






