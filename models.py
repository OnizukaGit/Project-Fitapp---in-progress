from django.db import models
from django.contrib.auth.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=64)
    gramme = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    calories = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    carbohydrates = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    protein = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    fat = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Składniki"
        verbose_name_plural = "Składniki"

    def __str__(self):
        return self.name


class TimeofDay(models.Model):
    options = (
        ('Śniadanie', 'Śniadanie'),
        ('Obiad', 'Obiad'),
        ('Kolacja', 'Kolacja'),
    )
    name = models.CharField(max_length=64, choices=options)

    class Meta:
        verbose_name = "Pora jedzenia"
        verbose_name_plural = "Pora jedzenia"

    def __str__(self):
        return self.name


class Meal(models.Model):
    name = models.CharField(max_length=64)
    ingredient = models.ManyToManyField(Ingredient)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Posiłek"
        verbose_name_plural = "Posiłek"

    def __str__(self):
        return str(self.name)


class MealTime(models.Model):
    options = (
        ('Poniedziałek','Poniedziałek'),
        ('Wtorek','Wtorek'),
        ('Środa','Środa'),
        ('Czwartek','Czwartek'),
        ('Piątek','Piątek'),
        ('Sobota','Sobota'),
        ('Niedziela','Niedziela'),
    )
    name = models.CharField(max_length=64, choices=options)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    timeofday = models.ForeignKey(TimeofDay, on_delete=models.CASCADE)
    users = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Dzień tygodnia"
        verbose_name_plural = "Dni tygodnia"

    def __str__(self):
        return self.name






