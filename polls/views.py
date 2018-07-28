from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils import timezone
import code
from .models import Choice, Question, User, Answer


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
	    """
	    Return the last five published questions (not including those set to be
	    published in the future).
	    """
	    return Question.objects.filter(
	        pub_date__lte=timezone.now()
	    ).order_by('-pub_date')[:5]

class UserIndexView(generic.ListView):
    model = User
    template_name = 'polls/userIndex.html'
    context_object_name = 'latest_answer_list'

    def get_context_data(self, **kwargs):
        context = super(UserIndexView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.kwargs['user_id'])
        context['question'] = Question.objects.get(id=self.kwargs['question_id'])
        return context

    def get_queryset(self):
        """
        Return the last five published answers for this user (not including those set to be
        published in the future).
        """
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        sliced_queryset = Answer.objects.filter(
            user=user
        ).order_by('-answer_date')[:5]
        answers = Answer.objects.filter(id__in=sliced_queryset)
        #code.interact(local=dict(globals(), **locals()))
        return Answer.objects.filter(id__in=sliced_queryset)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    # additional parameters
    user_id = None

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['user'] = User.objects.get(id=self.kwargs['user_id'])
        return context
    
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if (not request.POST['username']):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a username.",
        })
    else:
        try:
            user = User.objects.get(username=request.POST['username'])
        except (KeyError, User.DoesNotExist):
            user = User.objects.create(username=request.POST['username'])
            user.save()
        try:
            selected_choice = question.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice.",
            })
        else:
            selected_choice.votes += 1
            selected_choice.save()
            answer = Answer.objects.create(answer_date=timezone.now(), user=user, choice=selected_choice)
            answer.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(question.id, user.id)))