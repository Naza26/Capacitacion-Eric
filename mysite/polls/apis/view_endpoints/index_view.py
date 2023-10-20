from mysite.polls.models import Question
from django.views import generic
from django.shortcuts import render


class IndexView(generic.View):

    def get(self, request):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
        context = {"latest_question_list": latest_question_list}
        return render(request, "polls/index.html", context)
