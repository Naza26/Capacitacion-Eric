from mysite.polls.models import Question
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


class ResultsView(generic.View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        return render(request, "polls/results.html", {"question": question})
