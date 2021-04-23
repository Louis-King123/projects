"""asp_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from asp_test import modify_time
from asp_test.utils import TimeTools

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^$', modify_time.init_task),
    url(r'^test_add_task/$', modify_time.test_add_task),
    # url(r'^test_modify_task/$', modify_time.test_modify_task),
    # url(r'^all_task/$', modify_time.all_task),
    # url(r'^get_all_job/$', modify_time.get_all_job),
    # url(r'^remove_all_jobs/$', modify_time.remove_all),
]
