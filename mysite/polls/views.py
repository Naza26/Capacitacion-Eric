from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.http import Http404


class IndexView(generic.View):

    def get(self, request):
        latest_question_list = self._latest_questions()

        context = {"latest_question_list": latest_question_list}
        return render(request, "polls/index.html", context)

    def _latest_questions(self):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        return latest_question_list


class DetailView(generic.View):
    def get(self, request, pk):
        try:
            question = self._published_question(pk, timezone.now())
        except Exception:
            raise Http404("Question does not exist")
        return render(request, "polls/detail.html", {"question": question})

    def _published_question(self, pk, published_date):
        question = Question.objects.get(pk=pk, pub_date__lte=published_date)
        return question


class ResultsView(generic.View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, "polls/results.html", {"question": question})


class VoteView(generic.View):

    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            selected_choice.votes += 1
            selected_choice.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
