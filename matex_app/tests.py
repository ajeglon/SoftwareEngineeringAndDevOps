from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.urls import reverse

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

    def setUp(self):
        # Create a certificate holder
        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

    def test_certificate_info_save_auto_expiration_date(self):
        # Test that expiration date is calculated correctly on save
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date()
        )
        certificate.save()

        self.assertEqual(
            certificate.certificate_expiration_date,
            certificate.certificate_start_date + timedelta(days=365)
        )

    def test_certificate_info_valid_clean(self):
        # Test that a valid CertificateInfo instance passes validation
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date(),
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        try:
            certificate.full_clean()  # Triggers the certClean method
        except ValidationError:
            self.fail("CertificateInfo.clean() raised ValidationError unexpectedly!")

    def test_certificate_info_missing_start_date(self):
        # Test that missing start date raises ValidationError
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_start_date', cm.exception.message_dict)

    def test_certificate_info_missing_expiration_date(self):
        # Test that missing expiration date raises ValidationError
        certificate = CertificateInfo(
            certificate_holder=self.certificate_holder,
            certificate_start_date=datetime(2023, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_expiration_date', cm.exception.message_dict)

    def test_certificate_info_missing_holder(self):
        # Test that missing certificate holder raises ValidationError
        certificate = CertificateInfo(
            certificate_start_date=datetime(2023, 1, 1).date(),
            certificate_expiration_date=datetime(2024, 1, 1).date()
        )
        with self.assertRaises(ValidationError) as cm:
            certificate.full_clean()

        self.assertIn('certificate_holder', cm.exception.message_dict)

# Tests for user login

class UserLoginTests(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_valid_user_login(self):
        # Simulate a POST request with valid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'testpassword',
        }, follow=True)

        # Check if the user is successfully logged in
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)  # Check session for login
        self.assertContains(response, "Succesfully logged in", html=False)

    def test_invalid_user_login(self):
        # Simulate a POST request with invalid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        }, follow=True)

        # Check that the user is not logged in
        self.assertNotIn('_auth_user_id', self.client.session)  # No login in session

        # Check for the error message in the final response
        self.assertContains(response, "There was an error login, please try again")

    def test_get_request(self):
        # Simulate a GET request
        response = self.client.get(reverse('index'))

        # Check that the page is rendered successfully
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')


# Tests for viewing Certificate Holders
class CertificateHoldersViewTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create some certificate holders
        CertificateHolder.objects.create(nhs_number=1000000001, first_name='John', last_name='Doe',
                                         email='john.doe@example.com', date_of_birth='2000-01-01')
        CertificateHolder.objects.create(nhs_number=1000000002, first_name='Jane', last_name='Smith',
                                         email='jane.smith@example.com', date_of_birth='1995-05-15')

        # URL for the view
        self.url = reverse('certificate-holders')

    def test_authenticated_user(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to the view
        response = self.client.get(self.url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Verify that the template is correct
        self.assertTemplateUsed(response, 'certificate-holders.html')

        # Check that all certificate holders are in the context
        cert_holders = response.context['cert_holders']
        self.assertEqual(cert_holders.count(), 2)
        self.assertQuerysetEqual(
            cert_holders.order_by('nhs_number'),
            CertificateHolder.objects.all().order_by('nhs_number'),
            transform=lambda x: x
        )

    def test_unauthenticated_user(self):
        # Send GET request without logging in
        response = self.client.get(self.url)

        # Check for redirection to the login page
        self.assertRedirects(response, reverse('index'))

        # Verify that the message is present
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))

# Tests for viewing Certificates
class CertificatesViewTest(TestCase):
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a certificate holder
        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        # Create some certificates
        CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2023-01-01',
            certificate_expiration_date='2024-01-01'
        )
        CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2022-01-01',
            certificate_expiration_date='2023-01-01'
        )

        # URL for the view
        self.url = reverse('certificates')

    def test_authenticated_user(self):
        # Log in as the test user
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to the view
        response = self.client.get(self.url)

        # Check response status code
        self.assertEqual(response.status_code, 200)

        # Verify that the template is correct
        self.assertTemplateUsed(response, 'certificates.html')

        # Check that all certificates are in the context
        certs = response.context['certs']
        self.assertEqual(certs.count(), 2)
        self.assertQuerysetEqual(
            certs.order_by('certificate_start_date'),
            CertificateInfo.objects.all().order_by('certificate_start_date'),
            transform=lambda x: x
        )

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('index'))

        # Verify that the message is present
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))