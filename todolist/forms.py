from django import forms
from django.contrib.auth.forms import UserCreationForm

from todolist.models import (
    Task,
    Tag,
    User,
)


class TaskCreateUpdateForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.prefetch_related("tasks"),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput,
        required=False,
    )

    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "deadline",
            "tags",
        ]


class TaskSearchForm(forms.Form):
    title = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by task title",
            }
        )
    )


class TagCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = [
            "name",
        ]


class TagSearchForm(forms.Form):
    name = forms.CharField(
        label="",
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by tag name",
            }
        )
    )


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]
