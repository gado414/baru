from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Question
from .models import Choice, Question
# Create your views here.
class IndexView(generic.ListView):
    template_name = 'akun/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'akun/index.html', context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'akun/detail.html'
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'akun/detail.html', {'question': question})

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'akun/results.html'
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, '/results.html', {'question': question})
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'akun/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('akun:results', args=(question.id,)))