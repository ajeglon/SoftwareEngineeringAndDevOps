from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime, timedelta


# Create your models here.
class CertificateHolder(models.Model):
    nhs_number = models.IntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    date_of_birth = models.DateField()

    def __str__(self):
        return str(self.nhs_number) + " - " + f'{self.first_name} {self.last_name}'


class CertificateInfo(models.Model):
    certificate_holder = models.ForeignKey(CertificateHolder, on_delete=models.CASCADE)
    certificate_number = models.AutoField(primary_key=True)
    certificate_start_date = models.DateField(null=True)
    certificate_expiration_date = models.DateField()

    def __str__(self):
        return str(self.certificate_number) + " - " + f'{self.certificate_holder}'

    def save(self, *args, **kwargs):
        self.certificate_expiration_date = self.certificate_start_date + timedelta(days=365)
        super().save(*args, **kwargs)