"""
URL configuration for bio_showcase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path, include
import django.conf.urls.static
import django.conf  # noqa: F401
from bio_polls.admin import admin_site
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('polls/', include('bio_polls.urls')),
    path('primer/', include('bio_primer.urls')),
    path('admin/', admin_site.urls),
    path('', include('bio_polls.urls')),
] + debug_toolbar_urls()
