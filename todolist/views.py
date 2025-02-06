from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic

from todolist.forms import (
    TaskCreateUpdateForm,
    TagCreateUpdateForm,
    UserCreateForm, TaskSearchForm, TagSearchForm,
)
from todolist.models import Task, Tag


def index(request: HttpRequest) -> HttpResponse:
    if not request.user.is_authenticated:
        return render(
            request,
            "todolist/index.html",
            {
                "number_of_tasks": 0,
                "number_of_tags": 0,
                "number_of_visits": 0}
        )

    user = request.user
    number_of_user_tasks = Task.objects.filter(user=user).count()
    number_of_user_tags = Tag.objects.filter(user=user).count()

    number_of_tasks = number_of_user_tasks
    number_of_tags = number_of_user_tags

    number_of_visits = request.session.get("number_of_visits", 1)
    request.session["number_of_visits"] = number_of_visits + 1

    context = {
        "number_of_tasks": number_of_tasks,
        "number_of_tags": number_of_tags,
        "number_of_visits": number_of_visits,
    }

    return render(
        request,
        "todolist/index.html",
        context=context,
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "todolist/task_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title")
        context["search_form"] = TaskSearchForm(
            initial={"title": title}
        )

        return context

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user)
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(
                title__icontains=form.cleaned_data["title"],
            )

        return queryset


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TaskCreateUpdateForm
    context_object_name = "task"
    template_name = "todolist/task_create_update.html"
    success_url = reverse_lazy("todolist:task-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskCreateUpdateForm
    context_object_name = "task"
    template_name = "todolist/task_create_update.html"
    success_url = reverse_lazy("todolist:task-list")

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        form.instance.tags.set(form.cleaned_data["tags"])

        return super().form_valid(form)


class TaskToggleStatusView(LoginRequiredMixin, generic.View):
    def post(self, request, pk):
        task = Task.objects.get(pk=pk, user=self.request.user)
        task.status = not task.status
        task.save()

        return redirect("todolist:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "todolist/task_delete.html"
    success_url = reverse_lazy("todolist:task-list")


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tags"
    template_name = "todolist/tag_list.html"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name")
        context["search_form"] = TagSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = Tag.objects.filter(user=self.request.user)
        form = TagSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = TagCreateUpdateForm
    context_object_name = "tag"
    template_name = "todolist/tag_create_update.html"
    success_url = reverse_lazy("todolist:tag-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    form_class = TagCreateUpdateForm
    context_object_name = "tag"
    template_name = "todolist/tag_create_update.html"
    success_url = reverse_lazy("todolist:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    context_object_name = "tag"
    template_name = "todolist/tag_delete.html"
    success_url = reverse_lazy("todolist:tag-list")


class UserCreateView(generic.CreateView):
    form_class = UserCreateForm
    context_object_name = "user"
    template_name = "todolist/user_create.html"
    success_url = reverse_lazy("login")
