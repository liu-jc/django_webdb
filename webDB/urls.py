"""webDB URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from webDB.view import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/$',index),
    url(r'^$',index),
    url(r'^people/$',people),
    url(r'^hello/$',hello),
    url(r'^add_people/$',add_people),
    url(r'^search-post/$',search_post),
    url(r'^team/$',team),
    url(r'^add_team/$',add_team),
    url(r'^team_member/$',team_member),
    url(r'^project/$',project),
    url(r'^add_project/$',add_project),
    url(r'^project_detail/$',project_detail),
    url(r'^event/$',event),
    url(r'^add_event/$',add_event),
    url(r'^event_detail/$',event_detail),
    url(r'^task/$',task),
    url(r'^add_task/$',add_task),
    url(r'^task_detail/$',task_detail),
    url(r'^people_delete/$',people_delete),
]
