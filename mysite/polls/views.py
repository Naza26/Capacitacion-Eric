from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question


class IndexView(generic.View):

    def get(self, request):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        context = {"latest_question_list": latest_question_list}
        return render(request, "polls/index.html", context)


class DetailView(generic.View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
        return render(request, "polls/detail.html", {"question": question})


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

def vote(request, question_id):
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
