import pytest
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.urls import reverse

from .models import CertificateHolder, CertificateInfo


# Tests for Certificate Holders
class CertificateHolderTests(TestCase):

    def test_nhs_number_valid(self):
        # Test a valid NHS number
        certHolder = CertificateHolder(nhs_number=, first_name="firstname", last_name="lastname", email="email@email.co.uk", date_of_birth="1990-01-01")
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
class CertificateInfoTests(TestCase):

    def setUp(self):
        # Create cert holder
        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

    def test_certificate_info_save_auto_expiration_date(self):
        # Test that expiration date is 1 year on
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
        # Test that valid CertificateInfo passes validation
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
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpassword")

    def test_valid_user_login(self):
        # POST request with valid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'testpassword',
        }, follow=True)

        # user successfully logged in
        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)  # Check session for login
        self.assertContains(response, "Succesfully logged in", html=False)

    def test_invalid_user_login(self):
        # POST request with invalid credentials
        response = self.client.post(reverse('index'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        }, follow=True)

        # Check that the user is not logged in
        self.assertNotIn('_auth_user_id', self.client.session)  # No login in session
        self.assertContains(response, "There was an error login, please try again")

    def test_get_request(self):
        # GET request
        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

# Tests for viewing Holder-info
class HolderInfoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.holder_info_url = reverse('holder-info', kwargs={'pk': self.holder.id})
        self.index_url = reverse('index')

    def test_authenticated_user_can_access_holder_info(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.get(self.holder_info_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'holder-info.html')
        self.assertEqual(response.context['holder_record'], self.holder)

    def test_unauthenticated_user_redirected_to_index(self):
        # GET request without logging in
        response = self.client.get(self.holder_info_url)

        # Verify redirection to index
        self.assertRedirects(response, self.index_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))

    def test_holder_info_nonexistent_record(self):
        self.client.login(username='testuser', password='testpassword')

        # GET request for a non-existent record
        non_existent_url = reverse('holder-info', kwargs={'pk': 9999})
        with self.assertRaises(ObjectDoesNotExist):
            self.client.get(non_existent_url)

    def test_unauthenticated_user_nonexistent_record(self):
        # GET request for a non-existent record without logging in
        non_existent_url = reverse('holder-info', kwargs={'pk': 9999})
        response = self.client.get(non_existent_url)

        self.assertRedirects(response, self.index_url)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))

# Tests for Deleting Holder-info
class DeleteCertHolderTests(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_user(username='admin', password='adminpassword', is_superuser=True)
        self.regular_user = User.objects.create_user(username='user', password='userpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        # URLs
        self.delete_cert_holder_url = reverse('delete-holder-info', kwargs={'pk': self.certificate_holder.pk})
        self.certificate_holders_url = reverse('certificate-holders')

    def test_superuser_can_delete_certificate_holder(self):
        # Log in as the superuser
        self.client.login(username='admin', password='adminpassword')

        # Send delete request
        response = self.client.get(self.delete_cert_holder_url)

        # Check if the certificate holder is deleted
        with self.assertRaises(CertificateHolder.DoesNotExist):
            CertificateHolder.objects.get(id=self.certificate_holder.id)

        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Certificate holder deleted successfully' for message in messages))

        self.assertRedirects(response, self.certificate_holders_url)

    def test_regular_user_cannot_delete_certificate_holder(self):
        # Log in as a regular user
        self.client.login(username='user', password='userpassword')

        # Try to send a delete request
        response = self.client.get(self.delete_cert_holder_url)

        # Check that the certificate holder is still in the database
        CertificateHolder.objects.get(id=self.certificate_holder.id)

        # Check for the 'Admin login required' message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Admin login required' for message in messages))

        self.assertRedirects(response, self.certificate_holders_url)

# Tests for updating Certificate Holders
class UpdateCertHolderTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.update_cert_holder_url = reverse('update-holder-info', kwargs={'pk': self.certificate_holder.id})
        self.certificate_holders_url = reverse('certificate-holders')

    def test_invalid_form_submission(self):
        self.client.login(username='testuser', password='testpassword')

        # GET request for form
        response = self.client.get(self.update_cert_holder_url)

        # invalid data (e.g., empty first name)
        invalid_data = {
            'first_name': '',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'date_of_birth': '1995-05-05',
        }

        # POST request with invalid data
        response = self.client.post(self.update_cert_holder_url, invalid_data)

        # Check that the form is re-rendered with errors
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')

        # Check if the certificate holder's data is unchanged
        self.certificate_holder.refresh_from_db()
        self.assertEqual(self.certificate_holder.first_name, 'John')

# Tests for viewing Certificate-info
class CertificateInfoViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.certificate_info = CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2023-01-01',
            certificate_expiration_date='2024-01-01'
        )

        self.certificate_info_url = reverse('certificate-info', kwargs={'pk': self.certificate_info.certificate_number})
        self.index_url = reverse('index')

    def test_authenticated_user_can_view_certificate_info(self):
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to certificate_info
        response = self.client.get(self.certificate_info_url)

        # Verify the response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'certificate-info.html')
        self.assertEqual(response.context['certificate_record'], self.certificate_info)

    def test_unauthenticated_user_cannot_view_certificate_info(self):
        # GET request without logging in
        response = self.client.get(self.certificate_info_url)

        # Check for redirection to index page
        self.assertRedirects(response, self.index_url)

        # Check for the message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Please log in to view this page' for message in messages))

# Tests for Deleting Certificate-info
class DeleteCertificateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superuser = User.objects.create_superuser(username='admin', password='adminpassword')

        self.certificate_holder = CertificateHolder.objects.create(
            nhs_number=1000000001,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            date_of_birth='2000-01-01'
        )

        self.certificate_info = CertificateInfo.objects.create(
            certificate_holder=self.certificate_holder,
            certificate_start_date='2023-01-01',
            certificate_expiration_date='2024-01-01'
        )

        # URL for the delete_certificate
        self.delete_cert_url = reverse('delete-certificate', kwargs={'pk': self.certificate_info.certificate_number})
        self.certificates_url = reverse('certificates')

    def test_superuser_can_delete_certificate(self):
        # Log in as superuser
        self.client.login(username='admin', password='adminpassword')

        # Send GET request to delete the certificate
        response = self.client.get(self.delete_cert_url)

        # Certificate is deleted from the database
        with self.assertRaises(CertificateInfo.DoesNotExist):
            CertificateInfo.objects.get(certificate_number=self.certificate_info.certificate_number)

        # Success message and redirection
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Certificate deleted successfully' for message in messages))
        self.assertRedirects(response, self.certificates_url)

    def test_non_superuser_cannot_delete_certificate(self):
        # Log in as non-superuser
        self.client.login(username='testuser', password='testpassword')

        # Send GET request to delete the certificate
        response = self.client.get(self.delete_cert_url)

        # Ensure no deletion occurs
        self.assertEqual(CertificateInfo.objects.count(), 1)

        # Check for the 'Admin login required' message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any(str(message) == 'Admin login required' for message in messages))

        # Verify redirection to the certificates list
        self.assertRedirects(response, self.certificates_url)