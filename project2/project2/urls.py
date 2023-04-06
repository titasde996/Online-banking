"""project2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
from registration.views import *
from registration.extra_views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view,name="home"),
    path('reg/',reg_view,name="reg"),
    path('login/',login_view,name="login"),
    path('profile/<str:my_id>/',profile_view,name="profile"),
    path('captcha/', include('captcha.urls')),
    path('withdraw/<str:my_acc>/',withdraw_view,name="withdraw"),
    path('deposit/',deposit_view,name="deposit"),
    path('delete/<str:my_acc>/',delete_view,name="delete"),
    path('create_account/',create_account_view,name="create_account"),
    path('view_account/',view_account_view,name="view_account"),
    path('update_profile/',update_profile_view,name="update_profile"),
    path('transaction/<str:my_acc>/',transaction_view,name="transaction"),
    path('api-auth/', include('rest_framework.urls')),
    path('verify/',verify_view,name="verify"),
    path('verification/',verification_view,name="verification"),
    path('base/',base_view,name="base"),
    path('contact/',contact_view,name="contact"),
    path('about/',about_view,name="about"),
    path('scheme/',scheme_view,name="scheme"),
    path('base2/',base2_view,name="base2"),
    path('fp1/',fp1_view,name="fp1"),
    path('fp2/',fp2_view,name="fp2"),
    path('update-password/',update_password_view,name="update-password"),
    path('ask_sq/',ask_sq_view,name="ask_sq"),
    path('receipt/<str:my_dic>/',receipt_view,name="receipt")
]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
