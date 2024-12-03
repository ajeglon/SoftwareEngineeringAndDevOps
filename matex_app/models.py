from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.db import models
from datetime import datetime, timedelta


# Create your models here.
class CertificateHolder(models.Model):
    nhs_number = models.BigIntegerField(
        validators=[
            MinValueValidator(1000000000),
            MaxValueValidator(9999999999)
        ],
        unique=True)
    first_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+$',
                message="First name can only contain letters."
            )
        ],
        help_text="Enter the first name (letters only)."
    )
    last_name = models.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]+$',
                message="Last name can only contain letters."
            )
        ],
        help_text="Enter the last name (letters only)."
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        unique=True,
        help_text="Enter a valid email address."
    )
    date_of_birth = models.DateField(
        help_text="Enter the date of birth (YYYY-MM-DD)."
    )

    def __str__(self):
        return str(self.nhs_number) + " - " + f'{self.first_name} {self.last_name}'

    def clean(self):
        # Custom validation for the nhs_number
        if not (1000000000 <= int(self.nhs_number) <= 9999999999):
            raise ValidationError({'nhs_number': 'NHS number must be a 10-digit number between 1000000000 and 9999999999.'})


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