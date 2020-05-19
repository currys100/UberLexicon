"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from words import views


# paths are the django 2.0 way to do things. urls are the less convenient way.
urlpatterns = [
    url(r'^new$', views.new_word, name='new_word'),
    url(r'^(\d+)/$', views.view_words, name='view_word'),
    url(r'^(\d+)/add_item$', views.add_item, name='add_item')
]