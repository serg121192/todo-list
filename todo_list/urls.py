"""
URL configuration for todo_list project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from todo_list import settings
from todolist.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("todolist/", include("todolist.urls")),
    path("", index, name="index"),
    path("__debug__/", include(debug_toolbar.urls)),
    path("accounts/", include("django.contrib.auth.urls")),
    path("favicon.ico", RedirectView.as_view(url="/static/favicon.ico")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
