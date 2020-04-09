from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Post, Consultation, Comment, Review
from .models import UserModel


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'good_date',)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'text'


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ('date', 'theme', 'description', 'spectators', 'duration', 'contact', 'place', 'hashtag',)


CHOICES = [(1, 'Очно'), (2, 'Заочно')]


class FilterDate(forms.Form):
    dateFrom = forms.DateTimeField(label="Дата от", required=False)
    dateTo = forms.DateTimeField(label="Дата до", required=False)
    search = forms.CharField(label="Поиск", required=False)
    contact = forms.MultipleChoiceField(label="Форма проведения", choices=CHOICES, required=False)
    hashtags = forms.CharField(label="Хештеги", required=False)


class SignUp(UserCreationForm):
    form = forms.CharField(max_length=2, help_text='Введите класс, в котором вы обучаетесь')

    class Meta:
        model = UserModel
        fields = ('form', 'email', 'password1', 'password2', 'username', 'first_name', 'last_name', 'vk',)


class ReviewAddForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
#
