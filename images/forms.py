from django import forms
from .models import Image, Comment

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image', 'title')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
