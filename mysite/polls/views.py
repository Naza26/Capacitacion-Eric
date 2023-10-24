from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render
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


class XXX:
    def __init__(self, error, question):
        self.error = error
        self.question = question


class VoteView(generic.View):

    def post(self, request, question_id):
        choice_id = request.POST["choice"]

        an_error_occurred, question = self._add_vote_to_choice(question_id, choice_id)
        result = XXX(an_error_occurred, question)

        if result.error == "Question does not exist":
            raise Http404("Question does not exist")
        if an_error_occurred == "Choice does not exist.":
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

    def _add_vote_to_choice(self, question_id, choice_id):
        error = None
        try:
            question = self._published_question(question_id)
        except Question.DoesNotExist:
            error = "Question does not exist"
            return error, None
        try:
            selected_choice = self._selected_choice(choice_id, question)
            selected_choice.votes += 1
            selected_choice.save()
        except (KeyError, Choice.DoesNotExist):
            error = "Choice does not exist."
        return error, question

    def _selected_choice(self, choice_id, question):
        selected_choice = question.choice_set.get(pk=choice_id)
        return selected_choice

    def _published_question(self, pk):
        question = Question.objects.get(pk=pk)
        return question
