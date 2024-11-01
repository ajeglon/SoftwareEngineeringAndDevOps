from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('certificate-holders', views.certificateholders, name='certificate-holders'),
    path('certificates', views.certificates, name='certificates'),
    path('add-holder', views.addholder, name='add-holder'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('holder-info/<int:pk>/', views.holder_info, name='holder-info'),
    path('delete-cert-holder/<int:pk>/', views.delete_cert_holder, name='delete-holder-info'),
    path('update-cert-holder/<int:pk>/', views.update_cert_holder, name='update-holder-info'),
    path('certificate-info/<int:pk>/', views.certificate_info, name='certificate-info'),
    path('add-certificate', views.add_certificate, name='add-certificate'),
    path('delete-certificate/<int:pk>/', views.delete_certificate, name='delete-certificate'),
    path('update-certificate/<int:pk>/', views.update_certificate, name='update-certificate')
]
