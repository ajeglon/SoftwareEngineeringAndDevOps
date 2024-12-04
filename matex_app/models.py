from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, EmailValidator
from django.db import models
from datetime import datetime, timedelta, date
import re


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
        unique=True
    )
    date_of_birth = models.DateField(
        help_text="Enter the date of birth (YYYY-MM-DD)."
    )

    def __str__(self):
        return str(self.nhs_number) + " - " + f'{self.first_name} {self.last_name}'

    def certHolderClean(self):
        if not self.nhs_number:
            raise ValidationError("NHS number cannot be empty.")
        if not (1000000000 <= int(self.nhs_number) <= 9999999999):
            raise ValidationError({'nhs_number': 'NHS number must be a 10-digit number between 1000000000 and 9999999999.'})
        if not self.first_name:
            raise ValidationError("First name cannot be empty.")
        if not re.fullmatch(r'[A-Za-z]+', self.first_name):
            raise ValidationError("First name can only contain letters.")
        if not self.last_name:
            raise ValidationError("Last name cannot be empty.")
        if not re.fullmatch(r'[A-Za-z]+', self.last_name):
            raise ValidationError("Last name can only contain letters.")
        if not self.email:
            raise ValidationError("Email cannot be empty.")
        validator = EmailValidator(message="Invalid email address format.")
        try:
            validator(self.email)  # Check if the email is valid
        except ValidationError:
            raise ValidationError({"email": "The email field must contain a valid email address."})
        if not self.date_of_birth:
            raise ValidationError("Date of Birth cannot be empty.")
        if isinstance(self.date_of_birth, str):
            try:
                self.date_of_birth = datetime.strptime(self.date_of_birth, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError(
                    {"date_of_birth": "The date of birth must be a valid date in the format YYYY-MM-DD."})
        if self.date_of_birth:
            if not isinstance(self.date_of_birth, date):
                raise ValidationError({"date_of_birth": "The date of birth must be a valid date."})



class CertificateInfo(models.Model):
    certificate_holder = models.ForeignKey(CertificateHolder, on_delete=models.CASCADE)
    certificate_number = models.AutoField(primary_key=True)
    certificate_start_date = models.DateField(null=True)
    certificate_expiration_date = models.DateField()

    def __str__(self):
        return str(self.certificate_number) + " - " + f'{self.certificate_holder}'

    def save(self, *args, **kwargs):
        if isinstance(self.certificate_start_date, str):
            self.certificate_start_date = datetime.strptime(self.certificate_start_date, "%Y-%m-%d").date()
        if self.certificate_start_date:
            self.certificate_expiration_date = self.certificate_start_date + timedelta(days=365)

        super().save(*args, **kwargs)

    def certClean(self):
        if not self.certificate_holder:
            raise ValidationError("Certificate holder cannot be empty.")
        if not self.certificate_number:
            raise ValidationError("Certificate number cannot be empty.")
        if not self.certificate_start_date:
            raise ValidationError("Certificate start date cannot be empty.")
        if not self.certificate_start_date:
            raise ValidationError({"certificate_start_date": "Certificate start date cannot be empty."})
        if self.certificate_start_date and self.certificate_expiration_date:
            if self.certificate_expiration_date <= self.certificate_start_date:
                raise ValidationError({
                    "certificate_expiration_date": "Expiration date must be after the start date."
                })
        if not self.certificate_expiration_date:
            raise ValidationError("Certificate expiration date cannot be empty.")