from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError

from account.models import Profile


class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='نام کاربری', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='ایمیل', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='تایید پسورد', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('این کاربر از قبل در سیستم ثبت نام شده است')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('نام کاربری انتخاب شده قبلا در سیستم ثبت شده است')
        return username

    def clean(self):
        cd = super(UserRegistrationForm, self).clean()
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('پسورد ها باید مشابه باشند')


class UserLoginForm(forms.Form):
    username = forms.CharField(label='نام کاربری یا ایمیل',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='پسورد', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data["username"]
        User.objects.filter(username=username).exists()
        if username is None:
            raise ValidationError('این نام کابری در سیستم ثبت نشده لطفا ثبت نام کنید')
        return username


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
