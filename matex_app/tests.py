from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CertificateHolder

class CertificateHolderTest(TestCase):

    def test_nhs_number_valid(self):
        # Test a valid NHS number
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.full_clean()  # This will run the clean method
        except ValidationError:
            self.fail("Valid NHS number raised ValidationError")

    def test_nhs_number_too_short(self):
        # Test an NHS number that is too short
        certHolder = CertificateHolder(nhs_number=999999999, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.full_clean()

    def test_nhs_number_too_long(self):
        # Test an NHS number that is too long
        certHolder = CertificateHolder(nhs_number=10000000000, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.full_clean()

    def test_nhs_number_out_of_range(self):
        # Test an NHS number that is out of the valid range
        certHolder = CertificateHolder(nhs_number=99999999999, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.full_clean()

    def test_nhs_number_not_int(self):
        # Test an NHS number that is out of the valid range
        certHolder = CertificateHolder(nhs_number="99999999999", first_name="firstname", last_name="lastname",
                                       email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.full_clean()