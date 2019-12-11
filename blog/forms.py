from django import forms

from .models import Post, User, Consultation



class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'password',)

class ConsultationForm(forms.ModelForm):

    class Meta:
        model = Consultation
        fields = ('creation', 'date', 'email', 'theme', 'discription', 'spectators', 'longliness')   