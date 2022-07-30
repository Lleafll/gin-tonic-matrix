from django.contrib import admin

from .models import Drinker, Gin, GinTonicEvaluation, Ingredient, Tonic

admin.site.register(Drinker)
admin.site.register(Gin)
admin.site.register(GinTonicEvaluation)
admin.site.register(Ingredient)
admin.site.register(Tonic)
