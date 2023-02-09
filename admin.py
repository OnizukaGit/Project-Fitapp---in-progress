from django.contrib import admin
from YourCalc.models import MealTime, Ingredient, TimeofDay, Meal

admin.site.register(MealTime)
admin.site.register(Ingredient)
admin.site.register(TimeofDay)
admin.site.register(Meal)

