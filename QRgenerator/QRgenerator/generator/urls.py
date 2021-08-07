from django.urls import path
from .views import *

app_name = 'generator'

urlpatterns=[
    path('',loginfun, name='loginpage'),
    path('QRgenerate/',qr_generatefun, name='qr_generatepage'),
    path('UINlink/',uin_linkfun, name='uin_linkpage'),
    path('IMEIgenerate/',imei_generatefun, name='imei_generatepage'),
    path('products/',productfun, name='productpage'),
    path('excel/', export_excelfun, name='export_excelpage'),
    path('logout/',logoutfun, name='logoutpage'),
    path('adminpage/',adminfun, name='adminpage'),
    path('register/',registerfun, name='registerpage'),
    path('staff/',staff_fun, name='staffpage'),    
    path('delete/<int:id>',staff_deletefun, name='staffdeletepage'),
    path('uin/',duplicate_generatefun, name='duplicate_generatepage'),  
]
