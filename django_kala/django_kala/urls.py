"""django_kala URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from .views import Home, LicenseView, UserDocumentationView

urlpatterns = [
    url(
        regex=r'^$',
        view=Home.as_view(),
        name='home'
    ),

    url(
        r'^companies/',
        include('companies.urls'),
    ),

    url(
        r'^documents/',
        include('documents.urls'),
    ),

    url(
        r'^accounts/',
        include('accounts.urls'),
    ),

    url(
        r'^projects/',
        include('projects.urls'),
    ),

    url(
        regex=r'^license$',
        view=LicenseView.as_view(),
        name='license',
    ),

    url(
        regex=r'^user_documentation$',
        view=UserDocumentationView.as_view(),
        name='user_documentation',
    ),
]
