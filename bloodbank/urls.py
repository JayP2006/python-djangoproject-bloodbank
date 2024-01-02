"""
URL configuration for bloodbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from blood import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('patient/',include('patient.urls')),
    path('',include('donor.urls')),
    path('',include('patient.urls')),
    path('admin_login/',views.admin_login,name='admin_login'),
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),
    path('updatep/<int:id>',views.updatep,name='updatep'),
    path('updated/<int:id>',views.updated,name='updated'),
    path('deletep/<int:id>',views.deletep,name='deletep'),
    path('deleted/<int:id>',views.deleted,name='deleted'),
    path('bloodstock/',views.bloodstock,name='bloodstock'),
    path('p_admin/',views.p_admin,name='p_admin'),
    path('d_admin/',views.d_admin,name='d_admin'),
    path('donations/',views.donations,name='donations'),
    path('blood_request/',views.blood_request,name='blood_request'),
    path('approvep/<int:id>',views.approvep,name='approvep'),
    path('approved/<int:id>',views.approved,name='approved'),
    path('rejectp/<int:id>',views.rejectp,name='rejectp'),
    path('rejectd/<int:id>',views.rejectd,name='rejectd'),
]
