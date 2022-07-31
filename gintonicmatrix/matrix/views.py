from django.shortcuts import render

from .models import Drinker, Gin, GinTonicEvaluation, Tonic


def index(request):
    gins = Gin.objects.all()
    tonics = Tonic.objects.all()
    drinkers = Drinker.objects.all()
    evaluation_rows = []
    for tonic in tonics:
        evaluation_row = []
        for gin in gins:
            gin_tonic = GinTonicEvaluation.objects.filter(gin=gin, tonic=tonic)
            if len(gin_tonic) == 0:
                evaluation_row.append((gin, None))
            else:
                mean = 0.0
                for evaluation in gin_tonic:
                    mean += evaluation.rating / len(gin_tonic)
                evaluation_row.append((gin, mean))
        evaluation_rows.append((tonic, evaluation_row))
    return render(
        request,
        "matrix/matrix.html",
        {"drinkers": drinkers,
         "gins": gins,
         "tonics": tonics,
         "evaluation_rows": evaluation_rows})


def evaluations(request, gin, tonic):
    gin_tonic = GinTonicEvaluation.objects.filter(gin=gin, tonic=tonic)
    return render(
        request, "matrix/evaluations.html", {"evaluations": gin_tonic})
