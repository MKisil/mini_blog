from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django import forms
from django.core import validators

from blog.models import Comment, Author, Blog


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Ім\'я', validators=[validators.MaxLengthValidator(30)])
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повтор пароля')
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'captcha')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class AddCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = '__all__'


class EditCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class CreateAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = '__all__'
        exclude = ('slug',)


class CreateArticleForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ('draft', 'author', 'slug')


