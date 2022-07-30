from django.shortcuts import render

from .models import Gin, GinTonicEvaluation, Tonic


def index(request):
    gins = Gin.objects.all()
    tonics = Tonic.objects.all()
    evaluation_rows = []
    for tonic in tonics:
        evaluation_row = []
        for gin in gins:
            evaluations = GinTonicEvaluation.objects.filter(gin=gin, tonic=tonic)
            if len(evaluations) == 0:
                evaluation_row.append(None)
            else:
                mean = 0.0
                for evaluation in evaluations:
                    mean += evaluation.rating / len(evaluations)
                evaluation_row.append(mean)
        evaluation_rows.append((tonic, evaluation_row))
    return render(request, "matrix/list.html", locals())
