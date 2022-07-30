from django.shortcuts import render

from .models import GinTonicEvaluation


def index(request):
    evaluations = GinTonicEvaluation.objects.all()
    return render(request, "matrix/list.html", locals())
