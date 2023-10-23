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
            question = self._published_question(pk)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, "polls/detail.html", {"question": question})

    def _published_question(self, pk):
        time_of_reading = timezone.now()
        question = Question.objects.get(pk=pk, pub_date__lte=time_of_reading)
        return question


class ResultsView(generic.View):

    def get(self, request, pk):
        try:
            question = self._published_question(pk)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, "polls/results.html", {"question": question})

    def _published_question(self, pk):
        question = Question.objects.get(pk=pk)
        return question


class VoteView(generic.View):

    def post(self, request, question_id):
        try:
            question = self._published_question(question_id)
        except Question.DoesNotExist:
            raise Http404("Question does not exist")
        choice_does_not_exist = False
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
            selected_choice.votes += 1
            selected_choice.save()
        except (KeyError, Choice.DoesNotExist):
            choice_does_not_exist = True

        if choice_does_not_exist:
            return render(
                request,
                "polls/detail.html",
                {
                    "question": question,
                    "error_message": "You didn't select a choice.",
                },
            )
        else:
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



    def _published_question(self, pk):
        question = Question.objects.get(pk=pk)
        return question
