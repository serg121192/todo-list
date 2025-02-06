from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from todolist.models import Task, Tag

TASKS_URL = reverse("todolist:task-list")
TAGS_URL = reverse("todolist:tag-list")

TASKS_LIST = [
    {
        "title": "Task 1",
        "description": "Task 1",
    },
    {
        "title": "Task 2",
        "description": "Task 2",
    },
    {
        "title": "Task 3",
        "description": "Task 3",
    },
    {
        "title": "Task 4",
        "description": "Task 4",
    },
    {
        "title": "Task 5",
        "description": "Task 5",
    },
]

TAGS_LIST = [
    {
        "name": "Tag name 1",
    },
    {
        "name": "Tag name 2",
    },
    {
        "name": "Tag name 3",
    },
    {
        "name": "Tag name 4",
    },
    {
        "name": "Tag name 5",
    }
]


class PublicTestTasks(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_list_for_unlogged_user(self):
        response = self.client.get(TASKS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTasks(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_task_list_for_logged_user(self):
        for task in TASKS_LIST:
            Task.objects.create(**task, user=self.user)

        response = self.client.get(TASKS_URL)
        self.assertEqual(response.status_code, 200)
        tasks = Task.objects.filter(user=self.user)
        search_task_title = "2"
        filtered_tasks = Task.objects.filter(
            title__icontains=search_task_title
        )
        filtered_response = self.client.get(
            TASKS_URL,
            {
                "title": search_task_title,
            }
        )
        self.assertEqual(list(tasks), list(response.context["tasks"]))
        self.assertTemplateUsed(filtered_response, "todolist/task_list.html")
        self.assertEqual(
            list(filtered_tasks),
            list(filtered_response.context["tasks"])
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["title"],
            search_task_title,
        )


class PublicTestTags(TestCase):
    def setUp(self):
        self.client = Client()

    def test_task_list_for_unlogged_user(self):
        response = self.client.get(TAGS_URL)
        self.assertNotEqual(response.status_code, 200)


class PrivateTestTags(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test1234!",
        )
        self.client.force_login(self.user)

    def test_task_list_for_logged_user(self):
        for tag in TAGS_LIST:
            Tag.objects.create(
                **tag,
                user=self.user
            )

        response = self.client.get(TAGS_URL)
        self.assertEqual(response.status_code, 200)
        tags = Tag.objects.filter(user=self.user)
        search_tag_name = "4"
        filtered_tags = Tag.objects.filter(
            name__icontains=search_tag_name
        )
        filtered_response = self.client.get(
            TAGS_URL,
            {
                "name": search_tag_name,
            }
        )
        self.assertEqual(list(tags), list(response.context["tags"]))
        self.assertTemplateUsed(filtered_response, "todolist/tag_list.html")
        self.assertEqual(
            list(filtered_tags),
            list(filtered_response.context["tags"])
        )
        self.assertEqual(
            filtered_response.context["search_form"].initial["name"],
            search_tag_name,
        )
