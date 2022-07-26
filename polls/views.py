from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Survey,User
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import random


def index(request):
    '''
    latest_question_list = Question.objects.order_by('-pub_date')[:5]  #filter einbauen um bestimmte Fragen anzuzeigen

    #output = ', '.join([q.question_text for q in latest_question_list] )   现在交给前端

    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list, #deklarierung für html, zu übergebender Context
    }
    return HttpResponse(template.render(context, request))
    '''
    
    all_entries = Survey.objects.all()
    
    showing_survey = all_entries.exclude(showing = 'False') # only show the survey that should be showing, you can hide the old surveys

    context = {
        'surveys': showing_survey,
    }
    return render(request, 'polls/index.html', context)

    # latest_question_list = Question.objects.order_by('-pub_date')[:5]#filter einbauen um bestimmte Umfragen zu zeigen
    # context = {'latest_question_list': latest_question_list}
    # return render(request, 'polls/index.html', context)


def get_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = survey.question_set.all()
    # latest_question_list = questions.order_by('added_to_survey')[:]
    question_list = questions.filter(added_to_survey=True) #only the selected questions can be showed
 
    #question_list = questions.filter(added_to_survey=True).order_by('?')[:4]# get 4 random questions that have been selected from our database 
    context = {
        'question_list': question_list,
        'title': survey.title,
        'count': question_list.count(),
    }
    return render(request, 'polls/questions.html', context)



def submit_vote(request):
    values = request.POST.items() #只可获得单选 .item
    q = User(pub_date=timezone.now())
    for k, v in values:
        if len(k) > 9 and k[:8] == 'question' and k[-2:] != '[]':
            question = get_object_or_404(Question, pk=int(k[9:]))
            try:
                selected_choice = question.choice_set.get(pk=int(v))
            except (KeyError, Choice.DoesNotExist):
                print("leider nicht gefunden")
            else:
                selected_choice.votes += 1
                selected_choice.save()
    return redirect('https://www.wbk.kit.edu/')

        # elif len(k) > 9 and k[:8] == 'question' and k[-2:] == '[]':
        #     list = request.POST.getlist(k) 可获得多选的list
        #     question = get_object_or_404(Question, pk=int(k[9:11]))
        #     for value in list:
        #         try:
        #             selected_choice = question.choice_set.get(pk=int(value))
        #         except (KeyError, Choice.DoesNotExist):
        #             print("leider nicht gefunden")
        #         else:
        #             selected_choice.votes += 1
        #             selected_choice.save()
    #     else:
    #         q.__setattr__(k, v) #获得提交的个人信息
    # q.save()
    # # return HttpResponseRedirect(reverse('polls:index')) ursprünglich
    # return redirect('https://www.wbk.kit.edu/')


    """
    ursprüngliche Version 

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question':question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])#让你可以通过关键字的名字获取提交的数据
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    """