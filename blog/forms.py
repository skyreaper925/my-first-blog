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
    class Meta:
        model = Consultation
        fields = ('date', 'theme', 'description', 'spectators', 'duration', 'contact', 'place',)


class SignUp(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('form', 'email', 'password1', 'password2', 'username', 'first_name', 'last_name',)


class CommentForm(forms.Form):
    parent_comment = forms.IntegerField(
        widget=forms.HiddenInput,
        required=False
    )

    comment_area = forms.CharField(
        label="",
        widget=forms.Textarea
    )
