from django.urls import path
from  patient import views
urlpatterns = [
    path('',views.home,name="home"),
    path('plogin/',views.plogin,name="plogin"),
    path('registration/',views.registration,name="registration"),
    path('pdashboard/',views.pdashboard,name="pdashboard"),
    path('psendrequest/',views.psendrequest,name="psendrequest"),
    path('phistory/',views.phistory,name="phisotry"),
    path('plogout/',views.plogout,name="plogout"),
]