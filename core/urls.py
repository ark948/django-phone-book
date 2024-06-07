"""
URL configuration for core project.

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
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls), # admin
    path('dj-auth/', include('django.contrib.auth.urls')), # web
    path("api-auth/", include("rest_framework.urls")), # api
    path("dj-rest-auth/", include("dj_rest_auth.urls")), # api
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")), # api
    path("api/schema/", SpectacularAPIView.as_view(), name='schema'), # api
    path("api/schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"), # api
    path("api/schema/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"), # api
    # authentication routes (login, logout, signup)
    path("accounts/", include("accounts.urls")), # web view
    # path("accounts/", include("django.contrib.auth.urls")), # web view
    path("api/", include("apis.urls")),
    path("contacts/", include("contacts.urls")),
    path("", include("pages.urls")),
]
