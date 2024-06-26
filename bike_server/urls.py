"""
URL configuration for bike_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

version = 'v1'

urlpatterns = [
    path(version + '/', include('user_management.urls')),
    path(version + '/bicycles/', include('bicycle.urls')),
    path(version + '/events/', include('event.urls')),
    path(version + '/feedbacks/', include('feedback.urls')),
    path(version + '/images/', include('resource.urls')),
    path(version + '/using-history/', include('usage.urls')),
    path(version + '/transactions/', include('transaction_location.urls')),
    path(version + '/statistics/', include('system_statistic.urls')),
    path(version + '/reports/', include('report.urls')),
    path(version + '/messengers/', include('messenger.urls')),
    path(version + '/notifications/', include('notification.urls')),
    path(version + '/vnpay/', include('vnpay.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
