from django.contrib.auth import get_user_model
from django.test import TestCase

from todolist.models import Task, Tag


class TestModels(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test1234!"
        )
        self.client.force_login(self.user)

    def test_task_str(self):
        task = Task.objects.create(
            title="Task 1",
            description="Test description",
            user=self.user,
        )
        self.assertEqual(str(task), task.title)

    def test_tag_str(self):
        tag = Tag.objects.create(
            name="Test tag",
            user=self.user,
        )
        self.assertEqual(str(tag), tag.name)
