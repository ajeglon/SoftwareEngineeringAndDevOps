from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CertificateHolder, CertificateInfo


# Tests for Certificate Holders
class CertificateHolderTest(TestCase):

    def test_nhs_number_valid(self):
        # Test a valid NHS number
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.certHolderClean()
        except ValidationError:
            self.fail("Valid NHS number raised ValidationError")

    def test_nhs_number_too_short(self):
        # Test an NHS number that is too short
        certHolder = CertificateHolder(nhs_number=999999999, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_nhs_number_too_long(self):
        # Test an NHS number that is too long
        certHolder = CertificateHolder(nhs_number=10000000000, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_nhs_number_out_of_range(self):
        # Test an NHS number that is out of the valid range
        certHolder = CertificateHolder(nhs_number=99999999999, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_nhs_number_not_int(self):
        # Test an NHS number that is out of the valid range
        certHolder = CertificateHolder(nhs_number="99999999999", first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_nhs_number_empty(self):
        # Test an NHS number that is empty
        certHolder = CertificateHolder(nhs_number="", first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_first_name_valid(self):
        # Test a valid First Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="Anthony", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.certHolderClean()
        except ValidationError:
            self.fail("Valid First Name raised ValidationError")

    def test_first_name_invalid(self):
        # Test an invalid First Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="123456", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_first_name_empty(self):
        # Test an empty First Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_last_name_valid(self):
        # Test a valid Last Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.certHolderClean()
        except ValidationError:
            self.fail("Valid First Name raised ValidationError")

    def test_last_name_invalid(self):
        # Test an invalid Last Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="123456", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_last_name_empty(self):
        # Test an empty Last Name
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="", email="email@email.co.uk", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_email_valid(self):
        # Test a valid email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="testemaill@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.certHolderClean()
        except ValidationError:
            self.fail("Valid email raised ValidationError")

    def test_email_invalid(self):
        # Test an invalid email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="testemaill", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_email_empty(self):
        # Test an empty email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="", date_of_birth="1990-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_date_of_birth_valid(self):
        # Test a valid email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="testemaill@email.co.uk", date_of_birth="1990-01-01")
        try:
            certHolder.certHolderClean()
        except ValidationError:
            self.fail("Valid Date of birth raised ValidationError")

    def test_date_of_birth_future(self):
        # Test an invalid email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="testemaill", date_of_birth="2099-01-01")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_date_of_birth_invalid(self):
        # Test an invalid email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="testemaill", date_of_birth="19990101")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

    def test_date_of_birth_empty(self):
        # Test an empty email
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="")
        with self.assertRaises(ValidationError):
            certHolder.certHolderClean()

# Tests for Certificates
class CertificateInfoTest(TestCase):

    # Test a valid Certificate holder
    def test_certificate_holder_valid(self):
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        certInfo = CertificateInfo(certificate_holder=certHolder, certificate_number="12345", certificate_start_date="2024-11-11",  certificate_expiration_date="2025-11-11")
        try:
            certInfo.certClean()
        except ValidationError:
            self.fail("Valid Certificate Holder raised ValidationError")

    # Test a valid Certificate number
    def test_certificate_number_valid(self):
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        certInfo = CertificateInfo(certificate_holder=certHolder, certificate_number="11",  certificate_start_date="2024-11-11", certificate_expiration_date="2025-11-11")
        try:
            certInfo.certClean()
        except ValidationError:
            self.fail("Valid Certificate Number raised ValidationError")

    # Test a valid Certificate start date
    def test_certificate_start_date_valid(self):
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        certInfo = CertificateInfo(certificate_holder=certHolder, certificate_number="12345", certificate_start_date="2024-06-06", certificate_expiration_date="2025-11-11")
        try:
            certInfo.certClean()
        except ValidationError:
            self.fail("Valid Certificate Start Date raised ValidationError")

    # Test a valid Certificate start date
    def test_certificate_expiration_date_valid(self):
        certHolder = CertificateHolder(nhs_number=1234567890, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
        certInfo = CertificateInfo(certificate_holder=certHolder, certificate_number="12345", certificate_start_date="2024-06-06", certificate_expiration_date="2025-06-06")
        try:
            certInfo.certClean()
        except ValidationError:
            self.fail("Valid Certificate Expiration Date raised ValidationError")