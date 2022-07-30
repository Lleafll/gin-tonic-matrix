from django.db import models


class Drinker(models.Model):
    name = models.CharField(50)


class Gin(models.Model):
    name = models.CharField(50)


class Tonic(models.Model):
    name = models.CharField(50)


class Ingredient(models.Model):
    name = models.CharField(50)


class GinTonicEvaluation(models.Model):
    class Rating(models.IntegerChoices):
        VeryGood = 4
        Good = 3
        Average = 2
        Bad = 1

    drinker = models.ForeignKey(Drinker, on_delete=models.PROTECT)
    gin = models.ForeignKey(Gin, on_delete=models.PROTECT)
    tonic = models.ForeignKey(Tonic, on_delete=models.PROTECT)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    rating = models.IntegerField(choices=Rating)
    created = models.DateTimeField("Rated on")
