from django import forms

from home.models import Post, Comment


class UpdateAndCreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.Textarea(attrs={'class': 'form-control', })
        }
        labels = {
            'body': 'متن کامنت'
        }


class CommentReplaysForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)

        widgets = {
            'body': forms.TextInput(attrs={'class': 'form-control', })
        }
        labels = {
            'body': 'متن کامنت'
        }


class SearchForm(forms.Form):
    search = forms.CharField(label='جستجو کنید', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اینجا سرچ کن'}))
