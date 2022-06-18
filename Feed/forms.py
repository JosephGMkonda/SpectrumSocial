from dataclasses import fields
from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    body = forms.CharField(
        label="",
        widget=forms.Textarea(attrs = {
            'rows':'3',
            'placeholder': "Whats your mind...."
        })
    )
    image = forms.ImageField(
        label=""

    )


    class Meta:
        model = Post
        fields = ['body','image']