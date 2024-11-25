from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from .models import Questions,Choice
from django.urls import reverse
from django.db.models import F
from django.views import generic

# Create your views here.

# def index(request):
#     latest_question_list = Questions.objects.order_by("-pub_date")[:5]
#     context = {"latest_question_list": latest_question_list}
#     return render(request, "polls/index.html", context)


# def detail(request, question_id):
#     question= get_object_or_404(Questions, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})


# def results(request, question_id):
#     question = get_object_or_404(Questions, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})





class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Questions.objects.order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Questions  # Specify the model to fetch data from
    template_name = "polls/detail.html"  # Specify the template to render

    # Optionally override `get_context_data` if additional context is needed.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_context'] = "Additional data if required"
        return context


class ResultsView(generic.DetailView):
    model = Questions
    template_name = "polls/results.html"

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def detail(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})



def vote(request, question_id):
    
    question = get_object_or_404(Questions, pk=question_id)
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
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))