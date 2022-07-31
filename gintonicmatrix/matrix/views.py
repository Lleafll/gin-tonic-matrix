from django.shortcuts import render

from .models import Drinker, Gin, GinTonicEvaluation, Ingredient, Tonic


def index(request):
    gins = Gin.objects.all()
    tonics = Tonic.objects.all()
    drinkers = Drinker.objects.all()
    ingredients = Ingredient.objects.all()
    try:
        selected_drinker = Drinker.objects.get(pk=request.POST["drinker"])
    except (KeyError, ValueError, Drinker.DoesNotExist):
        selected_drinker = None
    try:
        selected_ingredient = Ingredient.objects.get(
            pk=request.POST["ingredient"])
    except (KeyError, ValueError, Ingredient.DoesNotExist):
        selected_ingredient = None
    evaluation_rows = []
    for tonic in tonics:
        evaluation_row = []
        for gin in gins:
            lookup = {"gin": gin, "tonic": tonic}
            if selected_drinker is not None:
                lookup["drinker"] = selected_drinker
            if selected_ingredient is not None:
                lookup["ingredient"] = selected_ingredient
            gin_tonic = GinTonicEvaluation.objects.filter(**lookup)
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
        {"selected_drinker": selected_drinker,
         "selected_ingredient": selected_ingredient,
         "drinkers": drinkers,
         "gins": gins,
         "tonics": tonics,
         "ingredients": ingredients,
         "evaluation_rows": evaluation_rows})


def evaluations(request, gin, tonic):
    gin_tonic = GinTonicEvaluation.objects.filter(gin=gin, tonic=tonic)
    return render(
        request, "matrix/evaluations.html", {"evaluations": gin_tonic})
