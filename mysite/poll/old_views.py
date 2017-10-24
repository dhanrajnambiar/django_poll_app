#lines {5 + (16-19)} OR {4 + (8-14)} serve the same purpose (for the same view, 8-14 is the shortcut for which we have to import the 'shortcut' module containing the render function

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from .models import Question,Choice

def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('poll/index.html')
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))

    latest_question_list = Question.objects.order_by('pub_date')[:5]
    context = {'latest_question_list':latest_question_list}
    return render(request,'poll/index.html',context)

#lines 30-31 are shortcut for lines 24-28 using function get_object_or_404()

def detail(request, question_id):
#    try:
#        question = Question.objects.get(pk = question_id)
#    except Question.DoesNotExist:
#        raise Http404("Question doesn't exist")
#    return render(request,'poll/detail.html', {'question':question})

    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})
