from django import forms
from .models import Ingredient, MealTime, Meal
from django.contrib.auth import get_user_model, authenticate
from django.core.validators import ValidationError

User = get_user_model()


class Ingredientsform(forms.ModelForm):
    class Meta:
        model = Ingredient
        exclude = ()


class Mealform(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ('quantity', 'ingredient',)


class Dayform(forms.ModelForm):
    class Meta:
        model = MealTime
        exclude = ('users',)


class Registerform(forms.ModelForm):
    pass1 = forms.CharField(label="Hasło", widget=forms.PasswordInput)
    pass2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'username',
            'email',
        )
        help_texts = {
            'username': 'Twój login'
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError('Podany login już istnieje w bazie')
        return username

    def clean(self):
        cd = super().clean()
        pass1 = cd.get('pass1')
        pass2 = cd.get('pass2')
        if len(pass1) < 4:
            raise ValidationError("Hasło musi miec więcej niż 4 znaki")
        if pass2 != pass1:
            raise ValidationError("Hasło się nie zgadzają")


class Loginform(forms.Form):
    username = forms.CharField(label="Nazwa użytkownika")
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            raise ValidationError("Złe hasło lub login")
