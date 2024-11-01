from django.contrib import admin
from . models import CertificateHolder
from . models import CertificateInfo

# Register your models here.
admin.site.register(CertificateHolder),
admin.site.register(CertificateInfo)