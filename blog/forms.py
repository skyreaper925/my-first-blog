from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Consultation
from .models import Post
from .models import UserModel


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)


class ConsultationForm(forms.ModelForm):
    # duration = forms.TimeField(widget=forms.TimeInput(format='%H:%M'))
    # period = forms.ChoiceField(choices=[(1,"Лекция"), (2, "Курс")])
    class Meta:
        model = Consultation
        fields = ('period', 'date', 'theme', 'description', 'contact', 'spectators', 'duration',)


class SignUp(UserCreationForm):
    form = forms.CharField(max_length=2, help_text='Введите класс, в котором вы обучаетесь')

    class Meta:
        model = UserModel
        fields = ('form', 'email', 'password1', 'password2', 'username', 'first_name', 'last_name',)
