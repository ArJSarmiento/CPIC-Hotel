"""project4 URL Configuration

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
from django.urls import include, path
from django.conf.urls import handler400, handler403, handler404, handler500
from hotelSystem.sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap

handler400 = 'hotelSystem.views.handler400'
handler403 = 'hotelSystem.views.handler403'
handler404 = 'hotelSystem.views.handler404'
handler500 = 'hotelSystem.views.handler500'

sitemaps = {
    'static': StaticViewSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hotelSystem.urls")),
    path("sitemap.xml", sitemap, {"sitemaps":sitemaps}),
    path("", include('pwa.urls')),
]
