from django.urls import path

from todolist.views import (
    TaskListView,
    TagListView,
    TaskCreateView,
    TaskUpdateView,
    TaskDeleteView,
    TagCreateView,
    TagUpdateView,
    TagDeleteView,
    TaskToggleStatusView, UserCreateView,
)

urlpatterns = [
    path(
        "tasks/",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/update/<int:pk>/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/toggle_status/<int:pk>/",
        TaskToggleStatusView.as_view(),
        name="task-toggle-status"
    ),
    path(
        "tasks/delete/<int:pk>/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "tags/",
        TagListView.as_view(),
        name="tag-list"
    ),
    path(
        "tags/create/",
        TagCreateView.as_view(),
        name="tag-create"
    ),
    path(
        "tags/update/<int:pk>/",
        TagUpdateView.as_view(),
        name="tag-update"
    ),
    path(
        "tags/delete/<int:pk>/",
        TagDeleteView.as_view(),
        name="tag-delete"
    ),
    path(
        "user_create/",
        UserCreateView.as_view(),
        name="user-create"
    ),
]

app_name = "todolist"
