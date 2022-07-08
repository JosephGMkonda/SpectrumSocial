from django import forms
from PostFeed.models import Posts

class newPost(forms.ModelForm):
    picture = forms.ImageField(required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class':'input is-medium'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'input is-medium'}), required=True)

    class Meta:
        model = Posts
        fields = ('picture','caption','tags')