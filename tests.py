# import unittest
# from django.test import Client
# from django.urls import reverse
# from YourCalc.models import Meal, Ingredient
#
#
# class MealTestCase(unittest.TestCase):
#     def setUp(self):
#         self.client = Client()
#
#         self.ingredient = Ingredient.objects.create(
#             name='Test Ingredient',
#             gramme=100,
#             calories=100,
#             carbohydrates=100,
#             protein=100,
#             fat=100
#         )
#
#         self.meal = Meal.objects.create(
#             name='Test Meal'
#         )
#         self.meal.ingredient.add(self.ingredient)
#         self.meal.save()
#
#     def test_add_meal(self):
#         url = reverse('add-meal')
#         response = self.client.post(url, {'ingredients': [{'ingredient': self.ingredient.id, 'quantity': 2}]})
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(Meal.objects.count(), 2)
#         self.assertEqual(Meal.objects.last().ingredient.count(), 1)
#         self.assertEqual(Meal.objects.last().ingredient.first(), self.ingredient)
#
