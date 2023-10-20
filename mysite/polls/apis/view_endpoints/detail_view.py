from mysite.polls.models import Question
from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.utils import timezone


class DetailView(generic.View):
    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk, pub_date__lte=timezone.now())
        return render(request, "polls/detail.html", {"question": question})