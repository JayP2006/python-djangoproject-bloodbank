from django.urls import path
from  donor import views
urlpatterns = [
   path('dlogin/',views.dlogin,name='dlogin'),
   path('dregistration/',views.dregistration,name='dregistration'),
   path('ddashboard/',views.ddashboard,name='ddashboard'),
    path('dsendrequest/',views.dsendrequest,name="dsendrequest"),
    path('dhistory/',views.dhistory,name="dhistory"),
    path('dlogout/',views.dlogout,name="dlogout"),
    path('dbhistory/',views.dbhistory,name='dbhistory'),
    path('donate_blood/',views.donate_blood,name="donate_blood"),
    path('bloodrequest_view/',views.bloodrequest_view,name='bloodrequest_view'),
]