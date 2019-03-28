"""MIWorkflow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^login/$', auth_views.login, {'template_name': 'CentralMI/LoginForm.html'}, name='login'),
    #url(r'^logout/$', auth_views.logout, {'next_page': 'login'},name='logout'),
    url(r'^admin/', admin.site.urls),
    url(r'^', include('CentralMI.urls')),

    url(r'^CMI/', include('CentralMI.urls')),
    url(r'^CMI/report_builder/', include('report_builder.urls')),
    url(r'^CMI/password_reset/$', auth_views.password_reset, name='admin_password_reset'),

    url(r'^admin/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^CMI/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^CMI/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^CMI/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    #url(r'^$', views.HomeView.as_view(), name='home'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
