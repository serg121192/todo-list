from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

from todo_list import settings


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(null=True, blank=True)
    current_date = models.DateTimeField(default=datetime.now)
    status = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "Tag",
        related_name="tasks",
        blank=True
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tasks",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = [
            "status",
            "-created_at",
        ]

    def __str__(self):
        return f"{self.title}"


class Tag(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="tags",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = [
            "name"
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "user"],
                name="unique_tag_name_for_user",
            )
        ]

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    pass
