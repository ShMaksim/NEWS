from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category

class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=20)
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Post
        fields = ['author', 'title', 'text', 'categories']

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if title == text:
            raise ValidationError(
                "Название не может повторяться в тексте"
            )
        return cleaned_data
