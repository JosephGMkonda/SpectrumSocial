from socket import fromshare
from django import forms
from Comment.models import Comment

class CommentForms(forms.ModelForm):
    body = forms.CharField( 
        label="",
        widget=forms.Textarea

        (attrs=
        {
            'class':'input is-medium',
            'rows':'2',
            'placeholder':'write your comment'
        
        }),
        required=True)

    class Meta:
        model = Comment
        fields = ('body',)