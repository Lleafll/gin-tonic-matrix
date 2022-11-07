import dataclasses
import itertools
import operator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Drinker, Gin, GinTonicEvaluation, Ingredient, Tonic


def index(request):
    gins = Gin.objects.order_by("name")
    tonics = Tonic.objects.order_by("name")
    drinkers = Drinker.objects.order_by("name")
    ingredients = Ingredient.objects.order_by("name")
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
        tonic_rating = 0
        count = 0
        for row in evaluation_row:
            mean = row[1]
            if mean is not None:
                tonic_rating += mean
                count += 1
        if count > 0:
            tonic_rating /= count
        evaluation_rows.append((tonic_rating, tonic, evaluation_row))
    gin_ratings = []
    for i in range(len(gins)):
        gin_mean = 0
        count = 0
        for row in evaluation_rows:
            gin_tonic_mean = row[2][i][1]
            if gin_tonic_mean is not None:
                gin_mean += gin_tonic_mean
                count += 1
        if count > 0:
            gin_mean /= count
        gin_ratings.append(gin_mean)
    return render(
        request,
        "matrix/matrix.html",
        {"selected_drinker": selected_drinker,
         "selected_ingredient": selected_ingredient,
         "drinkers": drinkers,
         "gins": gins,
         "tonics": tonics,
         "ingredients": ingredients,
         "evaluation_rows": evaluation_rows,
         "gin_ratings": gin_ratings})


def evaluations(request, gin_id, tonic_id):
    gin = get_object_or_404(Gin, pk=gin_id)
    tonic = get_object_or_404(Tonic, pk=tonic_id)
    drinkers = Drinker.objects.all()
    ingredients = Ingredient.objects.all()
    gin_tonic = GinTonicEvaluation.objects.filter(
        gin=gin, tonic=tonic).order_by("-created")
    return render(request, "matrix/evaluations.html", {
        "gin": gin,
        "tonic": tonic,
        "evaluations": gin_tonic,
        "drinkers": drinkers,
        "ingredients": ingredients})


def evaluate(request, gin_id, tonic_id):
    gin = get_object_or_404(Gin, pk=gin_id)
    tonic = get_object_or_404(Tonic, pk=tonic_id)
    try:
        drinker = Drinker.objects.get(pk=request.POST["drinker"])
        ingredient = Ingredient.objects.get(pk=request.POST["ingredient"])
        rating = request.POST["rating"]
    except (ValueError,
            KeyError,
            Drinker.DoesNotExist,
            Ingredient.DoesNotExist):
        drinkers = Drinker.objects.all()
        ingredients = Ingredient.objects.all()
        gin_tonic = GinTonicEvaluation.objects.filter(gin=gin, tonic=tonic)
        return render(request, "matrix/evaluations.html", {
            "gin": gin,
            "tonic": tonic,
            "evaluations": gin_tonic,
            "drinkers": drinkers,
            "ingredients": ingredients,
            "error_message": "Bitte alle Felder ausfüllen"})
    GinTonicEvaluation(
        drinker=drinker,
        gin=gin,
        tonic=tonic,
        ingredient=ingredient,
        rating=rating,
        created=timezone.now()).save()
    return HttpResponseRedirect(
        reverse("matrix:evaluations", args=(gin_id, tonic_id)))


@dataclasses.dataclass
class GinTonicEvaluationCombination:
    name: str
    rating: float
    rating_count: int
    unique_rating_count: int


def _group_func(evaluation):
    return f"{evaluation.gin}-{evaluation.tonic} + {evaluation.ingredient}"


def _generate_combinations(evaluations):
    combinations = []
    for key, evaluation in itertools.groupby(evaluations, _group_func):
        evaluation = list(evaluation)
        combinations.append(GinTonicEvaluationCombination(
            key,
            sum(i.rating for i in evaluation) / len(evaluation),
            len(evaluation),
            len({i.drinker for i in evaluation})))
    return combinations


def ranking(request):
    evaluations = GinTonicEvaluation.objects.order_by(
        "gin", "tonic", "ingredient")
    combinations = _generate_combinations(evaluations)
    combinations.sort(key=operator.attrgetter("rating"), reverse=True)
    return render(request, "matrix/ranking.html", {
        "combinations": combinations})
