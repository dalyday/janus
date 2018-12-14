"""janus_crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from stark.service import v1
from crm import views

urlpatterns = [
    url(r'^login/$', views.login),
    url(r'^index/$', views.index),
    url(r'^reset/permission/$', views.reset_permission),
    url(r'^stark/', v1.site.urls),
    url(r'^custom1/$', views.custom1),
    url(r'^custom2/$', views.custom2),
    url(r'^custom3/$', views.custom3),
    url(r'^custom4/$', views.custom4),
]
