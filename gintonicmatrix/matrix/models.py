from django.db import models


class Drinker(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gin(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tonic(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


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
    rating = models.IntegerField(choices=Rating.choices)
    created = models.DateTimeField("Rated on")

    def __str__(self):
        return f"{self.gin}-{self.tonic}+{self.ingredient} ({self.drinker})"
