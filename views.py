from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, FormView, RedirectView, DetailView,ListView
from YourCalc.models import MealTime, Ingredient, Meal
from .forms import Ingredientsform, Mealform, Dayform, Registerform, Loginform
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model, login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin as Mixin
from django.shortcuts import redirect
User = get_user_model()
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator



class Register(CreateView):
    model = User
    template_name = "YourCalc/Register.html"
    form_class = Registerform
    success_url = reverse_lazy("monday")
    permission_required = 'auth.add.user'

    def form_valid(self, form):
        response = super().form_valid(form)
        cd = form.cleaned_data
        self.object.set_password(cd['pass1'])
        self.object.save()
        login(self.request, self.object)
        print(self.object)
        return response


class Login(FormView):
    template_name = "YourCalc/Login.html"
    success_url = reverse_lazy("monday")
    form_class = Loginform

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return response


class Logout(RedirectView):
    url = reverse_lazy("monday")

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(Logout, self).get(request, *args, **kwargs)


class Addingredients(Mixin, CreateView):
    login_url = 'login'
    template_name = "YourCalc/Add-ingredients.html"
    form_class = Ingredientsform
    success_url = reverse_lazy("monday")


class Addmeal(CreateView):
    model = Meal
    form_class = Mealform
    template_name = 'YourCalc/Add-meal.html'
    success_url = reverse_lazy('add-meal')

    def form_valid(self, form):
        meal = form.save(commit=False)
        ingredients = self.request.POST.getlist('ingredient')
        quantities = self.request.POST.getlist('quantity')

        for ingredient, quantity in zip(ingredients, quantities):
            ingredient = Ingredient.objects.get(id=ingredient)
            meal.ingredient.add(ingredient)
            ingredient.gramme *= int(quantity)
            ingredient.calories *= int(quantity)
            ingredient.carbohydrates *= int(quantity)
            ingredient.protein *= int(quantity)
            ingredient.fat *= int(quantity)

        meal.save()
        return super().form_valid(form)


class Addmealtoday(Mixin, CreateView):
    login_url = reverse_lazy("login")
    template_name = "YourCalc/Add-a-meal-to-the-day.html"
    form_class = Dayform
    success_url = reverse_lazy('monday')

    def form_valid(self, form):
        isinstance = form.save(commit=False)
        isinstance.users = self.request.user
        isinstance.save()
        return super().form_valid(form)


class Update(Mixin, UpdateView):
    template_name = "YourCalc/Add-ingredients.html"
    form_class = Ingredientsform
    success_url = reverse_lazy("first")

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Ingredient, pk=pk)


class Viewingredients(View):
    def get(self, request):
        ingredients = Ingredient.objects.all()
        ingredients_list = [model_to_dict(ingredient) for ingredient in ingredients]
        return JsonResponse({"ingredients": ingredients_list})


class Viewmeals(View):
    def get(self,request, pk):
        meals_id = MealTime.objects.get(meal__ingredients=pk)
        return render(request, "YourCalc/meals.html",context={"meals_id":meals_id})


class Monday(View):

    def get(self,request):
        brekfast = MealTime.objects.filter(name="Poniedziałek").filter(timeofday__name="Śniadanie")

        lunch = MealTime.objects.filter(name="Poniedziałek").filter(timeofday__name="Obiad")
        dinner = MealTime.objects.filter(name="Poniedziałek").filter(timeofday__name="Kolacja")
        return render(request, "YourCalc/Monday.html", context={"brekfast":brekfast,"lunch":lunch,"dinner":dinner})


class Tuesday(View):

    def get(self, request):
        tuesday = MealTime.objects.filter(name="Wtorek")
        return render(request, "YourCalc/Tuesday.html", context={"tuesday":tuesday})


class Wednesday(View):

    def get(self,request):
        wednesday = MealTime.objects.filter(name="Środa")
        return render(request, "YourCalc/Wednesday.html", context={"wednesday":wednesday})


class Thursday(View):

    def get(self,request):
        thursday = MealTime.objects.filter(name="Czwartek")
        return render(request, "YourCalc/Thursday.html", context={"thursday":thursday})


class Firday(View):

    def get(self,request):
        friday = MealTime.objects.filter(name="Piątek")
        return render(request, "YourCalc/Friday.html", context={"friday":friday})


class Saturday(View):

    def get(self,request):
        saturday = MealTime.objects.filter(name="Sobota")
        return render(request, "YourCalc/Saturday.html", context={"saturday":saturday})


class Sunday(View):

    def get(self,request):
        sunday = MealTime.objects.filter(name="Niedziela")
        return render(request, "YourCalc/Sunday.html", context={"sunday": sunday})




